import requests
import datetime

#Kneepads2 - Dylan - 11/19/2023

print("\nWeather App\n===========================\n")

#get city name from user
city_name = input("Enter city name: ")

#getting coordinates of the city using a geocoding api
geocode_url = f'https://api.api-ninjas.com/v1/geocoding?city={city_name}'
headers = {'X-Api-Key': 'API_KEY'} #get an api key from api ninjas, just make an account

#make request
geocode_response = requests.get(geocode_url, headers=headers)

#check if the request was successful
if geocode_response.status_code == requests.codes.ok:
    city_data = geocode_response.json()
    
    if city_data:  #ensure there's at least one result
        first_city = city_data[0]  #get only the first result
        latitude = first_city['latitude']
        longitude = first_city['longitude']
    else:
        print("\nCannot find the city you specified.")
        exit(1)
else:
    print("Error:", geocode_response.status_code, geocode_response.text)
    exit(1)

#weather API URL
weather_url = f'https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current=temperature_2m,is_day,weather_code&hourly=temperature_2m,apparent_temperature,precipitation_probability,weather_code,wind_speed_10m&daily=weather_code,temperature_2m_max,temperature_2m_min&timezone=America%2FNew_York'
weather_response = requests.get(weather_url)

#check if the request was successful
if weather_response.status_code == requests.codes.ok:
    weather_data = weather_response.json()
else:
    print("Error fetching weather data:", weather_response.status_code, weather_response.text)
    exit(1)

temperature = weather_data['hourly']['temperature_2m'] #get the hourly temperature over the course of the week
max_temp = weather_data['daily']['temperature_2m_max'] #get the max temp of today
min_temp = weather_data['daily']['temperature_2m_min'] #get the min temp of today
feels = weather_data['hourly']['apparent_temperature'] #get the week's apparent temperature
wind_speed = weather_data['hourly']['wind_speed_10m'] #get the week's wind speed

now = datetime.datetime.now()
current_date = now.strftime('%Y-%m-%d') #this whole chunk is to get the current hour, current time so that I can use it later
current_hour = now.strftime('%H')
current_time = f"{current_date}T{current_hour}:00" 

daily_temps = [[] for _ in range(7)]
hour_of_day = ["12 AM", "1 AM", "2 AM", "3 AM", "4 AM", "5 AM", "6 AM", "7 AM", "8 AM", "9 AM", "10 AM", "11 AM",
               "12 PM", "1 PM", "2 PM", "3 PM", "4 PM", "5 PM", "6 PM", "7 PM", "8 PM", "9 PM", "10 PM", "11 PM"]
hours = weather_data['hourly']['time']

for i, hour in enumerate(hours):
    day_index = i // 24
    hour_index = i % 24
    if hour == current_time:
        current_hour_temp = f"{temperature[i]}"
    daily_temps[day_index].append({
        'hours': hour_of_day[hour_index], 
        'temperature': temperature[i],
        'feels_like': feels[i],
        'wind_speed': wind_speed[i]
    })

#display the weather data for today
first_day_data = daily_temps[0]
min_temperature = min(hour_data['temperature'] for hour_data in first_day_data)
max_temperature = max(hour_data['temperature'] for hour_data in first_day_data)

print(f"\nTemperature in {city_name}:\n")
print(f"Current Temperature: {current_hour_temp}°C | Min: {min_temperature}°C | Max: {max_temperature}°C\n")
for hour_data in first_day_data:
    print(f"{hour_data['hours']} ~ Temperature: {hour_data['temperature']}°C ~ Feels Like: {hour_data['feels_like']}°C ~ Wind Speed: {hour_data['wind_speed']} km/h")

print("\n(If you're finding it difficult to find what the temperature is of a specific hour, try highlighting the row!)\n")
