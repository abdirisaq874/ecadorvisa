from flask import Flask, request, render_template, send_file
import fitz  # PyMuPDF
import qrcode
import pymongo
from io import BytesIO
import shutil
from PIL import Image
import os



app = Flask(__name__)

# Configure upload folder
UPLOAD_FOLDER = 'uploads/'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# MongoDB setup
client = pymongo.MongoClient("mongodb+srv://abdirisaq874:14789632Abdi.@nodejsprojects.tldzxrx.mongodb.net/visaEcuador?")
db = client["visa_db"]
collection = db["visas"]

@app.route('/adminjdfshjsdn', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        # Handle image upload
        image = request.files['image']
        if image:
            image_filename = os.path.join(app.config['UPLOAD_FOLDER'], image.filename)
            image.save(image_filename)
        # Get form data
        data = {
            "place_of_issue": request.form.get("place_of_issue"),
            "valid_from": request.form.get("valid_from"),
            "valid_until": request.form.get("valid_until"),
            "document_no": request.form.get("document_no"),
            "fullName": request.form.get("fullName"),
            "passportNo": request.form.get("passportNo"),
            "sex": request.form.get("sex"),
            "birth_date": request.form.get("birth_date"),
            "nationality": request.form.get("nationality"),
             "image_path": image_filename,  # Store user image path in the DB
        }
        
        # Save data to MongoDB
        collection.insert_one(data)
        return "Information saved to database"
    
    return render_template('admin.html')

@app.route('/', methods=['GET'])
def verify():
    passport_no = request.args.get('passportNo')
    visa_record = collection.find_one({"passportNo": passport_no})
    
    if visa_record:
        return render_template('verify.html', visa=visa_record, passportNo=passport_no)
    else:
        return render_template('verify.html', passportNo=passport_no)

@app.route('/download_visa', methods=['POST'])
def download_visa():
    passport_no = request.form.get('passportNo')
    visa_record = collection.find_one({"passportNo": passport_no})
    
    if visa_record:
        pdf_path = generate_pdf(visa_record)
        return send_file(pdf_path, as_attachment=True, download_name="visa.pdf")
    else:
        return "Visa not found"

def generate_pdf(data):
    template_pdf_path = "tmp/visa.pdf"
    output_dir = "/Users/mandeez/Documents/Generated_PDFs/"

    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Create a unique filename for each generated PDF
    import datetime
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    output_pdf_path = os.path.join(output_dir, f"Generated_{timestamp}.pdf")

    # Copy the template PDF to a new file
    shutil.copy(template_pdf_path, output_pdf_path)

    doc = fitz.open(output_pdf_path)  # Create a new PDF# Select the page you want to edit (0-indexed)
    page_number = 0
    page = doc[page_number]
    # Path to Verdana font
    font_path = "Verdana.ttf"

    # Load the font
    font = fitz.Font(fontname="verdana", fontfile=font_path)

    # Set text properties
    font_size = 6
    text_positions = {
        "place_of_issue": (222, 218, data["place_of_issue"]),
        "valid_from": (345, 218, data["valid_from"]),
        "valid_until": (439, 218, data["valid_until"]),
        "document_no": (419, 234, data["document_no"]),
        "fullName": (222, 273, data["fullName"]),
        "passportNo": (222, 294, data["passportNo"]),
        "sex": (321, 294, data["sex"]),
        "birth_date": (371, 296, data["birth_date"]),
        "nationality": (445, 294, data["nationality"])
    }
    
    # Insert text
    for key, (x, y, text) in text_positions.items():
        page.insert_text((x, y), text, fontsize=font_size)
    
    # Insert QR Code
    qr_url = f"https://cancilleria-gycqdbhqazguambr.eastus-01.azurewebsites.net/?passportNo={data['passportNo']}"
    qr_img = generate_qr_code(qr_url)
    # Insert QR code without saving to disk
    qr_img_bytes = BytesIO()
    qr_img.save(qr_img_bytes)
    qr_img_bytes.seek(0)
    page.insert_image(fitz.Rect(281, 643, 354, 716), stream=qr_img_bytes)
    # Dynamic image path from the database
    image_path = data["image_path"]
    if image_path:
        page.insert_image(fitz.Rect(107, 229, 171, 316), filename=image_path)
    doc.saveIncr()
    doc.close()
    return output_pdf_path

def generate_qr_code(url):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill='black', back_color='white')
    return img

if __name__ == '__main__':
    app.run(debug=True)