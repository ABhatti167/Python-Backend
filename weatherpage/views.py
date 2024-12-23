from django.shortcuts import render
import json
import urllib.request

# Create your views here.
def index(request):
    
    if request.method == 'POST':
        city = request.POST["city"]
        res = urllib.request.urlopen("https://api.openweathermap.org/data/2.5/weather?q=" + city+"&appid=aa1b776f24fab30553b63f628dee52cb").read()
        json_data = json.loads(res)
        data = {
            'country': str(json_data['sys']['country']),
            'coordinates': str(json_data['coord']['lon'])+' '+str(json_data['coord']['lat']),
            'tem': str(round((int(json_data['main']['temp'])-273.15),2)) + 'C',
            'pressure': str(json_data['main']['pressure']),
            'humidity': str(json_data['main']['humidity']),
            
        }
        
        
    else:
        city=''
        data={}
        
    return render(request, 'index.html', {'city':city, 'data':data})