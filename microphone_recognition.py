#!/usr/bin/env python3

# NOTE: this example requires PyAudio because it uses the Microphone class

import speech_recognition as sr
from ibm_watson import ToneAnalyzerV3
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

# from watson_developer_cloud import ToneAnalyzerV3
from textblob import TextBlob
import json

from os import path
from pydub import AudioSegment

# AUDIO_FILE_EN = path.join(path.dirname(path.realpath(__file__)), "TIO/TIO1.mp3")
#
# sound = AudioSegment.from_mp3(AUDIO_FILE_EN)
# sound.export("transcript.wav", format="wav")

# transcribe audio file
AUDIO_FILE = "transcript.wav"


authenticator = IAMAuthenticator('7al8kKNELNqeKlW-X6Ckpxcos-PTMINxzsgi2-N72w6M')#q67IEUb3KzvJ_Yv1tbklxJ5MsbNFV3jIsQTY1LhskRIT')#'
tone_analyzer = ToneAnalyzerV3(
    version='2016-05-19',
    authenticator=authenticator
)
# tone_analyzer.set_service_url('https://f633c362-22bf-483a-9bc6-fc4fcb648f6b-bluemix.cloudantnosqldb.appdomain.cloud')

tone_analyzer.set_service_url('https://api.eu-gb.tone-analyzer.watson.cloud.ibm.com/instances/823fb747-be1e-4be2-8db3-66198f6b3812')

# obtain audio from the microphone
r = sr.Recognizer()
# with sr.AudioFile(AUDIO_FILE) as source:
#     audio = r.record(source)  # read the entire audio file
with sr.Microphone() as source:
    r.adjust_for_ambient_noise(source)  # listen for 1 second to calibrate the energy threshold for ambient noise levels
    print("Say something!")
    while(True):
        audio = r.listen(source)
        # recognize speech using Google Speech Recognition
        try:
            # for testing purposes, we're just using the default API key
            # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
            # instead of `r.recognize_google(audio)`
            print("Google Speech Recognition thinks you said " + r.recognize_google(audio))
            analysis = TextBlob(r.recognize_google(audio))
            print(analysis.sentiment.polarity)

            tone_analysis = tone_analyzer.tone({'text': r.recognize_google(audio)},content_type='application/json').get_result()
            tone_analysis = (tone_analysis['document_tone']['tone_categories'][0]['tones'])
            anger = tone_analysis[0]['score']
            disgust = tone_analysis[1]['score']
            fear = tone_analysis[2]['score']
            joy = tone_analysis[3]['score']
            sadness = tone_analysis[4]['score']
            # print(json.dumps(tone_analysis, indent=2))
            print('anger:{}'.format(anger))
            print('disgust:{}'.format(disgust))
            print('fear:{}'.format(fear))
            print('joy:{}'.format(joy))
            print('sadness:{}'.format(sadness))

        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))
