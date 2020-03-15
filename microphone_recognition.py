#!/usr/bin/env python3

# NOTE: this example requires PyAudio because it uses the Microphone class

import speech_recognition as sr
from ibm_watson import ToneAnalyzerV3
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from textblob import TextBlob
import json
from os import path
import csv
from subprocess import *
import os
import statistics
import matplotlib.pyplot as plt
import soundfile as sf

dir = path.dirname(path.realpath(__file__))

# transcribe audio file
AUDIO_FILE = "test.wav"


authenticator = IAMAuthenticator('7al8kKNELNqeKlW-X6Ckpxcos-PTMINxzsgi2-N72w6M')#q67IEUb3KzvJ_Yv1tbklxJ5MsbNFV3jIsQTY1LhskRIT')#'
tone_analyzer = ToneAnalyzerV3(
    version='2016-05-19',
    authenticator=authenticator
)

tone_analyzer.set_service_url('https://api.eu-gb.tone-analyzer.watson.cloud.ibm.com/instances/823fb747-be1e-4be2-8db3-66198f6b3812')

# obtain audio from the microphone
r = sr.Recognizer()
with sr.AudioFile(AUDIO_FILE) as source:
    audio = r.record(source)  # read the entire audio file
    try:
        # Tone Analysis
        dir2 = path.join(dir,'opensmile-2.3.0/')
        command = "{0}SMILExtract -C {1}config/emobase_live4_batch.conf -I {2}/{3} > {4}/result.txt".format(dir2,dir2,dir,AUDIO_FILE,dir)
        os.system(command)

        # for testing purposes, we're just using the default API key
        # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
        # instead of `r.recognize_google(audio)`
        print("Google Speech Recognition thinks you said " + r.recognize_google(audio))
        analysis = TextBlob(r.recognize_google(audio))
        print(analysis.sentiment.polarity)

        tone_analysis = tone_analyzer.tone({'text': r.recognize_google(audio)},content_type='application/json').get_result()
        tone_analysis = (tone_analysis['document_tone']['tone_categories'][0]['tones'])
        word_anger = tone_analysis[0]['score']
        word_disgust = tone_analysis[1]['score']
        word_fear = tone_analysis[2]['score']
        word_joy = tone_analysis[3]['score']
        word_sadness = tone_analysis[4]['score']
        print('\n\nWord Analysis')
        print('anger:{}'.format(word_anger))
        print('disgust:{}'.format(word_disgust))
        print('fear:{}'.format(word_fear))
        print('joy:{}'.format(word_joy))
        print('sadness:{}'.format(word_sadness))
        word_sum = word_anger + word_disgust + word_fear + word_joy + word_sadness
        word_sum = word_sum/100
        # Pie chart, where the slices will be ordered and plotted counter-clockwise:
        labels = 'Anger', 'Disgust', 'Fear', 'Joy' , 'Sadness'
        sizes = [word_anger/word_sum, word_disgust/word_sum, word_fear/word_sum, word_joy/word_sum, word_sadness/word_sum]

        #colors
        colors = ['#ff9999','#66b3ff','#99ff99','#ffcc99','#66ffb3']

        #explsion
        explode = (0.05,0.05,0.05,0.05,0.05)

        fig1, ax1 = plt.subplots()
        # ax1.pie(sizes,colors=colors, autopct='%1.1f%%',startangle=90, pctdistance=0.85)
        patches, texts = plt.pie(sizes, colors=colors, startangle=90 , explode = explode)
        plt.legend(labels=['%s, %1.1f %%' % (l, s) for l, s in zip(labels, sizes)], loc="best")
        #draw circle
        centre_circle = plt.Circle((0,0),0.70,fc='white')
        fig = plt.gcf()
        fig.gca().add_artist(centre_circle)
        # Equal aspect ratio ensures that pie is drawn as a circle
        ax1.axis('equal')
        plt.tight_layout()
        mng = plt.get_current_fig_manager()
        mng.full_screen_toggle()
        # plt.show()


        anger = []
        boredom = []
        disgust = []
        fear = []
        happiness = []
        neutral = []
        sadness = []

        file = open('result.txt','r')
        Results = file.read()
        Results = Results.split('SMILE-RESULT::ORIGIN=libsvm::TYPE=classification::COMPONENT=emodbEmotion::')
        print('\n\nTone Analysis')
        for result in Results:
            if 'SMILE-RESULT::ORIGIN=libsvm::TYPE=regression::COMPONENT=arousal::VIDX=0' in result:
                continue
            start = result.find("PROB=0;anger:") + len("PROB=0;anger:")
            end = result.find("::PROB=1")
            anger.append(float(result[start:end]))

            start = result.find("PROB=1;boredom:") + len("PROB=1;boredom:")
            end = result.find("::PROB=2")
            boredom.append(float(result[start:end]))

            start = result.find("PROB=2;disgust:") + len("PROB=2;disgust:")
            end = result.find("::PROB=3")
            disgust.append(float(result[start:end]))

            start = result.find("PROB=3;fear:") + len("PROB=3;fear:")
            end = result.find("::PROB=4")
            fear.append(float(result[start:end]))

            start = result.find("PROB=4;happiness:") + len("PROB=4;happiness:")
            end = result.find("::PROB=5")
            happiness.append(float(result[start:end]))

            start = result.find("PROB=5;neutral:") + len("PROB=5;neutral:")
            end = result.find("::PROB=6")
            neutral.append(float(result[start:end]))

            start = result.find("PROB=6;sadness:") + len("PROB=6;sadness:")
            end = result.find("\nSMILE-RESULT::ORIGIN=libsvm::TYPE=classification::COMPONENT=abcAffect")
            sadness.append(float(result[start:end]))

        print('anger:{}'.format(anger))
        print('boredom:{}'.format(boredom))
        print('disgust:{}'.format(disgust))
        print('fear:{}'.format(fear))
        print('happiness:{}'.format(happiness))
        print('neutral:{}'.format(neutral))
        print('sadness:{}\n\n'.format(sadness))

        print('Mean Values')
        print('anger:{}'.format(statistics.mean(anger)))
        print('boredom:{}'.format(statistics.mean(boredom)))
        print('disgust:{}'.format(statistics.mean(disgust)))
        print('fear:{}'.format(statistics.mean(fear)))
        print('happiness:{}'.format(statistics.mean(happiness)))
        print('neutral:{}'.format(statistics.mean(neutral)))
        print('sadness:{}\n'.format(statistics.mean(sadness)))

        fig2, ax2 = plt.subplots()
        ax2.plot(anger ,marker='o', markerfacecolor='red', markersize=6, color='pink', linewidth=2,label='anger')
        ax2.plot(boredom ,marker='o', markerfacecolor='blue', markersize=6, color='skyblue', linewidth=2,label='boredom')
        ax2.plot(disgust ,marker='o', markerfacecolor='gold', markersize=6, color='yellow', linewidth=2,label='disgust')
        ax2.plot(fear ,marker='o', markerfacecolor='purple', markersize=6, color='palevioletred', linewidth=2,label='fear')
        ax2.plot(happiness ,marker='o', markerfacecolor='green', markersize=6, color='lightgreen', linewidth=2,label='happiness')
        ax2.plot(neutral ,marker='o', markerfacecolor='black', markersize=6, color='lightgrey', linewidth=2,label='neutral')
        ax2.plot(sadness ,marker='o', markerfacecolor='darkorange', markersize=6, color='orange', linewidth=2,label='sadness')
        plt.legend(loc="upper right")
        plt.xlabel('Time Step')
        plt.ylabel('Normalised Percentage %')
        plt.grid()
        mng = plt.get_current_fig_manager()
        mng.full_screen_toggle()
        # plt.show()
        fig1.savefig(path.join(dir,"Word_Analysis.png"))
        fig2.savefig(path.join(dir,"Tone_Analysis.png"))

        f = sf.SoundFile(AUDIO_FILE)
        # print('samples = {}'.format(len(f)))
        # print('sample rate = {}'.format(f.samplerate))
        print('seconds = {}'.format(len(f) / f.samplerate))

    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
