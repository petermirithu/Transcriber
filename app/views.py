from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect
from .forms import UploadFileForm
import speech_recognition as sr
from pydub import AudioSegment
from django.contrib import messages
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import os
import cloudinary
from getmac import get_mac_address as gma
from app.models import audio_files
import requests
from django.conf import settings



# Create your views here.
def home(request):
    user_uploads=audio_files.get_user_uploads(gma())
    if user_uploads:
        for fl in user_uploads:
            cloudinary.api.delete_resources([fl.file_au])

    return render(request,"index.html",{"form":UploadFileForm()})

def file_upload(request):
    if request.method=='POST':
        form=UploadFileForm(request.POST)
        if form.is_valid():
            form_x=form.save(commit=False)
            form_x.user_mac=gma()
            form_x.save()          
            print("*************************")              
            print("good")            
            print("*************************")              
            messages.info(request, 'Successfully Uploaded you file. Scroll down and hover Transcribe button for magic.')        
            return redirect('home',uploaded_file_url="yes" )             

        else:
            print("*************************")              
            print("not audio file")            
            print("*************************")              
            return redirect("home")

    print("*************************")              
    print("bad")            
    print("*************************")              
    return redirect("home")

def converter(request):
    # file_path="media/"+file_name
    url_file="https://res.cloudinary.com/pyra-z/video/upload/v1592577254/newsreel_enmxls.mp3"
    path_file="./speech.mp3"

    response = requests.get(url_file)     # get the response of the url
    with open(path_file, 'wb') as file:   # create the file
        file.write(response.content) # write response contents to the fil

    # user_uploads=audio_files.get_user_uploads(gma())
    # cloudinary.api.delete_resources(["image1", "image2"])
    # check file          
      
    str_url = str(path_file)
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

        client_id=settings.CLIENT_ID
        client_key=settings.CLIENT_KEY

        with sr.AudioFile(sound_mp3) as source:
            ls_mp3.adjust_for_ambient_noise(source)                      
            audio_mp3 = ls_mp3.record(source)          
            try:
                text_mp3=ls_mp3.recognize_houndify((audio_mp3),client_id,client_key)                                                    
            except Exception as e:
                messages.info(request, e)
                return redirect("home")                
        
        messages.info(request, 'Successfully did magic for you. Scroll down to see it!')        
        return render(request,'index.html',{"text":text_mp3})           

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
            except Exception as e:
                messages.info(request, e)
                return redirect("home")                

        messages.info(request, 'Successfully did magic for you. Scroll down to see it!')                                    
        return redirect('home',text=text_wav )             
        
    else:            
        messages.info(request, 'Bad News! We only accept audio files!.')
        return redirect("home")         
