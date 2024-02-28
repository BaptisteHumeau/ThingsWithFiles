import os
import re
from PyPDF2 import PdfReader
import tkinter as tk
from tkinter import filedialog

root = tk.Tk()
root.withdraw()

destination_directory = filedialog.askdirectory(title="Select Directory Containing PDF Files")

if not destination_directory:
    print("No directory selected. Exiting...")
    exit()

input1 = input("Enter the string on the left bound of your pattern: ")
input2 = input("Enter the string on the right bound of your pattern: ")
pattern = re.compile(rf'{re.escape(input1)}(.+?){re.escape(input2)}', re.IGNORECASE)

suffix = input("Enter a Suffix to append to the renamed files: ")

for filename in os.listdir(destination_directory):
    if filename.lower().endswith('.pdf'):
        file_path = os.path.join(destination_directory, filename)

        file = open(file_path, 'rb')
        reader = PdfReader(file)
        text = reader.pages[0].extract_text()
        text = text.replace('\n', '')
        match = re.search(pattern, text)

        if match:
            extracted_string = match.group(1).strip()
            new_filename = f"{extracted_string}_{suffix}.pdf"
            file.close()

            count = 1
            while os.path.exists(os.path.join(destination_directory, new_filename)):
                new_filename = f"{extracted_string}_{suffix}_{count}.pdf"
                count += 1

            os.rename(file_path, os.path.join(destination_directory, new_filename))
            print(f"Renamed '{filename}' to '{new_filename}'")
        else:
            file.close()
            print(f"Pattern not found in '{filename}'")
