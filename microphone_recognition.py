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
import random
from shutil import copyfile

dir = path.dirname(path.realpath(__file__))

# transcribe audio file
AUDIO_FILE = "{0}/test.wav".format(dir)


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
        command = "{0}SMILExtract -C {1}config/emobase_live4_batch.conf -I {2} > {3}/result.txt".format(dir2,dir2,AUDIO_FILE,dir)
        # print(command)
        os.system(command)

        # for testing purposes, we're just using the default API key
        # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
        # instead of `r.recognize_google(audio)`
        Speech2Text = r.recognize_google(audio)
        print("Google Speech Recognition thinks you said " + Speech2Text )
        analysis = TextBlob(Speech2Text)
        print(analysis.sentiment.polarity)

        tone_analysis = tone_analyzer.tone({'text': Speech2Text},content_type='application/json').get_result()
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
        fig1.suptitle('Word Analysis', fontsize=20)
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
        if Results is not "":
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

            anger_mean = statistics.mean(anger)
            boredom_mean = statistics.mean(boredom)
            disgust_mean = statistics.mean(disgust)
            fear_mean = statistics.mean(fear)
            happiness_mean = statistics.mean(happiness)
            neutral_mean = statistics.mean(neutral)
            sadness_mean = statistics.mean(sadness)

            tone_sum= (anger_mean + boredom_mean + disgust_mean + fear_mean + happiness_mean+ neutral_mean + sadness_mean)
            print('Mean Values')
            print('anger:{}'.format(anger_mean/tone_sum))
            print('boredom:{}'.format(boredom_mean/tone_sum))
            print('disgust:{}'.format(disgust_mean/tone_sum))
            print('fear:{}'.format(fear_mean/tone_sum))
            print('happiness:{}'.format(happiness_mean/tone_sum))
            print('neutral:{}'.format(neutral_mean/tone_sum))
            print('sadness:{}\n'.format(sadness_mean/tone_sum))

            tone_analysis = {anger_mean:"anger", boredom_mean:"boredom",
             disgust_mean:"disgust", fear_mean:"fear", happiness_mean:"happiness",
             neutral_mean:"neutral", sadness_mean:"sadness"}

            word_analysis = {word_anger:"anger", word_disgust:"disgust", word_fear:"fear",
             word_joy:"joy", word_sadness:"sadness"}

            dict_names = {
            'anger'     : {'anger':'anger',     'disgust':'anger',   'fear':'fear',   'joy':'happy',    'sadness':'anger'},
            'boredom'   : {'anger':'anger',     'disgust':'boredom', 'fear':'fear',   'joy':'happy',    'sadness':'sadness'},
            'disgust'   : {'anger':'anger',     'disgust':'anger',   'fear':'fear',   'joy':'happy',    'sadness':'sadness'},
            'fear'      : {'anger':'anger',     'disgust':'fear',    'fear':'fear',   'joy':'happy',    'sadness':'sadness'},
            'joy'       : {'anger':'happy',     'disgust':'happy',    'fear':'fear',  'joy':'happy',    'sadness':'sadness'},
            'neutral'   : {'anger':'anger',     'disgust':'anger',   'fear':'fear',   'joy':'happy',    'sadness':'sadness'},
            'sadness'   : {'anger':'anger',     'disgust':'sadness', 'fear':'fear',   'joy':'happy',    'sadness':'sadness'}}

            meme_choice = dict_names[tone_analysis.get(max(tone_analysis))][word_analysis.get(max(word_analysis))]
            meme = (dir + "/memes/"+ meme_choice+'{0}.jpg'.format(random.randint(1, 3)))
            copyfile(meme, dir + '/elvis_app/assets/meme.jpg')


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
            fig2.suptitle('Tone Analysis', fontsize=20)

            fig1.savefig(path.join(dir,"elvis_app/assets/Word_Analysis.png"))
            fig2.savefig(path.join(dir,"elvis_app/assets/Tone_Analysis.png"))

        # plt.show()
        f = sf.SoundFile(AUDIO_FILE)
        # print('samples = {}'.format(len(f)))
        # print('sample rate = {}'.format(f.samplerate))
        print('seconds = {}'.format(len(f) / f.samplerate))
        print('Number of words = {}'.format(len(Speech2Text.split())))

    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
