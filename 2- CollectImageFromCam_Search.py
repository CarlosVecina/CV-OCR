
from PIL import Image
import pytesseract
import cv2
import os
import webbrowser
import cv2
import numpy

preprocess = "None"
cam = cv2.VideoCapture(0)

cv2.namedWindow("test")

img_counter = 0

while True:
    ret, frame = cam.read()
    #frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    cv2.imshow("test", frame)
    if not ret:
        break
    k = cv2.waitKey(1)

    if k%256 == 27:
        # ESC pressed
        print("Escape hit, closing...")
        break
    elif k%256 == 32:
        # SPACE pressed
        img_name = "images/opencv_frame_{}.png".format(img_counter)
        cv2.imwrite(img_name, frame)
        frame2 = numpy.invert(frame)
        print("{} written!".format(img_name))
        img_counter += 1

        # Procesamiento de la pregunta
        pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files (x86)/Tesseract-OCR/tesseract'
        text = pytesseract.image_to_string(frame, lang="spa")
        print(text)
        questiontext = text[text.find("¿") + 1: text.find("?")].replace('\n', ' ')
        print(questiontext)

        # Procesamiento de las respuestas
        frame2 = numpy.invert(frame)
        answers = pytesseract.image_to_string(frame2, lang="spa").replace('\n', ' ')

        #answerstext = answers[answerstext.find("?")+1:]
        #answers

        # Lanzamiento de la busqueda de Google de la pregunta
        url = "https://www.google.es/search?q=" + questiontext.replace(' ', '+')
        #os.system('taskkill /im chrome.exe')
        webbrowser.open_new_tab(url)


cam.release()

cv2.destroyAllWindows()

