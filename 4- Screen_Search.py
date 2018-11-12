import pyautogui
import time
import pytesseract
from PIL import Image
import PIL.ImageOps
import webbrowser
import os
import numpy as np
#Parte II
import unidecode
from urllib.request import Request, urlopen
import tkinter
#import win32api
#import win32con
#import pywintypes
import requests
from bs4 import BeautifulSoup

metodo3 = True

pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files (x86)/Tesseract-OCR/tesseract'
while True:
    try:
        input("Press enter to continue")
    except SyntaxError:
        pass
    print("")
    # Take screenshot
    #pic = pyautogui.screenshot(region=(1950, 70, 600, 1000))
    pic = pyautogui.screenshot(region=(1350, 100, 700, 900))

    #inverted_image = PIL.ImageOps.invert(pic)

    # Save the image
    #inverted_image.save('Screenshot.png')
    pic.save('Screenshot.png')
    # time.sleep(1)

    # Procesamiento de texto

    text = pytesseract.image_to_string(Image.open('Screenshot.png'), lang="spa")
    questiontext = text[text.find("¿") + 1: text.find("?")].replace('\n', ' ')
    print(text)
    print("****")
    print(questiontext)

    url = "https://www.google.es/search?q=" + questiontext.replace(' ', '+')
    # os.system('taskkill /im chrome.exe')
    webbrowser.open_new_tab(url)

    # Procesamiento de las respuestas
    answersImage = np.invert(pic)
    answersText = pytesseract.image_to_string(answersImage, lang="spa")
    answersList = answersText[answersText.find("?") + 1:].splitlines()


    def by_size(words, size):
        return [word for word in words if len(word) > size]


    answerFinalList = by_size(answersList, 1)
    print(answerFinalList)

    # Sacar el recuento de aparicion de las respuestas en la busqueda
    url = u"https://www.google.es/search?q=" + questiontext.replace(' ', '+')
    print(url)
    url = url + "&start=0"
    print(url)
    unaccented_url = unidecode.unidecode(url)
    page = Request(unaccented_url, headers={'User-Agent': 'Mozilla/5.0'})  # Para que no detecten el spider
    webpage = urlopen(page).read()
    # find = webpage.find(answerFinalList[1].encode())
    counter = [(x, webpage.find(x.encode())) for x in answerFinalList]
    print(counter)

    # Plotear el recuento en la pantalla
    if len(counter) == 3:
        print(counter)
        #label = tkinter.Label(text=counter, font=('Times New Roman', '20'), fg='red', bg='white')
        #label.master.overrideredirect(True)
        #label.master.geometry("+1050+250")
        #label.master.lift()
        #label.master.wm_attributes("-topmost", True)
        #label.master.wm_attributes("-disabled", True)
        #label.master.wm_attributes("-transparentcolor", "white")

        #hWindow = pywintypes.HANDLE(int(label.master.frame(), 16))
        ## http://msdn.microsoft.com/en-us/library/windows/desktop/ff700543(v=vs.85).aspx
        ## The WS_EX_TRANSPARENT flag makes events (like mouse clicks) fall through the window.
        #exStyle = win32con.WS_EX_COMPOSITED | win32con.WS_EX_LAYERED | win32con.WS_EX_NOACTIVATE | win32con.WS_EX_TOPMOST | win32con.WS_EX_TRANSPARENT
        #win32api.SetWindowLong(hWindow, win32con.GWL_EXSTYLE, exStyle)

        #label.pack()
        #label.mainloop()
        ##label.update_idletasks()
        ##label.update()


        # METODO 3- DEFF entre Nº RESULTADOS DE LA BUSQUEDA + RESPUESTAS
        if metodo3 == True:
            urlAns1 = "https://www.google.es/search?q=" + questiontext.replace(' ', '+')+"+"+answerFinalList[0].replace(' ', '+')
            urlAns2 = "https://www.google.es/search?q=" + questiontext.replace(' ', '+')+"+"+answerFinalList[1].replace(' ', '+')
            urlAns3 = "https://www.google.es/search?q="+ questiontext.replace(' ', '+')+"+"+answerFinalList[2].replace(' ', '+')
            unaccented_url1 = unidecode.unidecode(urlAns1)
            unaccented_url2 = unidecode.unidecode(urlAns2)
            unaccented_url3 = unidecode.unidecode(urlAns3)
            r1 = requests.get(unaccented_url1)
            r2 = requests.get(unaccented_url2)
            r3 = requests.get(unaccented_url3)
            soup = [BeautifulSoup(r1.text).find('div', {'id': 'resultStats'}).text,BeautifulSoup(r2.text).find('div', {'id': 'resultStats'}).text,BeautifulSoup(r3.text).find('div', {'id': 'resultStats'}).text]
            print(soup)

