#!/usr/bin/env bash
# ArduPilot SITL'i ve MAVProxy'yi başlatır.
#   ./sitl/baslat.sh            çok rotorlu (ArduCopter)
#   ./sitl/baslat.sh ucak       sabit kanat (ArduPlane)
#   ./sitl/baslat.sh rover      kara aracı / İKA (ArduRover)
# Kodunuz udp:127.0.0.1:14550'ye, ikinci bir araç (ör. C# örneği) 14551'e bağlanır.
# Ev konumu Bursa'da bir nokta. Değiştirmek için: EV="enlem,boylam,irtifa,yön" ./sitl/baslat.sh
set -euo pipefail
KOK="$(cd "$(dirname "$0")/.." && pwd)"
SITL="${SITL_DIZIN:-$HOME/.sitl}"
EV="${EV:-40.1885,29.0610,100,0}"
CALISMA="$KOK/.sitl-calisma"
mkdir -p "$CALISMA"

case "${1:-copter}" in
  copter|cok-rotor) ikili=arducopter; model="+"; parm=copter.parm ;;
  ucak|plane)       ikili=arduplane;  model=plane; parm=plane.parm ;;
  rover|ika)        ikili=ardurover;  model=rover; parm=rover.parm ;;
  *) echo "Bilinmeyen araç: $1 (copter, ucak, rover)" >&2; exit 2 ;;
esac
[ -x "$SITL/$ikili" ] || { echo "SITL kurulu değil. Çalıştırın: .devcontainer/kurulum.sh" >&2; exit 1; }

# Önceki simülasyon açıksa kapanır; port (5760) boşalana kadar beklenir
pkill -f "$SITL/ardu" 2>/dev/null || true
for _ in $(seq 20); do pgrep -f "$SITL/ardu" >/dev/null || break; sleep 0.5; done
cd "$CALISMA"
"$SITL/$ikili" --model "$model" --speedup 1 --defaults "$SITL/$parm" --home "$EV" -I0 > sitl.log 2>&1 &
echo "SITL başladı ($ikili, günlük: .sitl-calisma/sitl.log). MAVProxy açılıyor; çıkmak için: Ctrl+C"
sleep 2
exec mavproxy.py --master tcp:127.0.0.1:5760 --out udp:127.0.0.1:14550 --out udp:127.0.0.1:14551 --state-basedir "$CALISMA" "${@:2}"
