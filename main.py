import csv
import os
import smtplib
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders
from PIL import Image, ImageDraw, ImageFont
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader

# ── EMAIL SETTINGS ─────────────────────────────────────────
SENDER_EMAIL = "tupshendrekumar9@gmail.com"
APP_PASSWORD  = "joqioqwoeydnwclg"
# ───────────────────────────────────────────────────────────

CSV_FILE      = "participants.csv"
OUTPUT_FOLDER = "certificates"
DESIGNS       = ["design1.jpg", "design2.jpg","design3.jpg"]

DESIGN_CONFIG = {
    "design1.jpg": {
        "x": 0.30, "y": 0.55,
        "font_size": 85,
        "color": (0, 220, 220)
    },
    "design2.jpg": {
        "x": 0.50, "y": 0.41,
        "font_size": 72,
        "color": (0, 80, 60)
    },
    "design3.jpg":{
        "x":0.50,"y": 0.48,
        "font_size":70,
        "color": (212,175,55)
    },
}

def get_font(size):
    font_paths = [
        "C:/Windows/Fonts/georgiai.ttf",
        "C:/Windows/Fonts/georgia.ttf",
        "C:/Windows/Fonts/times.ttf",
        "C:/Windows/Fonts/arial.ttf",
    ]
    for path in font_paths:
        if os.path.exists(path):
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()

def generate_certificate(name, design_file, output_path):
    img    = Image.open(design_file).convert("RGB")
    width, height = img.size
    draw   = ImageDraw.Draw(img)
    config = DESIGN_CONFIG[design_file]
    font   = get_font(config["font_size"])
    color  = config["color"]

    x = int(width  * config["x"])
    y = int(height * config["y"])

    bbox        = draw.textbbox((0, 0), name, font=font)
    text_width  = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    text_x = x - text_width  // 2
    text_y = y - text_height // 2

    draw.text((text_x, text_y), name, font=font, fill=color)

    # Date bhi print karo
    date_font = get_font(28)
    date_str  = datetime.now().strftime("%B %d, %Y")
    date_color = color
    draw.text((int(width * 0.18), int(height * 0.88)),
              date_str, font=date_font, fill=date_color)

    temp_img = output_path.replace(".pdf", "_temp.jpg")
    img.save(temp_img, "JPEG", quality=95)

    iw, ih = Image.open(temp_img).size
    pdf_w  = iw * 0.75
    pdf_h  = ih * 0.75

    c = canvas.Canvas(output_path, pagesize=(pdf_w, pdf_h))
    c.drawImage(ImageReader(temp_img), 0, 0, pdf_w, pdf_h)
    c.save()
    os.remove(temp_img)
    print(f"  Certificate ready: {output_path}")

def send_email(to_email, name, pdf_path):
    msg = MIMEMultipart("alternative")
    msg["From"]    = SENDER_EMAIL
    msg["To"]      = to_email
    msg["Subject"] = "Your Certificate - Workshop"

    html_body = f"""
    <html>
    <body style="font-family: Arial, sans-serif; background-color: #f4f4f4; padding: 30px;">
        <div style="max-width: 600px; margin: auto; background: white; border-radius: 10px; padding: 30px; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
            <h1 style="color: #2c3e50; text-align: center;">Congratulations, {name}!</h1>
            <p style="font-size: 16px; color: #555; text-align: center;">
                We are pleased to present you with your certificate of achievement.
            </p>
            <div style="background: #f9f9f9; border-left: 4px solid #3498db; padding: 15px; margin: 20px 0;">
                <p style="margin: 0; color: #333;">Please find your personalized certificate attached to this email.</p>
            </div>
            <p style="font-size: 14px; color: #888; text-align: center;">
                Thank you for participating in our workshop!
            </p>
            <hr style="border: none; border-top: 1px solid #eee;">
            <p style="font-size: 12px; color: #aaa; text-align: center;">
                This is an automated email. Please do not reply.
            </p>
        </div>
    </body>
    </html>
    """

    msg.attach(MIMEText(html_body, "html"))

    with open(pdf_path, "rb") as f:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(f.read())
        encoders.encode_base64(part)
        part.add_header(
            "Content-Disposition",
            f"attachment; filename={os.path.basename(pdf_path)}"
        )
        msg.attach(part)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(SENDER_EMAIL, APP_PASSWORD)
        server.sendmail(SENDER_EMAIL, to_email, msg.as_string())
    print(f"  Email sent to: {to_email}")

def main():
    if not os.path.exists(OUTPUT_FOLDER):
        os.makedirs(OUTPUT_FOLDER)

    participants = []
    with open(CSV_FILE, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            participants.append({
                "name":  row["Name"].strip(),
                "email": row["Email"].strip()
            })

    print(f"\n{len(participants)} participants found\n")

    for i, p in enumerate(participants):
        design     = DESIGNS[i % len(DESIGNS)]
        safe_name  = p["name"].replace(" ", "_")
        output_pdf = os.path.join(OUTPUT_FOLDER,
                                  f"{safe_name}_certificate.pdf")
        print(f"Processing: {p['name']} → {design}")
        generate_certificate(p["name"], design, output_pdf)
        send_email(p["email"], p["name"], output_pdf)
        print()

    print("Done! Saare certificates ban gaye aur emails bhi chali gayi!")

if __name__ == "__main__":
    main()