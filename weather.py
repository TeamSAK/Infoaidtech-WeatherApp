import requests
import json
import tkinter as tk
from tkinter import messagebox

API_KEY = "bd5e378503939ddaee76f12ad7a97608"
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"
FORECAST_URL = "http://api.openweathermap.org/data/2.5/forecast"

favorite_locations = {}

class WeatherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Weather App")

        self.location_label = tk.Label(root, text="Enter location:")
        self.location_label.pack(pady=20)

        self.location_entry = tk.Entry(root,width=50)
        self.location_entry.pack()

        self.fetch_button = tk.Button(root, text="Fetch Weather", command=self.fetch_weather)
        self.fetch_button.pack(pady=10)

        self.forecast_button = tk.Button(root, text="Fetch Forecast", command=self.fetch_forecast)
        self.forecast_button.pack(pady=10)

        self.favorites_button = tk.Button(root, text="View Favorites", command=self.view_favorites)
        self.favorites_button.pack(pady=10)

        self.exit_button = tk.Button(root, text="Exit", command=root.quit)
        self.exit_button.pack(pady=10)

        self.weather_text = tk.Text(root, height=20, width=60)
        self.weather_text.pack()

    def fetch_weather(self):
        location = self.location_entry.get()
        weather_data = self.fetch_weather_data(location)
        if weather_data:
            self.display_weather(weather_data)
            self.add_to_favorites(location)
        else:
            messagebox.showerror("Error", "Location not found.")

    def fetch_weather_data(self, location):
        params = {
            "q": location,
            "appid": API_KEY,
            "units": "metric"
        }
        response = requests.get(BASE_URL, params=params)
        data = response.json()
        if response.status_code == 200:
            return data
        return None

    def display_weather(self, weather_data):
        weather_info = f"Weather in {weather_data['name']}:\n"
        weather_info += f"Temperature: {weather_data['main']['temp']}°C\n"
        weather_info += f"Description: {weather_data['weather'][0]['description']}\n"
        weather_info += f"Humidity: {weather_data['main']['humidity']}%\n"
        weather_info += f"Wind Speed: {weather_data['wind']['speed']} m/s\n"

        self.weather_text.delete("1.0", tk.END)
        self.weather_text.insert(tk.END, weather_info)

    def fetch_forecast(self):
        location = self.location_entry.get()
        forecast_data = self.fetch_forecast_data(location)
        if forecast_data:
            self.display_forecast(forecast_data)
        else:
            messagebox.showerror("Error", "Location not found.")

    def fetch_forecast_data(self, location):
        params = {
            "q": location,
            "appid": API_KEY,
            "units": "metric"
        }
        response = requests.get(FORECAST_URL, params=params)
        data = response.json()
        if response.status_code == 200:
            return data
        return None

    def display_forecast(self, forecast_data):
        forecast_info = "Weather Forecast:\n"
        for forecast in forecast_data['list']:
            date = forecast['dt_txt']
            temp = forecast['main']['temp']
            description = forecast['weather'][0]['description']
            forecast_info += f"{date}: {temp}°C - {description}\n"

        self.weather_text.delete("1.0", tk.END)
        self.weather_text.insert(tk.END, forecast_info)

    def view_favorites(self):
        if favorite_locations:
            favorites_info = "Favorite Locations:\n"
            for fav_location in favorite_locations.keys():
                favorites_info += fav_location + "\n"
            self.weather_text.delete("1.0", tk.END)
            self.weather_text.insert(tk.END, favorites_info)
        else:
            messagebox.showinfo("Info", "No favorite locations yet.")

    def add_to_favorites(self, location):
        favorite_locations[location] = True
        messagebox.showinfo("Success", f"{location} added to favorites.")

def main():
    root = tk.Tk()
    app = WeatherApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
