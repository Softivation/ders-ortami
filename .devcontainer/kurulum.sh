#!/usr/bin/env bash
# Codespace ilk açıldığında bir kez çalışır: Python paketleri ve ArduPilot SITL ikilileri.
# Her indirilen dosyanın SHA-256 özeti sitl/surumler.txt ile karşılaştırılır; tutmazsa kurulum durur.
set -euo pipefail
KOK="$(cd "$(dirname "$0")/.." && pwd)"
HEDEF="${SITL_DIZIN:-$HOME/.sitl}"

echo "Python paketleri kuruluyor…"
python3 -m pip install --no-cache-dir --disable-pip-version-check -q -r "$KOK/requirements.txt"
python3 -m pip install --no-cache-dir --disable-pip-version-check -q --no-deps MAVProxy==1.8.75

echo "ArduPilot SITL indiriliyor (çok rotorlu, sabit kanat, kara aracı)…"
mkdir -p "$HEDEF"
gecici="$(mktemp -d)"
trap 'rm -rf "$gecici"' EXIT
grep -v '^#' "$KOK/sitl/surumler.txt" | while read -r ad adres ozet; do
  [ -n "${ad:-}" ] || continue
  curl --proto '=https' --tlsv1.2 -fsSL --retry 3 -o "$gecici/$ad" "$adres"
  echo "$ozet  $gecici/$ad" | sha256sum -c --quiet - || { echo "HATA: $ad özeti tutmadı, kurulum durdu." >&2; exit 1; }
  install -m 0644 "$gecici/$ad" "$HEDEF/$ad"
  case "$ad" in ardu*) chmod 0755 "$HEDEF/$ad" ;; esac
done

echo "Hazır. Simülasyonu başlatmak için: ./sitl/baslat.sh (ayrıntı README.md)"
