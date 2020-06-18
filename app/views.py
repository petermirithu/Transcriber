from django.shortcuts import render,redirect
import speech_recognition as sr
from pydub import AudioSegment

from django.templatetags.static import static

# Create your views here.
def home(request):
    return render(request,"index.html")
    
def converter(request):

    file_x="static/audio/newsreel.mp3" 
    sound_x = AudioSegment.from_mp3(file_x)
    sound_x.export("static/audio/newsreel.wav", format="wav")

    sound="static/audio/newsreel.wav"
                
    # file_x="static/audio/Just To Know.wav"
    # sound_x = AudioSegment.from_wav(file_x)
    # sound_x = sound_x.set_channels(1)
    # sound_x.export("static/audio/Just To Know.wav", format="wav")
    # sound="static/audio/Just To Know.wav"

    # listening to audio
    ls=sr.Recognizer()

    with sr.AudioFile(sound) as source:
        ls.adjust_for_ambient_noise(source)

        print("Converting to text...")

        # audio=ls.listen(source)

        audio = ls.record(source)  # read the entire audio file                  

        # print("Transcription: " + r.recognize_google(audio))

        try:
            print("Converted Audio is :")
            print(ls.recognize_google(audio))
        except Exception as e:
            print("Error {} : ".format(e))        

    return redirect('home')

