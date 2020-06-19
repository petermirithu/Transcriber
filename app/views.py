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
import requests,json
from django.conf import settings



# Create your views here.
def home(request):
    return render(request,"index.html",{"form":UploadFileForm()})

def file_upload(request):
    if request.method=='POST':        
        file_x=request.FILES['myfile']     
        cloudinary.api.delete_resources([gma()])                                    
        file_name=gma()                
        cloudinary.uploader.upload(file_x,resource_type="video",public_id="transcribe_x/"+file_name)        
        messages.info(request, 'Successfully Uploaded you file. Scroll down and hover Transcribe button for magic.')                
        return render(request,'index.html',{"uploaded_file_url":"yes"})                     

    return redirect("home")

def converter(request):           
    result = cloudinary.Search().expression('resource_type:video').sort_by('public_id','desc').execute()    
    file_list=[]
    for x in result["resources"]:        
        if x["filename"]==gma():
            file_list.append(x["url"])                     
                    
    # check file                
    exte_str=file_list[0][-3]+file_list[0][-2]+file_list[0][-1]
    
    if exte_str=="mp3":        
        url_file=file_list[0]        
        path_file="./speech.mp3"    

        response = requests.get(url_file)     # get the response of the url
        with open(path_file, 'wb') as file:   # create the file
            file.write(response.content) # write response contents to the file

        str_url = str(path_file)

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
            except Exception:
                messages.info(request,"Could Not Read You File!")
                return redirect("home")                
        
        messages.info(request, 'Successfully did magic for you. Scroll down to see it!')        
        return render(request,'index.html',{"text":text_mp3})           

    elif exte_str=="wav":
        url_file_x=file_list[0]        
        path_file_x="./speech.wav"    

        response = requests.get(url_file_x)     # get the response of the url
        with open(path_file_x, 'wb') as file:   # create the file
            file.write(response.content) # write response contents to the file

        str_url_x = str(path_file_x)

        file_wav=str_url_x
        sound_x_wav = AudioSegment.from_wav(file_wav)
        sound_x_wav = sound_x_wav.set_channels(1)
        sound_x_wav.export(file_wav, format="wav")            
        sound_wav=str_url_x
        
        # listening to audio
        ls_wav=sr.Recognizer()

        with sr.AudioFile(sound_wav) as source_wav:
            ls_wav.adjust_for_ambient_noise(source_wav)
                
            audio_wav = ls_wav.record(source_wav)          
            try:                    
                text_wav=ls_wav.recognize_google(audio_wav)                    
            except Exception:
                messages.info(request,"Could Not Read You File!")
                return redirect("home")                

        messages.info(request, 'Successfully did magic for you. Scroll down to see it!')                                    
        return render(request,'index.html',{"text":text_wav})                   
        
    else:            
        messages.info(request, 'Bad News! We only accept audio files!.')
        return redirect("home")         
