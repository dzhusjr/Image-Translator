import cv2
from pytesseract import *
from pytesseract import Output
from collections import Counter
from googletrans import Translator
from PIL import Image

translator = Translator()
img_path = r'image_translator\1.png'
img = cv2.imread(img_path)
im = Image.open(img_path)
# pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

img_data = image_to_data(img, output_type=Output.DICT)

def most_frequent_colour(img):
    width, height = img.size
    rgb_total = []
    for x in range(width):
        for y in range(height):
            r, g, b = img.getpixel((x,y))
            rgb_total.append((r,g,b))
    return Counter(rgb_total).most_common(1)

def main():
    for i in range(len(img_data['level'])):
        (x, y, w, h) = (img_data['left'][i], img_data['top'][i], img_data['width'][i], img_data['height'][i])
        if img_data['text'][i]:
            cropped_im = im.crop((x, y, x+w, y+w))
            cv2.rectangle(img, (x, y), (x + w, y + h), most_frequent_colour(cropped_im.convert('RGB'))[0][0], -2)
            cv2.putText(img, translator.translate(img_data['text'][i], src = 'en', dest='uk').text, (x,y+h), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)
    
    cv2.imshow('img', img)
    cv2.waitKey(0)
if __name__ == '__main__':
    print('Processing...')
    main()