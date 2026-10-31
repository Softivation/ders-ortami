// MAVLink'i kütüphanesiz okumak: UDP 14551'den gelen paketlerin başlığını çözer, HEARTBEAT ve GLOBAL_POSITION_INT'i yazar.
// Önce: ./sitl/baslat.sh   Sonra: dotnet run --project ornekler/csharp/MavlinkDinle
// MAVLink v2 paketi: 0xFD | uzunluk | uyumsuz bayrak | uyumlu bayrak | sıra | sistem | bileşen | mesaj no (3 bayt) | veri | CRC (2) [| imza (13)]
using System.Buffers.Binary;
using System.Net;
using System.Net.Sockets;

using var udp = new UdpClient(new IPEndPoint(IPAddress.Loopback, 14551));
Console.WriteLine("UDP 14551 dinleniyor (10 sn)…");
var son = DateTime.UtcNow.AddSeconds(10);
var sayac = new Dictionary<uint, int>();

while (DateTime.UtcNow < son)
{
    var bekle = udp.ReceiveAsync();
    if (await Task.WhenAny(bekle, Task.Delay(2000)) != bekle) continue;
    var b = bekle.Result.Buffer;
    for (int i = 0; i + 12 <= b.Length;)
    {
        if (b[i] != 0xFD) { i++; continue; }           // yalnız MAVLink v2
        int uzunluk = b[i + 1];
        bool imzali = (b[i + 2] & 0x01) != 0;
        int toplam = 10 + uzunluk + 2 + (imzali ? 13 : 0);
        if (i + toplam > b.Length) break;
        byte sistem = b[i + 5];
        uint no = (uint)(b[i + 7] | b[i + 8] << 8 | b[i + 9] << 16);
        // MAVLink v2 sondaki sıfır baytları kırpar; okumadan önce veri tam boyuna sıfırla tamamlanır
        var veri = new byte[255];
        Array.Copy(b, i + 10, veri, 0, uzunluk);
        sayac[no] = sayac.GetValueOrDefault(no) + 1;

        if (no == 0 && sistem != 255)                   // HEARTBEAT (255: yer istasyonu)
        {
            uint ozelMod = BinaryPrimitives.ReadUInt32LittleEndian(veri);
            byte tur = veri[4], temelMod = veri[6];
            bool armli = (temelMod & 0x80) != 0;
            Console.WriteLine($"Kalp atışı · sistem {sistem} · araç türü {tur} · özel mod {ozelMod} · {(armli ? "arm" : "disarm")}");
        }
        else if (no == 33)                              // GLOBAL_POSITION_INT
        {
            int lat = BinaryPrimitives.ReadInt32LittleEndian(veri.AsSpan(4));
            int lon = BinaryPrimitives.ReadInt32LittleEndian(veri.AsSpan(8));
            int yerden = BinaryPrimitives.ReadInt32LittleEndian(veri.AsSpan(16));
            Console.WriteLine($"Konum · {lat / 1e7:F6}, {lon / 1e7:F6} · yerden {yerden / 1000.0:F1} m");
        }
        i += toplam;
    }
}

Console.WriteLine("En sık gelen mesajlar (mesaj no: adet): " +
    string.Join(", ", sayac.OrderByDescending(k => k.Value).Take(5).Select(k => $"{k.Key}: {k.Value}")));
