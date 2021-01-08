import yaml

def hexToFitzColor(hexstr):
    return (int(hexstr[1:3], 16)/255, int(hexstr[3:5], 16)/255, int(hexstr[5:7], 16)/255)

def loadConfig(filename):
    config = yaml.safe_load(filename)
    for word in config['itemcount']:
        if not 'color' in word:
            word['color'] = '#ffff00'
        if not 'extend x' in word:
            word['extend x'] = 0
        if not 'extend y' in word:
            word['extend y'] = 0
    for word in config['wordlist']:
        if not 'color' in word:
            word['color'] = '#ffff00'
        if not 'extend x' in word:
            word['extend x'] = 0
        if not 'extend y' in word:
            word['extend y'] = 0
    for word in config['imagelist']:
        if not 'x' in word:
            word['x'] = 0
        if not 'y' in word:
            word['y'] = 0
        if not 'width' in word:
            word['width'] = 100
        if not 'height' in word:
            word['height'] = 0
    
    return config