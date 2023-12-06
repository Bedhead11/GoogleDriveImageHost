import csv
import tkinter as tk
from tkinter import filedialog, ttk
from PIL import Image, ImageTk

class CSVConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Google Drive Link Converter")
        self.root.geometry("520x700")  # Adjusted height
        self.root.configure(bg="#2E2E2E")

        # Image Display
        self.image_path = "guideImage.png"
        self.display_image()

        # Instructions Text
        instructions_text = (
            "Instructions:\n"
            "1. Click 'Browse for Input File' to select an input CSV file.\n"
            "2. Click 'Browse for Output Location' to select an output CSV file.\n"
            "3. Ensure the input CSV file has columns 'Image Title' and 'Image Link'.\n"
            "   Example: Title,https://drive.google.com/file/d/abc1234567/view\n"
            "4. (Optional) Click 'Create Template File' to generate a template CSV file for input.\n"
            "   This file is optional and can be used to structure your input data.\n"
            "5. Click 'Process' to convert the CSV file, adding an 'Embeddable Link' column.\n"
            "6. The converted CSV file will be saved to the specified output location."
        )

        instructions_label = tk.Label(
            self.root, text=instructions_text, justify=tk.LEFT, bg="#2E2E2E", fg="white"
        )
        instructions_label.pack(pady=10)

        # File Browser Inputs
        self.input_csv_entry = tk.Entry(self.root, width=50, bg="#4E4E4E", fg="white")
        self.input_csv_entry.pack(padx=10, pady=5)

        self.output_csv_entry = tk.Entry(self.root, width=50, bg="#4E4E4E", fg="white")
        self.output_csv_entry.pack(padx=10, pady=5)

        self.browse_input_button = tk.Button(
            self.root, text="Browse for Input File", command=self.choose_input_file, bg="#1E1E1E", fg="white"
        )
        self.browse_input_button.pack(pady=5)

        self.browse_output_button = tk.Button(
            self.root, text="Browse for Output Location", command=self.choose_output_file, bg="#1E1E1E", fg="white"
        )
        self.browse_output_button.pack(pady=5)

        self.create_template_button = tk.Button(
            self.root, text="Create Template File (Optional)", command=self.create_template_file, bg="#1E1E1E", fg="white"
        )
        self.create_template_button.pack(pady=5)

        self.process_button_file_browser = tk.Button(
            self.root, text="Process", command=self.process_conversion_file_browser, bg="#1E1E1E", fg="white"
        )
        self.process_button_file_browser.pack(pady=5)

        self.convert_status_label = tk.Label(self.root, text="", bg="#2E2E2E", fg="white")
        self.convert_status_label.pack(pady=10)

        # Copyright Label
        copyright_label = tk.Label(
            self.root, text="© 2023 Chase Pronger", bg="#2E2E2E", fg="white", font=("Arial", 8)
        )
        copyright_label.pack(side=tk.RIGHT, anchor=tk.SE, padx=10, pady=10)

    def display_image(self):
        image = Image.open(self.image_path)
        photo = ImageTk.PhotoImage(image)

        img_label = tk.Label(self.root, image=photo, bg="#2E2E2E")
        img_label.image = photo  # to prevent image from being garbage collected
        img_label.pack(pady=10)

    def choose_input_file(self):
        file_path = filedialog.askopenfilename(
            title="Select Input CSV file",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        self.input_csv_entry.delete(0, tk.END)
        self.input_csv_entry.insert(0, file_path)

    def choose_output_file(self):
        file_path = filedialog.asksaveasfilename(
            title="Select Output CSV file",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
            defaultextension=".csv"
        )
        self.output_csv_entry.delete(0, tk.END)
        self.output_csv_entry.insert(0, file_path)

    def create_template_file(self):
        template_path = filedialog.asksaveasfilename(
            title="Save Template CSV file",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
            defaultextension=".csv"
        )

        if template_path:
            with open(template_path, 'w', newline='') as template_file:
                fieldnames = ['Image Title', 'Image Link']
                writer = csv.DictWriter(template_file, fieldnames=fieldnames)
                writer.writeheader()
                self.convert_status_label.config(text=f"Template created. Save your input data in this format.")

    def process_conversion_file_browser(self):
        input_csv_file = self.input_csv_entry.get()
        output_csv_file = self.output_csv_entry.get()

        if not input_csv_file or not output_csv_file:
            self.convert_status_label.config(text="Please select input and output files.")
            return

        try:
            self.convert_status_label.config(text="Converting...")
            process_csv(input_csv_file, output_csv_file)
            self.convert_status_label.config(text=f"Conversion complete. Output saved to {output_csv_file}")
        except Exception as e:
            self.convert_status_label.config(text=f"An error occurred: {e}")

def convert_to_embeddable_link(gdrive_link):
    # Example: https://drive.google.com/file/d/abc1234567/view
    file_id = gdrive_link.split("/")[-2]
    direct_download_link = f"https://drive.google.com/uc?id={file_id}"
    return direct_download_link

def process_csv(input_csv, output_csv):
    with open(input_csv, 'r') as input_file, open(output_csv, 'w', newline='') as output_file:
        reader = csv.DictReader(input_file)
        fieldnames = reader.fieldnames + ['Embeddable Link']

        writer = csv.DictWriter(output_file, fieldnames=fieldnames)
        writer.writeheader()

        for row in reader:
            gdrive_link = row['Image Link']
            embeddable_link = convert_to_embeddable_link(gdrive_link)

            row['Embeddable Link'] = embeddable_link
            writer.writerow(row)

if __name__ == "__main__":
    root = tk.Tk()
    app = CSVConverterApp(root)
    root.mainloop()