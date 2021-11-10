from pdf2image import convert_from_bytes
from PIL import Image
from pyzbar.pyzbar import decode
import pdfplumber
import re

def cv2_pdf2img(pdf_path, sap):
    images = convert_from_bytes(pdf_path.read(), 500) 
    for i in range(len(images)):
        images[i].save(str(sap)+'.jpg', 'JPEG')
    return str(sap) + ".jpg"

def decodeQR(img_path):
    result = decode(Image.open(img_path))
    for i in range(len(result)):
        return type(result[i].data) == bytes
        
def clean_text(txt):
    txt = txt.lower()
    txt = re.sub(r'[^\w\s]','',txt)
    txt = re.sub(r'[^a-z0-9]', ' ', txt)
    txt = txt.split()
    return txt

def verify(pdf_path, sap):
    d = {}
    im_path = cv2_pdf2img(pdf_path, sap)
    vv = decodeQR(im_path)
    #print(vv)
    if not vv:
        return {"val": False, "details": "Fradulent certificate"}
        
    v = False
    with pdfplumber.open(pdf_path) as pdf:
        first_page = pdf.pages[0]
        data = first_page.extract_text().split('\n')
        #print(data)
    for i in data:
        #print(i)
        if 'final certiﬁcate for covid-19 vaccination' in i.lower().strip():
            v = True
        if 'fully vaccinated' in i.lower().strip():
            v = True
    
    if v:
        for i in data:
            txt = clean_text(i.lower().strip())
            
            if ("bene" in txt) and ("ciary" in txt) and ("name" in txt):
                d["name"] = txt[3:]
            elif ("date" in txt) and ("of" in txt) and ("2nd" in txt) and ("dose" in txt):
                d["date of last dose"] = txt[4:7]
            elif ("date" in txt) and ("of" in txt) and ("dose" in txt):
                d["date of last dose"] = txt[3:6]
            elif ("age" in txt):
                d["age"] = txt[1:]
            elif ("gender" in txt):
                d["gender"] = txt[1:]
        return {"val":True, "details" : {"data": d, "im_path": im_path}}
    
    return {"val": False, "details": "Only 1 dose done"}