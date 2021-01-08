import fitz
from utility import *
from tkinter import Tk     # from tkinter import Tk for Python 3.x
from tkinter.filedialog import askopenfilename

# load config
print('Loading config...')

with open('config.yaml', encoding='utf8') as stream:
    config = loadConfig(stream)
    print(config)

wordlist = config['wordlist']
imagelist = config['imagelist']
itemcount = config['itemcount'][0]
cornerOrderTxt = config['cornertext']

# read in pdf
print('Select input file')

Tk().withdraw() # we don't want a full GUI
filename = askopenfilename()

### PROCESSING ###

doc = fitz.open(filename)
for page in doc:
    print('page ' + str(page.number))

    ## Hilighting part ##

    # more than 1 item alert
    text_instances = page.searchFor(itemcount['indicator'])
    for inst in text_instances:
        
        count = fitz.Rect(inst.x0-30,inst.y0,inst.x1+10,inst.y1)
        try :
            if int(page.getTextbox(count)[:-4]) > 1 :
                highlight = page.addHighlightAnnot(count)
                highlight.setColors({"stroke":hexToFitzColor(itemcount['color']), "fill":None})
                highlight.update()
        except ValueError as error:
            None

    # wordlist hilighting
    for word in wordlist:
        text_instances = page.searchFor(word['word'])
        for inst in text_instances:
            box = fitz.Rect(inst.x0-word['extend x'], inst.y0-word['extend y'], inst.x1+word['extend x'], inst.y1+word['extend y'])
            highlight = page.addHighlightAnnot(box)
            highlight.setColors({"stroke":hexToFitzColor(word['color']), "fill":None})
            highlight.update()

    # insert image
    text_instances = page.searchFor(cornerOrderTxt)
    for inst in text_instances:
        for image in imagelist:
            img = open(image['location'], 'rb').read()
            page.insertImage(fitz.Rect(inst.x0 + image['x'], inst.y0 + image['y'], inst.x1 + image['x'] + image['width'], inst.y1 + image['y'] + image['height']), stream = img, keep_proportion = True)

### OUTPUT ###

doc.save('output.pdf', garbage=4, deflate=True, clean=True)
doc.close()
