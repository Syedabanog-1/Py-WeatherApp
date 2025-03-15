import streamlit as st
import requests
import json  # Import JSON module

# OpenWeatherMap API Key
API_KEY = "4565bdea59e6778f22b6db165ac65149"  # Replace with your API key

# Sample country and city data (if JSON file does not exist, create it)
country_city_data = {
    "USA": ["New York", "Los Angeles", "Chicago"],
    "UK": ["London", "Manchester", "Birmingham"],
    "India": ["Delhi", "Mumbai", "Bangalore"],
    "Pakistan": ["Lahore", "Karachi", "Islamabad"],
    "Germany": ["Berlin", "Munich", "Hamburg"]
}

# Save country and city data to a JSON file
json_filename = "countries_cities.json"
try:
    with open(json_filename, "x", encoding="utf-8") as file:
        json.dump(country_city_data, file, indent=4)
except FileExistsError:
    pass  # File already exists, do nothing

# Load country and city data from JSON file
with open(json_filename, "r", encoding="utf-8") as file:
    country_city_data = json.load(file)

def get_weather(city, country):
    if not city or not country:
        st.error("Please select both country and city.")
        return
    
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city},{country}&appid={API_KEY}&units=metric"
    
    try:
        response = requests.get(url)
        data = response.json()
        
        if response.status_code != 200:
            st.error(data.get("message", "Error retrieving weather data"))
            return
        
        weather_desc = data["weather"][0]["description"].capitalize()
        temp = data["main"]["temp"]
        
        st.success(f"**Weather:** {weather_desc}\n\n**Temperature:** {temp}°C")
    
    except Exception as e:
        st.error(f"Could not retrieve weather data: {e}")

# Streamlit UI
st.title("Weather App")

# Country selection dropdown
countries = list(country_city_data.keys())
selected_country = st.selectbox("Select Country:", countries)

# City selection dropdown (based on selected country)
cities = country_city_data.get(selected_country, [])
selected_city = st.selectbox("Select City:", cities)

if st.button("Get Weather"):
    get_weather(selected_city, selected_country)
