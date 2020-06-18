from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect
from .forms import UploadFileForm
import speech_recognition as sr
from pydub import AudioSegment
from django.conf import settings
from django.core.files.storage import FileSystemStorage

from django.templatetags.static import static

# Create your views here.
def home(request):
    return render(request,"index.html")

def file_upload(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        return render(request, 'index.html', {'uploaded_file_url': uploaded_file_url})
    return redirect("home")

def converter(request):

    # file_x="media/newsreel.mp3" 
    # sound_x = AudioSegment.from_mp3(file_x)
    # sound_x.export("media/newsreel.wav", format="wav")

    sound="media/newsreel.wav"
                
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

        text=ls.recognize_google(audio)

        try:
            print("Converted Audio is :")
            print(ls.recognize_google(audio))
        except Exception as e:
            print("Error {} : ".format(e))        

    return render( request, 'index.html',{"text":text})

