# Türkiye Adres Verisi (il / ilçe / mahalle)

Shopify ödeme sayfasındaki **Türkiye Adres Seçici** eklentisinin mahalle listelerini
çektiği statik veri. Sunucu yok; dosyalar jsDelivr CDN üzerinden sunulur:

```
https://cdn.jsdelivr.net/gh/<hesap>/turkiye-adres-verisi@main/ilce/<ilçe-id>.json
```

| Dosya | İçerik |
|---|---|
| `il.json` | 81 il: `{"id","ad"}` |
| `ilce.json` | 973 ilçe: `{"id","il","ad"}` |
| `ilce/<id>.json` | O ilçenin mahalle/köy adları, Türkçe alfabeye göre sıralı |

Kaynak: PTT verisi, [serhatmorkoc/PTT-il-ilce-semt-mahalle-jsondata](https://github.com/serhatmorkoc/PTT-il-ilce-semt-mahalle-jsondata).
Adlar PTT biçiminde: `Akpınar Mah`, `Çakmak Mah (Akdurak Köyü)`.

## Güncelleme

```
python uret.py
git add -A && git commit -m "Veri güncellendi" && git push
```

jsDelivr `@main` dosyalarını en geç 12 saat içinde yeniler. Eklentiyi yeniden
yüklemek gerekmez.
