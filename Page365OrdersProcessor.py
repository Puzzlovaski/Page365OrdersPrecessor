import fitz
import yaml
from tkinter import Tk     # from tkinter import Tk for Python 3.x
from tkinter.filedialog import askopenfilename

# load config
print("Loading config...")

with open("config.yaml", encoding="utf8") as stream:
    config = yaml.safe_load(stream)

wordlist = config["wordlist"]
imagelist =config["imagelist"]
tooMuchItemTxt = "สินค้าเกินจำนวนที่สามารถแสดงบนหน้า\nโปรดใช้งานบนเว็บไซต"
unitTxt = "ชิ้น"
cornerOrderTxt = "*กรณีจัดส่งสินค้าไม่สำเร็จ"

# read in pdf
print("Select input file")

Tk().withdraw() # we don't want a full GUI
filename = askopenfilename()

### PROCESSING ###

doc = fitz.open(filename)
for page in doc:
    print("page " + str(page.number))

    ## Hilighting part ##

    # Too much item alert
    text_instances = page.searchFor(tooMuchItemTxt)
    for inst in text_instances:
        
        highlight = page.addHighlightAnnot(fitz.Rect(inst.x0-20,inst.y0-5,inst.x1+20,inst.y1))

    # more than 1 item alert
    text_instances = page.searchFor(unitTxt)
    for inst in text_instances:
        
        count = fitz.Rect(inst.x0-30,inst.y0,inst.x1+10,inst.y1)
        try :
            if int(page.getTextbox(count)[:-4]) > 1 :
                highlight = page.addHighlightAnnot(count)
        except ValueError as error:
            None

    # wordlist hilighting
    for text in wordlist:
        text_instances = page.searchFor(text)
        for inst in text_instances:
            highlight = page.addHighlightAnnot(fitz.Rect(inst.x0,inst.y0,inst.x1,inst.y1))

    # insert image
    text_instances = page.searchFor(cornerOrderTxt)
    for inst in text_instances:
        for image in imagelist:
            img = open(image["location"], "rb").read()
            page.insertImage(fitz.Rect(inst.x0 + image["x"], inst.y0 + image["y"], inst.x1 + image["x"] + image["width"], inst.y1 + image["y"] + image["height"]), stream = img, keep_proportion = True)

### OUTPUT ###

doc.save("output.pdf", garbage=4, deflate=True, clean=True)
doc.close()
