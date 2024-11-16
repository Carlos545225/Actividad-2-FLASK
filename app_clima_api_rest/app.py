from flask import Flask, render_template, request
import requests

app = Flask(__name__)

API_KEY = 'cc4552b5d77473ae40bc4cc76bbc1fd9'

@app.route('/', methods=['GET', 'POST'])
def index():
    weather_data = []
    if request.method == 'POST':
        ciudad = request.form['ciudad']
        city_list = [city.strip() for city in ciudad.split(',')]
        
        for city in city_list:
            url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric&lang=es'
            response = requests.get(url)
            
            if response.status_code == 200:
                data = response.json()
                weather = {
                    'city': data['name'],
                    'temperature': data['main']['temp'],
                    'description': data['weather'][0]['description'],
                    'feels_like': data['main']['feels_like'],
                    'temp_min': data['main']['temp_min'],
                    'temp_max': data['main']['temp_max'],
                    'icon': data['weather'][0]['icon'],
                }
                weather_data.append(weather)
            else:
                weather_data.append({'city': city, 'error': 'No se pudo obtener el clima.'})
    
    return render_template('index.html', weather_data=weather_data)

if __name__ == '__main__':
    app.run(debug=True)