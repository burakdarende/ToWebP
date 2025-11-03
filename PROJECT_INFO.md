# 🎯 Proje Özeti - Image to WebP Converter

## 📋 Proje Yapısı

```
ToWebP/
├── 📄 gui.py              # Ana GUI uygulaması
├── 📄 converter.py        # Dönüştürme motoru
├── 📄 build_exe.py        # EXE/APP builder
├── 📄 test.py             # Test scripti
│
├── 🚀 start.bat           # Windows hızlı başlatma
├── 🚀 start.ps1           # Windows PowerShell başlatma
├── 🚀 start.sh            # macOS/Linux başlatma
│
├── 🔨 build.ps1           # Windows build scripti
├── 🔨 build.sh            # macOS/Linux build scripti
│
├── 📖 README.md           # İngilizce dokümantasyon
├── 📖 KULLANIM.md         # Türkçe kullanım kılavuzu
├── 📋 requirements.txt    # Python bağımlılıkları
└── 🚫 .gitignore         # Git ignore dosyası
```

## 🎨 Özellikler

### ✅ Temel Özellikler

- ✨ Modern, karanlık tema GUI
- 📁 Klasör yapısını birebir kopyalama
- 🔄 Çoklu format desteği (JPG, PNG, BMP, TIFF, GIF)
- ⚙️ Kalite ve sıkıştırma ayarları
- 📊 Gerçek zamanlı ilerleme göstergesi
- 📝 Detaylı log kaydı

### 🖥️ Platform Desteği

- ✅ Windows (7, 8, 10, 11)
- ✅ macOS (10.12+)
- ✅ Linux (Ubuntu, Debian, Fedora, vb.)

### 🎁 Ekstra Özellikler

- 🔒 Orijinal dosyalar korunur
- 🚀 Standalone EXE/APP oluşturma
- 🌐 İnternet gerektirmez
- 🎯 Çok kolay kullanım

## 🚀 Kullanım Senaryoları

### Senaryo 1: Direkt Çalıştırma (Hızlı)

```bash
# Windows
start.bat

# macOS/Linux
chmod +x start.sh
./start.sh
```

### Senaryo 2: Python ile Çalıştırma

```bash
pip install -r requirements.txt
python gui.py
```

### Senaryo 3: EXE/APP Oluşturma (Dağıtım için)

```bash
# Windows
.\build.ps1

# macOS/Linux
chmod +x build.sh
./build.sh
```

## 💻 Teknik Detaylar

### Kullanılan Teknolojiler

| Teknoloji     | Versiyon | Amaç              |
| ------------- | -------- | ----------------- |
| Python        | 3.8+     | Ana dil           |
| Pillow        | 10.0+    | Görüntü işleme    |
| CustomTkinter | 5.2+     | Modern GUI        |
| PyInstaller   | Latest   | EXE/APP oluşturma |

### Desteklenen Formatlar

| Format | Uzantı      | Notlar                 |
| ------ | ----------- | ---------------------- |
| JPEG   | .jpg, .jpeg | En yaygın format       |
| PNG    | .png        | Şeffaflık desteği      |
| BMP    | .bmp        | Windows bitmap         |
| TIFF   | .tiff, .tif | Yüksek kalite          |
| GIF    | .gif        | Animasyon desteklenmez |

### Performans Metrikleri

- **Ortalama Hız:** ~50-100 resim/dakika (5MB, Quality 85)
- **RAM Kullanımı:** ~100-300 MB
- **CPU Kullanımı:** Tek çekirdek, %50-80
- **Disk I/O:** Sıralı okuma/yazma

## 🎓 Kod Yapısı

### converter.py - Ana Dönüştürme Motoru

```python
class ImageToWebPConverter:
    - convert_folder()      # Ana dönüştürme fonksiyonu
    - _count_images()       # Resim sayma
    - _process_directory()  # Klasör işleme
    - _convert_image()      # Tek resim dönüştürme
```

### gui.py - Grafik Arayüz

```python
class WebPConverterGUI:
    - _setup_ui()           # Arayüz kurulumu
    - _browse_folder()      # Klasör seçimi
    - _start_conversion()   # Dönüştürme başlatma
    - _convert_thread()     # Thread'de dönüştürme
    - _update_progress()    # İlerleme güncelleme
```

## 🔧 Geliştirme

### Yeni Özellik Ekleme

1. `converter.py` - Backend değişiklikler
2. `gui.py` - Frontend değişiklikler
3. `test.py` - Test ekle
4. Build ve test et

### Test Etme

```bash
python test.py
```

### Debug Modu

```python
# gui.py içinde
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 📊 Klasör Yapısı Örneği

### Input:

```
C:/serkan-fotolar/
├── 2023/
│   ├── yaz/
│   │   └── deniz.jpg
│   └── kis/
│       └── kar.png
└── ailecek.jpg
```

### Output:

```
C:/serkan-fotolar_WebP/    ← Sadece root'a _WebP eklenir
├── 2023/                   ← Alt klasörler aynı
│   ├── yaz/
│   │   └── deniz.webp
│   └── kis/
│       └── kar.webp
└── ailecek.webp
```

## 🎯 Kullanım İpuçları

### Fotoğraflar için:

```
Quality: 80
Lossless: ❌ Kapalı
Compression: 4
→ Sonuç: Dengeli kalite ve boyut
```

### Web için:

```
Quality: 75
Lossless: ❌ Kapalı
Compression: 3
→ Sonuç: Hızlı yükleme, iyi kalite
```

### Arşivleme için:

```
Quality: 100
Lossless: ✅ Açık
Compression: 6
→ Sonuç: Mükemmel kalite, yavaş
```

## 🐛 Bilinen Sorunlar

1. **Çok büyük resimler** (>50MB) RAM sorununa yol açabilir

   - Çözüm: Resimleri küçük gruplar halinde işleyin

2. **Animasyonlu GIF** desteği yok

   - Sadece ilk frame dönüştürülür

3. **macOS Gatekeeper** uyarısı
   - Çözüm: `xattr -cr ImageToWebP.app`

## 📈 Gelecek Özellikler (TODO)

- [ ] Toplu yeniden boyutlandırma
- [ ] Animasyonlu GIF desteği
- [ ] Drag & drop özelliği
- [ ] Çoklu işlemci desteği (multiprocessing)
- [ ] Önizleme özelliği
- [ ] Dosya karşılaştırma (önce/sonra)
- [ ] Komut satırı arayüzü (CLI)
- [ ] Toplu isim değiştirme

## 📞 İletişim ve Destek

- **GitHub Issues:** Sorunlar ve öneriler için
- **README.md:** Genel bilgi
- **KULLANIM.md:** Detaylı kullanım kılavuzu

## 📄 Lisans

Bu proje açık kaynak kodludur ve özgürce kullanılabilir.

## 🙏 Teşekkürler

- **Pillow Team:** Harika image processing kütüphanesi için
- **CustomTkinter:** Modern GUI framework'ü için
- **PyInstaller:** Standalone executable desteği için

---

**Geliştirici Notu:** Bu proje, klasör yapısını koruyarak toplu resim dönüştürme ihtiyacından doğmuştur. Amacı, kullanıcı dostu ve güçlü bir araç sunmaktır.

Keyifli kullanımlar! 🚀
