from django.shortcuts import render
import requests
import sys
from subprocess import run, PIPE

def button(request):

    return render(request, 'lets_talk.html')

def output(request):
    # data = requests.get("https://www.uppingyourelvis.com/")
    #data = requests.get("http://127.0.0.1:8000/home/yadav/Desktop/HackMed2020/THE_APP/elvis_app/html_pages/lets_talk.html")
    # print(data.text)
    # data = data.text

    out = run([sys.executable, '//home//yadav//Desktop//HackMed2020//THE_APP//microphone_recognition.py'], shell=False)

    return render(request, 'lets_talk.html', {'data4':out.stdout})

def external(request):
    # inp = request.POST.get('param')
    out = run([sys.executable, '//home//yadav//Desktop//HackMed2020//THE_APP//record.py'], shell=False)


    return render(request, 'lets_talk.html', {'data1':out.stdout}) #put data1 into out

# def external2(request):
#     inp = request.POST.get('param')
#     out = run([sys.executable, '//home//yadav//Desktop//HackMed2020//THE_APP//microphone_recognition.py', inp], shell=False, stdout=PIPE)
#     print(out)
#     button(request)
#
#     return render(request, 'lets_talk.html', {'data2':out.stdout}) #put data1 into out
