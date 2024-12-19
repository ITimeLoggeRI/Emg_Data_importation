import fitz  # PyMuPDF
import os
import re

# "Find all XPS and OXPS files in the specified folder."
def get_xps_and_oxps_files(directory):
    return [os.path.join(directory, f) for f in os.listdir(directory) if f.endswith('.xps') or f.endswith('.oxps')]

# "Extract text and numbers from the content of the file."
def extract_text_and_numbers_from_xps(file_path):
    document = fitz.open(file_path)
    text_content = ""

    # "It scans the text on each page."
    for page_num in range(len(document)):
        page = document.load_page(page_num)
        #"Extract the page text and preserve the line breaks."
        text_content += page.get_text("text") + "\n"  # Her sayfadan sonra bir satır ekleyerek ayırma yapar

    # "Remove extra blanks."
    text_content = re.sub(r'\s+', ' ', text_content)  # Convert extra blanks into a single blank.
    return text_content.strip()  # "Trim leading and trailing blanks."

# "Write the text and numbers to the corresponding .txt file."
def write_text_to_txt(file_path, text_content, output_dir):
    base_name = os.path.basename(file_path)  # "Get the file name (without the extension)."
    txt_file_name = os.path.splitext(base_name)[0] + ".txt"  # "Create a file name with a .txt extension."
    output_file_path = os.path.join(output_dir, txt_file_name)  #"Set the output path."
    
    # "Write the text to the .txt file."
    with open(output_file_path, 'w', encoding='utf-8') as txt_file:
        txt_file.write(text_content)
    
    print(f"{output_file_path} dosyasına yazıldı.")

# "It scans the XPS and OXPS files in the folder and generates output .txt files."
def process_directory(directory, output_dir):
    # Klasördeki tüm XPS ve OXPS dosyalarını al
    xps_files = get_xps_and_oxps_files(directory)

    # Her dosya için işlemi uygula
    for xps_file in xps_files:
        text_content = extract_text_and_numbers_from_xps(xps_file)
        write_text_to_txt(xps_file, text_content, output_dir)

# "Take inputs from the user."
input_directory = input("Lütfen taranacak klasör yolunu girin: ")
output_directory = input("Lütfen çıkış klasörünü girin (txt dosyaları için): ")

# "Process the files in the folder."
process_directory(input_directory, output_directory)
