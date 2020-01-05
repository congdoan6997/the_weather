from django.shortcuts import render
import requests
from .models import  City

# Create your views here.
def index(request):
    url="http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=c2a293069b9a83c6a0f0c4ebf8768f76"
    weather_data =[]
    for city in City.objects.all():        
        r = requests.get(url.format(city)).json()
        weather ={
            'city': city,
            'temp': r["main"]["temp"],
            'desc': r["weather"][0]["description"],
            'icon':r["weather"][0]['icon']
        }
        weather_data.append(weather)

    return render(request,'weather/index.html',{'weather_data': weather_data})