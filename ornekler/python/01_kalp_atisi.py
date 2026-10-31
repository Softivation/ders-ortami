"""1. Bağlan ve dinle: aracın kalp atışı, modu, konumu ve bataryası (her araç türünde çalışır).

Önce bir terminalde:  ./sitl/baslat.sh          (ya da: ./sitl/baslat.sh ucak, ./sitl/baslat.sh rover)
Sonra başka terminalde: python ornekler/python/01_kalp_atisi.py
"""
import time
from pymavlink import mavutil
from ortak import baglan

m = baglan()
son = time.time() + 10
while time.time() < son:
    msg = m.recv_match(type=["HEARTBEAT", "GLOBAL_POSITION_INT", "SYS_STATUS"], blocking=True, timeout=2)
    if msg is None or msg.get_srcSystem() != m.target_system:
        continue
    t = msg.get_type()
    if t == "HEARTBEAT":
        armli = bool(msg.base_mode & mavutil.mavlink.MAV_MODE_FLAG_SAFETY_ARMED)
        print(f"Kalp atışı · mod {mavutil.mode_string_v10(msg)} · {'arm' if armli else 'disarm'}")
    elif t == "GLOBAL_POSITION_INT":
        print(f"Konum · {msg.lat / 1e7:.6f}, {msg.lon / 1e7:.6f} · yerden {msg.relative_alt / 1000:.1f} m")
    elif t == "SYS_STATUS":
        print(f"Batarya · {msg.voltage_battery / 1000:.2f} V · %{msg.battery_remaining}")
