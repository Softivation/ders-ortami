"""2. Çok rotorlu: GUIDED modda 10 m'ye kalkış, 5 sn bekleme, iniş; irtifa grafiği irtifa.png'ye.

Önce: ./sitl/baslat.sh   Sonra: python ornekler/python/02_kalkis_ve_inis.py
"""
import time
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from pymavlink import mavutil
from ortak import baglan, hazir_bekle, mod, arm, disarm_bekle

HEDEF = 10  # m

m = baglan()
hazir_bekle(m)
mod(m, "GUIDED")
arm(m)
m.mav.command_long_send(m.target_system, m.target_component, mavutil.mavlink.MAV_CMD_NAV_TAKEOFF, 0, 0, 0, 0, 0, 0, 0, HEDEF)
print(f"Kalkış: hedef {HEDEF} m")

zaman, irtifa = [], []
bas = time.time()
asama, tepe = "kalkis", None
while True:
    p = m.recv_match(type="GLOBAL_POSITION_INT", blocking=True, timeout=5)
    if p is None or p.get_srcSystem() != m.target_system:
        continue
    h = p.relative_alt / 1000
    zaman.append(time.time() - bas); irtifa.append(h)
    if asama == "kalkis" and h >= HEDEF * 0.95:
        print(f"{h:.1f} m'ye ulaşıldı, 5 sn bekleniyor"); asama, tepe = "bekle", time.time()
    elif asama == "bekle" and time.time() - tepe > 5:
        mod(m, "LAND"); asama = "inis"
    elif asama == "inis" and h < 0.3:
        break

disarm_bekle(m)
plt.figure(figsize=(7, 3.5))
plt.plot(zaman, irtifa, color="#1f6fb2")
plt.axhline(HEDEF, ls="--", color="#999")
plt.xlabel("zaman (sn)"); plt.ylabel("yerden yükseklik (m)"); plt.title("Kalkış ve iniş")
plt.tight_layout(); plt.savefig("irtifa.png", dpi=120)
print("Grafik: irtifa.png")
