import os
from PIL import Image

def optimize_webp(input_folder, output_folder, lossless=False, quality=70, method=6):
    """
    WebP dosyalarını yeniden kaydedip boyutunu küçültür.

    :param input_folder: Kaynak klasör yolu
    :param output_folder: Hedef klasör yolu
    :param lossless: True ise kayıpsız (lossless) sıkıştırma yapar
    :param quality: 0-100 arası kalite (lossless False olduğunda kullanılır)
    :param method: 0-6 arası sıkıştırma metodu (yüksek değer = daha iyi sıkıştırma, daha yavaş işlem)
    """
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(input_folder):
        if filename.lower().endswith(".webp"):
            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, filename)

            try:
                with Image.open(input_path) as img:
                    img.save(
                        output_path,
                        "WEBP",
                        lossless=lossless,
                        quality=quality,
                        method=method,
                        optimize=True
                    )
                print(f"{filename} optimize edildi.")
            except Exception as e:
                print(f"{filename} optimize edilirken hata oluştu: {e}")

if __name__ == "__main__":
    source_folder = input("Kaynak klasör yolunu girin: ").strip('"')
    target_folder = input("Kaydedilecek klasör yolunu girin: ").strip('"')

    # True = kalite kaybı olmadan sıkıştır
    optimize_webp(source_folder, target_folder, lossless=True)
    print("Tüm işlemler tamamlandı.")
