# Softivation ders ortamı

[Softivation](https://softivation.com) eğitimlerindeki kodu bilgisayarınıza bir şey kurmadan çalıştırın. Tarayıcıda açılan
hazır ortamda Python, pymavlink, MAVProxy ve ArduPilot simülasyonu (SITL) kurulu gelir: çok rotorlu, sabit kanat ve kara aracı (İKA).

[![Codespaces'te açın](https://github.com/codespaces/badge.svg)](https://codespaces.new/Softivation/ders-ortami?quickstart=1)

## Nasıl kullanılır

1. Yukarıdaki **Codespaces'te açın** düğmesine basın (GitHub hesabı gerekir). İlk açılış 3–5 dakika sürer; kurulum kendiliğinden yapılır.
2. Açılan editörde **Terminal**'de simülasyonu başlatın:
   ```bash
   ./sitl/baslat.sh          # çok rotorlu (ArduCopter)
   ./sitl/baslat.sh ucak     # sabit kanat (ArduPlane)
   ./sitl/baslat.sh rover    # kara aracı / İKA (ArduRover)
   ```
   MAVProxy konsolu açılır (`mode guided`, `arm throttle` gibi komutları buraya yazabilirsiniz).
3. İkinci bir terminal açın (+ işareti) ve bir örnek çalıştırın:
   ```bash
   cd ornekler/python
   python 01_kalp_atisi.py        # her araçta: kalp atışı, mod, konum, batarya
   python 02_kalkis_ve_inis.py    # çok rotorlu: 10 m kalkış, iniş, irtifa grafiği (irtifa.png)
   python 03_ika_hedefe_git.py    # kara aracı: 40 m kuzeye sür (önce ./sitl/baslat.sh rover)
   ```
4. C# ile MAVLink'i kütüphanesiz okumak için:
   ```bash
   dotnet run --project ornekler/csharp/MavlinkDinle
   ```

Kendi kodunuz `udp:127.0.0.1:14550` adresine bağlanır (`ornekler/python/ortak.py`). İkinci bir program 14551'i dinleyebilir.

## Ücret

Codespaces, GitHub'ın kişisel hesaplara verdiği aylık ücretsiz kullanımdan düşer (şu an ücretsiz hesapta ayda 120 çekirdek saati;
bu ortam 2 çekirdekli olduğu için yaklaşık 60 saat). Hesabınızda ödeme yöntemi yoksa kota bitince durur, ücret çıkmaz. İşiniz bitince
Codespace'i **durdurun** (GitHub → Codespaces); 30 dakika boşta kalınca kendisi de durur. Güncel koşullar:
[GitHub Codespaces faturalandırması](https://docs.github.com/en/billing/concepts/product-billing/github-codespaces).

## Colab defterleri (Google hesabıyla, kurulumsuz)

Simülasyon gerektirmeyen alıştırmalar Google Colab'da da açılır:

| Defter | Açın |
|---|---|
| MAVLink mesajını kodlayın ve çözün | [![Colab'da açın](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Softivation/ders-ortami/blob/main/colab/01_mavlink.ipynb) |
| PID ile irtifa tutma | [![Colab'da açın](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Softivation/ders-ortami/blob/main/colab/02_pid.ipynb) |
| İki GPS noktası arası mesafe ve yön | [![Colab'da açın](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Softivation/ders-ortami/blob/main/colab/03_gps.ipynb) |

Aynı alıştırmalar sitede de, hiçbir hesap gerekmeden çalışır: [Python deneme alanı](https://softivation.com/kaynaklar/python-deneme-alani).

## Güvenlik

- Ortam hiçbir gizli değer (secret, token) kullanmaz ve istemez. Bir yerde parola ya da anahtar girmeniz istenirse bu depodan değildir.
- Simülasyon ve MAVLink bağlantı noktaları dışarı açılmaz; yalnız Codespace'in içinde çalışır.
- Bütün sürümler sabittir: Python paketleri `requirements.txt`'te, SITL ikilileri `sitl/surumler.txt`'te SHA-256 özetiyle. İndirilen
  dosyanın özeti tutmazsa kurulum durur. Güncellemeleri Dependabot önerir, Softivation inceleyip birleştirir.
- Bu depoya yalnız Softivation yazar. Bir güvenlik sorunu görürseniz: iletisim@softivation.com.

## İçindekiler

| Yol | Ne |
|---|---|
| `.devcontainer/` | Codespaces tanımı (Python 3.12, .NET 8) ve kurulum betiği |
| `sitl/` | SITL sürümleri, özetleri ve başlatma betiği |
| `ornekler/python/` | pymavlink örnekleri |
| `ornekler/csharp/` | C# ile MAVLink okuma |
| `colab/` | Google Colab defterleri |

ArduPilot, pymavlink ve MAVProxy kendi lisanslarıyla (GPLv3 / LGPLv3) dağıtılır; bu depo onları değiştirmeden, resmî kaynaklarından indirir.
