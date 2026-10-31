"""Örneklerin paylaştığı küçük yardımcılar: bağlanma, mod, arm, telemetri bekleme."""
import time
from pymavlink import mavutil

ADRES = "udpin:127.0.0.1:14550"  # sitl/baslat.sh MAVProxy üzerinden buraya gönderir


def baglan(adres=ADRES):
    print(f"{adres} dinleniyor (önce başka bir terminalde ./sitl/baslat.sh çalışmalı)…")
    m = mavutil.mavlink_connection(adres)
    # Hattaki ilk kalp atışı MAVProxy'nin (yer istasyonu) olabilir; aracın kendi kalp atışı beklenir
    son = time.time() + 30
    while True:
        h = m.recv_match(type="HEARTBEAT", blocking=True, timeout=5)
        if h and h.type != mavutil.mavlink.MAV_TYPE_GCS and h.autopilot != mavutil.mavlink.MAV_AUTOPILOT_INVALID:
            m.target_system, m.target_component = h.get_srcSystem(), h.get_srcComponent()
            break
        if time.time() > son:
            raise TimeoutError("Araçtan kalp atışı gelmedi. SITL açık mı? ./sitl/baslat.sh")
    print(f"Bağlandı: sistem {m.target_system}, bileşen {m.target_component}")
    # Örnekler için akış: konum ve durum saniyede 4 kez
    m.mav.request_data_stream_send(m.target_system, m.target_component, mavutil.mavlink.MAV_DATA_STREAM_ALL, 4, 1)
    return m


def hazir_bekle(m, sure=120):
    """EKF konumu güvenle kestirene kadar bekler (SITL açılışta ~20-40 sn)."""
    son = time.time() + sure
    while time.time() < son:
        s = m.recv_match(type="SYS_STATUS", blocking=True, timeout=2)
        e = m.recv_match(type="EKF_STATUS_REPORT", blocking=True, timeout=2)
        g = m.recv_match(type="GPS_RAW_INT", blocking=True, timeout=2)
        if e and g and g.fix_type >= 3 and (e.flags & 0x10):  # EKF_POS_HORIZ_ABS
            print(f"Hazır: GPS fix {g.fix_type}, {g.satellites_visible} uydu")
            return
        print("EKF ve GPS bekleniyor…")
    raise TimeoutError("Araç hazır olmadı; SITL günlüğüne bakın: .sitl-calisma/sitl.log")


def mod(m, ad):
    m.set_mode(m.mode_mapping()[ad])
    while True:
        h = m.recv_match(type="HEARTBEAT", blocking=True, timeout=5)
        if h and mavutil.mode_string_v10(h) == ad:
            print(f"Mod: {ad}")
            return


def arm(m, sure=60):
    son = time.time() + sure
    while time.time() < son:
        m.arducopter_arm()
        if _armli_bekle(m, 3):
            print("Arm edildi")
            return
        print("Arm reddedildi, ön kontroller bekleniyor…")
    raise TimeoutError("Arm edilemedi")


def _armli_bekle(m, sure):
    son = time.time() + sure
    while time.time() < son:
        h = m.recv_match(type="HEARTBEAT", blocking=True, timeout=1)
        if h and h.get_srcSystem() == m.target_system and (h.base_mode & mavutil.mavlink.MAV_MODE_FLAG_SAFETY_ARMED):
            return True
    return False


def disarm_bekle(m, sure=120):
    son = time.time() + sure
    while time.time() < son:
        h = m.recv_match(type="HEARTBEAT", blocking=True, timeout=2)
        if h and h.get_srcSystem() == m.target_system and not (h.base_mode & mavutil.mavlink.MAV_MODE_FLAG_SAFETY_ARMED):
            print("Disarm: araç indi")
            return
    raise TimeoutError("Araç disarm olmadı")
