# 📘 Kullanım Kılavuzu - Image to WebP Converter

## 🚀 Hızlı Başlangıç

### Windows Kullanıcıları için

#### Seçenek 1: Programı Direkt Çalıştırma (Önerilen)

```powershell
python gui.py
```

#### Seçenek 2: EXE Dosyası Oluşturma

1. PowerShell'i açın
2. Proje klasörüne gidin
3. Şu komutu çalıştırın:

```powershell
.\build.ps1
```

4. `dist` klasöründe `ImageToWebP.exe` dosyası oluşacak
5. Bu exe dosyasını istediğiniz yere kopyalayabilir, Python kurulumu olmadan çalıştırabilirsiniz!

### macOS Kullanıcıları için

#### Seçenek 1: Programı Direkt Çalıştırma (Önerilen)

```bash
python3 gui.py
```

#### Seçenek 2: APP Dosyası Oluşturma

1. Terminal'i açın
2. Proje klasörüne gidin
3. Build script'ini çalıştırılabilir yapın:

```bash
chmod +x build.sh
```

4. Build script'ini çalıştırın:

```bash
./build.sh
```

5. `dist` klasöründe `ImageToWebP.app` oluşacak
6. Bu app'i istediğiniz yere kopyalayabilir, Applications klasörüne taşıyabilirsiniz!

## 🎯 Nasıl Kullanılır?

### Adım 1: Kaynak Klasörü Seçin

1. "Browse" butonuna tıklayın
2. Resimlerin bulunduğu klasörü seçin (örnek: `C:/serkan-fotolar`)

### Adım 2: Ayarları Yapın

#### Kalite (Quality)

- **1-100 arası** değer
- **Önerilen:** 75-85 (dengeli kalite ve boyut)
- **Yüksek kalite için:** 90-100
- **Küçük dosya için:** 60-75

#### Lossless (Kayıpsız Sıkıştırma)

- ✅ **Açık:** Tamamen kayıpsız, mükemmel kalite ama daha büyük dosya
- ❌ **Kapalı:** Minimal kalite kaybı ama çok daha küçük dosya (önerilen)

#### Compression Level (Sıkıştırma Seviyesi)

- **0-6 arası** değer
- **4 (önerilen):** İyi denge
- **6:** En iyi sıkıştırma ama daha yavaş
- **0:** En hızlı ama daha büyük dosya

### Adım 3: Dönüştürmeyi Başlatın

1. "🚀 Start Conversion" butonuna tıklayın
2. İlerlemeyi izleyin
3. Tamamlandığında bildirim gelecek

### Adım 4: Sonucu Kontrol Edin

Yeni klasör oluşturuldu: `[kaynak-klasör]_WebP`

## 📂 Klasör Yapısı Örneği

### GİRDİ:

```
C:/serkan-fotolar/
├── 2023/
│   ├── yaz/
│   │   ├── deniz.jpg
│   │   └── kumsal.png
│   └── kis/
│       ├── kar.jpg
│       └── dag.bmp
├── 2024/
│   ├── ilkbahar/
│   │   └── cicekler.jpg
│   └── sonbahar/
│       └── yapraklar.png
└── ailecek.jpg
```

### ÇIKTI:

```
C:/serkan-fotolar_WebP/
├── 2023/
│   ├── yaz/
│   │   ├── deniz.webp
│   │   └── kumsal.webp
│   └── kis/
│       ├── kar.webp
│       └── dag.webp
├── 2024/
│   ├── ilkbahar/
│   │   └── cicekler.webp
│   └── sonbahar/
│       └── yapraklar.webp
└── ailecek.webp
```

## ✅ Desteklenen Formatlar

Program şu formatlardaki resimleri WebP'ye dönüştürür:

- 📷 JPEG (.jpg, .jpeg)
- 🖼️ PNG (.png)
- 🎨 BMP (.bmp)
- 📸 TIFF (.tiff, .tif)
- 🎬 GIF (.gif)

## 💡 İpuçları

### En İyi Ayarlar:

#### Fotoğraflar için:

- **Quality:** 80
- **Lossless:** Kapalı
- **Compression:** 4

#### Grafik/Logo için:

- **Quality:** 90
- **Lossless:** Açık
- **Compression:** 6

#### Web için Hız Optimizasyonu:

- **Quality:** 75
- **Lossless:** Kapalı
- **Compression:** 3

#### Arşivleme için:

- **Quality:** 100
- **Lossless:** Açık
- **Compression:** 6

## 🔧 Sorun Giderme

### Program Başlamıyor

```powershell
# Gereksinimleri yeniden yükleyin
pip install -r requirements.txt
```

### EXE/APP Oluşturmuyor

```powershell
# PyInstaller'ı yükleyin
pip install pyinstaller

# Tekrar deneyin
.\build.ps1  # Windows
./build.sh   # macOS
```

### Dönüştürme Hatası

- Kaynak klasörün var olduğundan emin olun
- Klasör izinlerini kontrol edin
- Disk alanınızın yeterli olduğundan emin olun

### macOS'ta "App is damaged" Hatası

```bash
# Güvenlik ayarlarını bypass edin
xattr -cr dist/ImageToWebP.app
```

## 🎓 Gelişmiş Kullanım

### Komut Satırından Modül Olarak Kullanma

```python
from converter import ImageToWebPConverter

# Converter oluştur
converter = ImageToWebPConverter(
    quality=85,
    lossless=False,
    method=4
)

# Dönüştür
output, total, processed, errors = converter.convert_folder(
    "C:/serkan-fotolar",
    progress_callback=lambda msg, cur, tot: print(f"{cur}/{tot}: {msg}")
)

print(f"Output: {output}")
print(f"Success: {processed}/{total}")
```

## 📊 Performans

### Dosya Boyutu Karşılaştırması (Ortalama):

- **PNG → WebP (Quality 80):** %60-80 küçültme
- **JPG → WebP (Quality 80):** %20-40 küçültme
- **BMP → WebP (Quality 80):** %90-95 küçültme

### İşlem Hızı (1000 adet 5MB fotoğraf):

- **Compression 0:** ~2-3 dakika
- **Compression 4:** ~4-5 dakika
- **Compression 6:** ~6-8 dakika

## 🛡️ Güvenlik

- ✅ Orijinal dosyalar **asla değiştirilmez**
- ✅ Sadece **okuma izni** gerekir
- ✅ Yeni klasöre **yazma izni** gerekir
- ✅ İnternet bağlantısı **gerekmez**
- ✅ Hiçbir veri **dışarı gönderilmez**

## 📞 Destek

Sorun yaşarsanız:

1. README.md dosyasını okuyun
2. GitHub'da issue açın
3. Hata mesajını ve log'ları ekleyin

## 🎉 Keyifli Kullanımlar!

Programı beğendiyseniz GitHub'da ⭐ vermeyi unutmayın!
