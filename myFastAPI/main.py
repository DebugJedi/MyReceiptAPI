from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
import pytesseract as pyract
import easyocr
from PIL import Image
import io
from fastapi.responses import JSONResponse
from myFastAPI.google_sheets import write_to_google_sheets
import re
import os
import shutil
tess_path = shutil.which("tesseract")
print(f"✅ TESSERACT CMD SET TO: {tess_path}")
print(f"✅ Exists: {os.path.exists(tess_path) if tess_path else 'Not found'}")

pyract.pytesseract.tesseract_cmd = tess_path if tess_path else "/usr/bin/tesseract"


app = FastAPI()

class ReceiptData(BaseModel):
    store_name: str
    store_location: str
    date: str
    time: str
    products: list


def parse_receipt_text(text: str):
    lines = text.splitlines()
    data = {
        "store_name": None,
        "store_location": None,
        "date": None,
        "time": None,
        "products": []
    }

    for i in range(min(5, len(lines))):
        if lines[i].strip():
            data["store_name"] = lines[i].strip()
            break

    address_keywords = ["Street", "St", "Road", "Rd", "Avenue", "Ave", "Blvd", "Drive", "Dr", "Plaza", "Mall", "Center", "Square"]
    for i in range(min(10), len(lines)):
        line = lines[i]
        if any(keyword in line for keyword in address_keywords) or re.search(r"\d{5}(-\d{4})?", line):
            data["store_location"] = line.strip()
            break

    date_pattern = r"(\d{1,2}[\/\-\.]\d{1,2}[\/\-\.]\d{2,4})"
    time_pattern = r"(\d{1,2}:\d{2}(?::\d{2})?\s*(AM|PM|am|pm)?)"

    full_text = " ".join(lines)

    date_match = re.search(date_pattern, full_text)
    time_match = re.search(time_pattern, full_text)

    data["date"] = date_match.group(1) if date_match else None
    data["time"] = time_match.group(1) if time_match else None

    product_pattern = r"([a-zA-Z0-9\s\-\&]+)\s+(\d+)?\s*[\$₹€]?\s*(\d+\.\d{2})"

    for line in lines:
        match = re.search(product_pattern, line)
        if match:
            name = match.group(1).strip()
            qty = int(match.group(2)) if match.group(2) else 1
            price = float(match.group(3))
            data["products"].append({
                "name": name,
                "quantity": qty,
                "price": price
            })
    return data



@app.post("/extract_receipt/")
async def extract_receipt(file: UploadFile = File(...)):


    try:

        image_bytes = await file.read()
        image = Image.open(io.BytesIO(image_bytes))
        print(f"Received file: {file.filename}")
        # OCR with pyttesseract

        reader = easyocr.Reader(['en'])
        # text = pyract.image_to_string(image)
        text = reader.readtext(image)

        # Simple text parsing
        extracted_data = parse_receipt_text(text)

        result = write_to_google_sheets(extracted_data)
        return JSONResponse(content={"message": "Data written to Google Sheets successfully.", "result": result})
    
    except Exception as e:
        return JSONResponse(content={"message": f"Error: {e}"}, status_code=400)