import os,io
from django.shortcuts import render, HttpResponse
from django.contrib.auth import authenticate
from PIL import Image
import pytesseract
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from google.cloud import vision
from google.cloud.vision import types


client = vision.ImageAnnotatorClient()


def home(request):
    return render(request, 'index.html')

def login(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        return render(request, 'upload.html')
    else:
        return HttpResponse('Login Error')

def upload(request):
    file_temp = request.FILES['note']

    # a = Image.open(file_temp)
    # text = pytesseract.image_to_string(a)
    # tokens = word_tokenize(text)
    # dict = {'text': text, 'tokens':tokens}
    extracted_keyword = []
    with io.open('/home/ejas/Pictures/a.jpg', 'rb') as image_file:
        content = image_file.read()
    image = vision.types.Image(content=content)
    response = client.text_detection(image=image)
    texts = response.text_annotations
    for text in texts:
        extracted_keyword.append(text.description)
    keywords = sent_tokenize(str(extracted_keyword[0]))

    return render(request, 'extract.html',{'response': keywords} )
    
