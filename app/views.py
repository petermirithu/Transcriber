from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect
from .forms import UploadFileForm
import speech_recognition as sr
from pydub import AudioSegment
from django.contrib import messages
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import os
from datetime import datetime


# Create your views here.
def home(request):
    path ="media"    
    now=datetime.now()

    for filename in os.listdir(path):        
        t = os.path.getmtime("media/"+filename)
        dt=datetime.fromtimestamp(t)
        res=(dt-now).days            
        if res<0:
            os.remove("media/"+filename)
            print("done")                    
        
    return render(request,"index.html")

def file_upload(request):
    if request.method == 'POST' and request.FILES['myfile']:                
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)     
        final_name=uploaded_file_url[6:]

        messages.info(request, 'Successfully Uploaded you file. Scroll down and hover Transcribe button for magic.')        
        return render(request, 'index.html', {'uploaded_file_url': final_name})

    return redirect("home")

def converter(request,file_name):
    file_path="media/"+file_name
    # check file        
    str_url = str(file_path)
    exte_str=str_url[-3]+str_url[-2]+str_url[-1]

    if "%" in str_url:
        messages.info(request, "Please rename your file. I don't accept file with spaces in between!")
        return redirect("home")
    elif exte_str=="mp3":
        file_x_mp3=str_url
        sound_x_mp3 = AudioSegment.from_mp3(file_x_mp3)
        cut_name1=str_url[0:(len(str_url)-4)]
        sound_x_mp3.export(cut_name1+".wav", format="wav")

        sound_mp3=cut_name1+".wav"

        # listening to audio
        ls_mp3=sr.Recognizer()

        with sr.AudioFile(sound_mp3) as source:
            ls_mp3.adjust_for_ambient_noise(source)                      
            audio_mp3 = ls_mp3.record(source)          
            try:
                text_mp3=ls_mp3.recognize_google(audio_mp3)                                                    
            except LookupError:
                messages.info(request, 'Bad News! There was error with you file.')
                return redirect("home")                
        
        messages.info(request, 'Successfully did magic for you. Scroll down to see it!')        
        return render( request, 'index.html',{"text":text_mp3})

    elif exte_str=="wav":
        file_wav=str_url
        sound_x_wav = AudioSegment.from_wav(file_wav)
        sound_x_wav = sound_x_wav.set_channels(1)
        sound_x_wav.export(file_wav, format="wav")            
        sound_wav=str_url
        
        # listening to audio
        ls_wav=sr.Recognizer()

        with sr.AudioFile(sound_wav) as source_wav:
            ls_wav.adjust_for_ambient_noise(source_wav)
                
            audio_wav = ls_wav.record(source_wav)          
            try:                    
                text_wav=ls_wav.recognize_google(audio_wav)                    
            except LookupError:
                messages.info(request, 'Bad News! There was error with you file.')
                return redirect("home")                

        messages.info(request, 'Successfully did magic for you. Scroll down to see it!')                                    
        return render( request, 'index.html',{"text":text_wav})
        
    else:            
        messages.info(request, 'Bad News! We only accept audio files!.')
        return redirect("home")         
