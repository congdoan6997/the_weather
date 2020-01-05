from django.shortcuts import render,redirect
import requests
from .models import  City
from .forms import  CityForm

# Create your views here.
def index(request):
    url="http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=c2a293069b9a83c6a0f0c4ebf8768f76"
    err_msg = ''
    msg=''
    class_msg=''
    if request.method == 'POST':
        formss = CityForm(request.POST)
        if formss.is_valid():
            newcity = formss.cleaned_data['name']
            exitcity = City.objects.filter(name= newcity).count()
            if exitcity == 0:
                rr = requests.get(url.format(newcity)).json()
                if rr['cod'] == 200:
                    formss.save()
                else:
                    err_msg = "This city is found!"
            else:
                err_msg = "This city is exist!"
        if err_msg != '':
            msg = err_msg
            class_msg='is-danger'
        else:
            msg='City added successfully'
            class_msg='is-success'
    form = CityForm()
    weather_data =[]
    for city in City.objects.all():        
        r = requests.get(url.format(city)).json()
        weather ={
            'city': city,
            'temp': r['main']['temp'],
            'desc': r['weather'][0]['description'],
            'icon':r['weather'][0]['icon']
        }
        weather_data.append(weather)

    return render(request,'weather/index.html',{'weather_data': weather_data,'form': form, 'msg' : msg,'class_msg': class_msg})

def delete_city(request,city_name):
    City.objects.get(name=city_name).delete()
    return redirect('index')
