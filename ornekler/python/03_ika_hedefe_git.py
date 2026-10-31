"""3. Kara aracı (İKA): GUIDED modda 40 m kuzeydeki noktaya sür, varınca dur.

Önce: ./sitl/baslat.sh rover   Sonra: python ornekler/python/03_ika_hedefe_git.py
"""
import math
from pymavlink import mavutil
from ortak import baglan, hazir_bekle, mod, arm

MESAFE = 40  # m, kuzeye


def uzaklik(lat1, lon1, lat2, lon2):
    """İki nokta arası yaklaşık yatay mesafe (m), haversine."""
    r = 6371000
    p1, p2 = math.radians(lat1), math.radians(lat2)
    a = math.sin((p2 - p1) / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(math.radians(lon2 - lon1) / 2) ** 2
    return 2 * r * math.asin(math.sqrt(a))


m = baglan()
hazir_bekle(m)
p = m.recv_match(type="GLOBAL_POSITION_INT", blocking=True, timeout=10)
lat0, lon0 = p.lat / 1e7, p.lon / 1e7
hedef_lat = lat0 + MESAFE / 111320  # 1 derece enlem ≈ 111,32 km
print(f"Başlangıç {lat0:.6f}, {lon0:.6f} → hedef {hedef_lat:.6f}, {lon0:.6f}")

mod(m, "GUIDED")
arm(m)
m.mav.set_position_target_global_int_send(
    0, m.target_system, m.target_component, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT_INT,
    0b110111111000,  # yalnız konum
    int(hedef_lat * 1e7), int(lon0 * 1e7), 0, 0, 0, 0, 0, 0, 0, 0, 0)

while True:
    p = m.recv_match(type="GLOBAL_POSITION_INT", blocking=True, timeout=5)
    if p is None or p.get_srcSystem() != m.target_system:
        continue
    kalan = uzaklik(p.lat / 1e7, p.lon / 1e7, hedef_lat, lon0)
    print(f"Hedefe {kalan:.1f} m, hız {math.hypot(p.vx, p.vy) / 100:.1f} m/s")
    if kalan < 2:
        break

mod(m, "HOLD")
m.arducopter_disarm()
print("Hedefe varıldı, araç durdu")
