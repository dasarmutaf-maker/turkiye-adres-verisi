# -*- coding: utf-8 -*-
"""
PTT il/ilçe/mahalle verisinden ilçe başına mahalle dosyası üretir.

Çalıştır (Windows):  python uret.py
Kaynak: https://github.com/serhatmorkoc/PTT-il-ilce-semt-mahalle-jsondata

Çıktı:
  il.json          -> [{"id": 1, "ad": "Adana"}, ...]
  ilce.json        -> [{"id": 1, "il": 1, "ad": "Aladağ"}, ...]
  ilce/<id>.json   -> ["Akpınar Mah", "Başpınar Mah (Kızılca Köyü)", ...]

Eklenti "ilce/<id>.json" dosyasını jsDelivr üzerinden çeker. Dosya adı ilçe
kimliğidir; kimlikler eklentideki turkiye_adres_data.js ile aynı kaynaktan gelir.
"""
import json
import locale
import os
import re
import sys
import urllib.request

KAYNAK = "https://raw.githubusercontent.com/serhatmorkoc/PTT-il-ilce-semt-mahalle-jsondata/master"
KOK = os.path.dirname(os.path.abspath(__file__))

TR_SIRA = "aâbcçdefgğhıiîjklmnoöprsştuüûvyz"


def tr_anahtar(metin):
    """Türkçe alfabeye göre sıralama anahtarı (İ/ı doğru yere düşsün)."""
    m = metin.replace("I", "ı").replace("İ", "i").lower()
    return [TR_SIRA.index(h) if h in TR_SIRA else 100 + ord(h) for h in m]


def indir(ad):
    yol = os.path.join(KOK, "_kaynak", ad)
    if not os.path.exists(yol):
        os.makedirs(os.path.dirname(yol), exist_ok=True)
        print("indiriliyor:", ad)
        urllib.request.urlretrieve(f"{KAYNAK}/{ad}", yol)
    with open(yol, encoding="utf-8") as f:
        return json.load(f)


# PTT kaynağında büyük "İ" hiç yok, hepsi "I" olmuş ("Inönü", "Istiklal").
# Kelime başındaki I: ilk ünlü "ı" ise gerçekten I (Ilıca, Işık, Iğdır),
# değilse İ (İnönü, İstasyon, İmam). Kurala uymayan gerçek I kökleri:
GERCEK_I = ("Ihlamur", "Irmak", "Ilgaz", "Ilgar", "Ilgayır", "Islak", "Irgat",
            "Irgut", "Irlamaz", "Isot", "Izgar", "Isparta")
UNLU = "aâeıiîoöuüû"


def i_duzelt(kelime):
    if not kelime.startswith("I") or kelime.startswith(GERCEK_I):
        return kelime
    ilk = next((h for h in kelime[1:].lower() if h in UNLU), "")
    return kelime if ilk == "ı" else "İ" + kelime[1:]


def temizle(ad):
    ad = re.sub(r"\s+", " ", ad).strip()
    ad = re.sub(r"(?<![^\s(])I[^\s()]*", lambda m: i_duzelt(m.group(0)), ad)
    ad = ad.replace(" (", " (").replace("( ", "(").replace(" )", ")")
    return ad


def yaz(yol, veri):
    with open(os.path.join(KOK, yol), "w", encoding="utf-8", newline="\n") as f:
        json.dump(veri, f, ensure_ascii=False, separators=(",", ":"))
        f.write("\n")


def main():
    iller = indir("il.json")
    ilceler = indir("ilce.json")
    mahalleler = indir("mahalle.json")

    yaz("il.json", [{"id": i["id"], "ad": i["il_name"]} for i in iller])
    yaz("ilce.json", [{"id": i["id"], "il": i["il_id"], "ad": i["ilce_name"]} for i in ilceler])

    grup = {}
    for m in mahalleler:
        grup.setdefault(m["ilce_id"], set()).add(temizle(m["mahalle_name"]))

    os.makedirs(os.path.join(KOK, "ilce"), exist_ok=True)
    eksik = [i["id"] for i in ilceler if i["id"] not in grup]
    toplam = 0
    for ilce_id, adlar in grup.items():
        sirali = sorted(adlar, key=tr_anahtar)
        toplam += len(sirali)
        yaz(f"ilce/{ilce_id}.json", sirali)

    print(f"il: {len(iller)}  ilçe: {len(ilceler)}  mahalle: {toplam}  dosya: {len(grup)}")
    if eksik:
        print("mahallesi olmayan ilçe kimlikleri:", eksik)


if __name__ == "__main__":
    if sys.platform == "win32":
        sys.stdout.reconfigure(encoding="utf-8")
    main()
