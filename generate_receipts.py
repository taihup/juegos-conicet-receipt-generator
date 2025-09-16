import csv
from PIL import Image, ImageDraw, ImageFont
import os

# === CONFIG ===
CSV_FILE = "participants.csv"       # CSV file with the columns: date, name, last name, dni, comprobante, monto
TEMPLATE_IMAGE = "comprobante_preinscripcion.png"  # Your background image
SIGNATURE_IMAGE = "signature.png"
OUTPUT_DIR = "output_images"     # Folder to save results
FONT_FILE = "arial.ttf"          # Path to a .ttf font file
FONT_SIZE = 50
TEXT_COLOR = (0, 0, 0)           # Black text


# Attributes to fill
DELEGACION_NAME_POSITION = (1100, 100)  # (x, y) position in pixels
NAME_POSITION = (450, 300)       # (x, y) position in pixels
RECEIPT_NUMBER_POSITION = (820, 240)  # (x, y) position in pixels
DATE_POSITION = (1200, 240)  # (x, y) position in pixels
DNI_POSITION = (200,420)  # (x, y) position in pixels
MONEY_POSITION = (760, 500)  # (x, y) position in pixels
MONEY_AGAIN_POSITION = (230, 830)  # (x, y) position in pixels
SIGNATURE_POSITION = (700, 580)  # (x, y) position in pixels


# === SCRIPT ===
def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Load font
    font = ImageFont.truetype(FONT_FILE, FONT_SIZE)
    
    # Initialize receipt number
    receipt_number = 0

    # Read CSV
    with open(CSV_FILE, newline='', encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if not row:  # skip empty lines
                continue
            date = "15/09/2025" # TODO: take the date from the form
            name = row[2].strip() # get the name from the .csv
            last_name = row[3].strip() # get the last name from the .csv
            dni = row[4].strip() # get the name from the .csv
            money = row[9].strip() # get the amount of money from the .csv
            name_and_last_name = name + " " + last_name
            receipt_number+=1 # increase receipt counter

            print("receipt_number: {} name_and_last_name: {} dni: {} money: {}".format(receipt_number, name_and_last_name, dni, money))

            # Open template image
            receipt_image = Image.open(TEMPLATE_IMAGE).convert("RGBA")
            draw = ImageDraw.Draw(receipt_image)

            # Open signature image and scale it
            signature_image = Image.open(SIGNATURE_IMAGE).convert("RGBA")
            scale = 0.5  # 50% smaller
            w, h = signature_image.size
            signature_image = signature_image.resize((int(w*scale), int(h*scale)))

            # Write text
            draw.text(DELEGACION_NAME_POSITION, "ROSARIO", font=font, fill=TEXT_COLOR)
            draw.text(NAME_POSITION, name_and_last_name, font=font, fill=TEXT_COLOR)
            draw.text(RECEIPT_NUMBER_POSITION, str(receipt_number), font=font, fill=TEXT_COLOR)
            draw.text(DATE_POSITION, date, font=font, fill=TEXT_COLOR)
            draw.text(DNI_POSITION, dni, font=font, fill=TEXT_COLOR)
            draw.text(MONEY_POSITION, money, font=font, fill=TEXT_COLOR)
            draw.text(MONEY_AGAIN_POSITION, money, font=font, fill=TEXT_COLOR)
            draw.bitmap(SIGNATURE_POSITION, signature_image, fill=TEXT_COLOR)

            # Save output
            output_path = os.path.join(OUTPUT_DIR, f"{name_and_last_name}.png")
            receipt_image.save(output_path)
            print(f"Saved: {output_path}")

if __name__ == "__main__":
    main()