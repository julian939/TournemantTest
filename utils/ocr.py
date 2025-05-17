import easyocr
import cv2

class OCR:
    def __init__(self):
        ...

    def get_results(self):
        image = cv2.imread('images/image.png')
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        reader = easyocr.Reader(['en', 'de'])
        result = reader.readtext(gray_image)

        collection = []
        pointscollection = []
        for (bbox, text, prob) in result:

            not_wanted = ["standing", "ist", "1st", "2nd", "3rd", "4th", "5th", "6th", "7th", "8th", "9th", "1oth", "10th", "11th", "12th"]

            if(not text.lower() in not_wanted and str(text).find("+") != 0):
                if(str(text).isdigit()):
                    pointscollection.append(text)
                else:
                    collection.append(text.lower())

        return collection, pointscollection