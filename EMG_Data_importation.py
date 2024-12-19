import fitz  # PyMuPDF
import os
import re

# Belirtilen klasördeki tüm XPS ve OXPS dosyalarını bulur
def get_xps_and_oxps_files(directory):
    return [os.path.join(directory, f) for f in os.listdir(directory) if f.endswith('.xps') or f.endswith('.oxps')]

# Metin ve sayıları dosyanın içeriğinden çeker
def extract_text_and_numbers_from_xps(file_path):
    document = fitz.open(file_path)
    text_content = ""

    # Her sayfadaki metni tarar
    for page_num in range(len(document)):
        page = document.load_page(page_num)
        # Sayfa metnini al ve satırları koru
        text_content += page.get_text("text") + "\n"  # Her sayfadan sonra bir satır ekleyerek ayırma yapar

    # Fazla boşlukları temizle
    text_content = re.sub(r'\s+', ' ', text_content)  # Fazla boşlukları tek boşluk yapar
    return text_content.strip()  # Baş ve son boşlukları temizle

# Metin ve sayıları ilgili .txt dosyasına yazar
def write_text_to_txt(file_path, text_content, output_dir):
    base_name = os.path.basename(file_path)  # Dosya ismini al (uzantısız)
    txt_file_name = os.path.splitext(base_name)[0] + ".txt"  # .txt uzantılı dosya ismini oluştur
    output_file_path = os.path.join(output_dir, txt_file_name)  # Çıkış yolunu belirle
    
    # Metni .txt dosyasına yazar
    with open(output_file_path, 'w', encoding='utf-8') as txt_file:
        txt_file.write(text_content)
    
    print(f"{output_file_path} dosyasına yazıldı.")

# Klasördeki XPS ve OXPS dosyalarını tarar ve çıktı .txt dosyaları oluşturur
def process_directory(directory, output_dir):
    # Klasördeki tüm XPS ve OXPS dosyalarını al
    xps_files = get_xps_and_oxps_files(directory)

    # Her dosya için işlemi uygula
    for xps_file in xps_files:
        text_content = extract_text_and_numbers_from_xps(xps_file)
        write_text_to_txt(xps_file, text_content, output_dir)

# Kullanıcıdan girdileri al
input_directory = input("Lütfen taranacak klasör yolunu girin: ")
output_directory = input("Lütfen çıkış klasörünü girin (txt dosyaları için): ")

# Klasördeki dosyaları işle
process_directory(input_directory, output_directory)
