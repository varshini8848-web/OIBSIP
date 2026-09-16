import tkinter as tk
from tkinter import messagebox
import requests
from datetime import datetime


# ---------------- WEATHER FUNCTIONS ---------------- #

def get_weather_icon(code):

    if code == 0:
        return "☀️"
    elif code in [1, 2, 3]:
        return "⛅"
    elif code in [45, 48]:
        return "🌫️"
    elif code in [51, 53, 55, 56, 57]:
        return "🌦️"
    elif code in [61, 63, 65, 66, 67]:
        return "🌧️"
    elif code in [71, 73, 75, 77]:
        return "❄️"
    elif code in [80, 81, 82]:
        return "🌦️"
    elif code in [95, 96, 99]:
        return "⛈️"
    else:
        return "🌤️"


def get_weather_condition(code):

    if code == 0:
        return "Clear Sky"
    elif code in [1, 2, 3]:
        return "Partly Cloudy"
    elif code in [45, 48]:
        return "Foggy"
    elif code in [51, 53, 55, 56, 57]:
        return "Drizzle"
    elif code in [61, 63, 65, 66, 67]:
        return "Rainy"
    elif code in [71, 73, 75, 77]:
        return "Snowy"
    elif code in [80, 81, 82]:
        return "Rain Showers"
    elif code in [95, 96, 99]:
        return "Thunderstorm"
    else:
        return "Unknown"


# ---------------- PLACEHOLDER FUNCTIONS ---------------- #

def remove_placeholder(event):

    if city_entry.get() == "Enter city name...":
        city_entry.delete(0, tk.END)
        city_entry.config(fg="white")


def add_placeholder(event):

    if city_entry.get() == "":
        city_entry.insert(0, "Enter city name...")
        city_entry.config(fg="#C8C2E8")


# ---------------- SEARCH WEATHER ---------------- #

def search_weather(event=None):

    city = city_entry.get().strip()

    # Don't search the placeholder text
    if city == "" or city == "Enter city name...":

        messagebox.showwarning(
            "Warning",
            "Please enter a city name"
        )

        return

    try:

        search_button.config(
            text="Searching...",
            state="disabled"
        )

        root.update()

        # ---------------- FIND CITY ---------------- #

        location_url = (
            "https://geocoding-api.open-meteo.com/v1/search"
        )

        location_params = {
            "name": city,
            "count": 10,
            "language": "en",
            "format": "json",
            "countryCode": "IN"
        }

        location_response = requests.get(
            location_url,
            params=location_params,
            timeout=10
        )

        location_data = location_response.json()

        if "results" not in location_data:

            messagebox.showerror(
                "City Not Found",
                "Please enter a valid Indian city."
            )

            return

        place = location_data["results"][0]

        latitude = place["latitude"]
        longitude = place["longitude"]

        city_name = place.get("name", city)
        state_name = place.get("admin1", "India")

        # ---------------- WEATHER API ---------------- #

        weather_url = (
            "https://api.open-meteo.com/v1/forecast"
        )

        weather_params = {

            "latitude": latitude,
            "longitude": longitude,

            "current": (
                "temperature_2m,"
                "relative_humidity_2m,"
                "wind_speed_10m,"
                "weather_code"
            ),

            "daily": (
                "weather_code,"
                "temperature_2m_max,"
                "temperature_2m_min"
            ),

            "timezone": "auto",
            "forecast_days": 7
        }

        weather_response = requests.get(
            weather_url,
            params=weather_params,
            timeout=10
        )

        weather_data = weather_response.json()

        # ---------------- CURRENT WEATHER ---------------- #

        current = weather_data["current"]

        temperature = current["temperature_2m"]
        humidity = current["relative_humidity_2m"]
        wind_speed = current["wind_speed_10m"]
        weather_code = current["weather_code"]

        condition = get_weather_condition(weather_code)
        icon = get_weather_icon(weather_code)

        # ---------------- DISPLAY CURRENT WEATHER ---------------- #

        city_title.config(
            text=city_name
        )

        state_title.config(
            text=state_name
        )

        weather_icon.config(
            text=icon
        )

        temperature_label.config(
            text=f"{round(temperature)}°C"
        )

        condition_label.config(
            text=condition
        )

        humidity_value.config(
            text=f"{humidity}%"
        )

        wind_value.config(
            text=f"{round(wind_speed)} km/h"
        )

        # ---------------- 7 DAY FORECAST ---------------- #

        daily = weather_data["daily"]

        for i in range(7):

            date = daily["time"][i]

            date_object = datetime.strptime(
                date,
                "%Y-%m-%d"
            )

            day_name = date_object.strftime("%a")

            max_temp = daily["temperature_2m_max"][i]
            min_temp = daily["temperature_2m_min"][i]

            code = daily["weather_code"][i]

            forecast_icon = get_weather_icon(code)

            forecast_day_labels[i].config(
                text=day_name
            )

            forecast_icons[i].config(
                text=forecast_icon
            )

            forecast_temp_labels[i].config(
                text=f"{round(max_temp)}°"
            )

            forecast_min_labels[i].config(
                text=f"{round(min_temp)}°"
            )

    except requests.RequestException:

        messagebox.showerror(
            "Connection Error",
            "Please check your internet connection."
        )

    except Exception as error:

        messagebox.showerror(
            "Error",
            f"Something went wrong:\n{error}"
        )

    finally:

        search_button.config(
            text="Search",
            state="normal"
        )


# ======================================================
# MAIN WINDOW
# ======================================================

root = tk.Tk()

root.title("Weather India")

root.geometry("900x700")

root.minsize(800, 600)

root.configure(
    bg="#241B5A"
)


# ======================================================
# SCROLLABLE AREA
# ======================================================

canvas = tk.Canvas(
    root,
    bg="#241B5A",
    highlightthickness=0
)

scrollbar = tk.Scrollbar(
    root,
    orient="vertical",
    command=canvas.yview
)

canvas.configure(
    yscrollcommand=scrollbar.set
)

scrollbar.pack(
    side="right",
    fill="y"
)

canvas.pack(
    side="left",
    fill="both",
    expand=True
)


# This frame will contain our entire application
main_frame = tk.Frame(
    canvas,
    bg="#241B5A"
)

canvas_window = canvas.create_window(
    (0, 0),
    window=main_frame,
    anchor="nw"
)


# Make scroll area update automatically
def update_scroll_region(event):

    canvas.configure(
        scrollregion=canvas.bbox("all")
    )


main_frame.bind(
    "<Configure>",
    update_scroll_region
)


# Make inner frame same width as canvas
def resize_frame(event):

    canvas.itemconfig(
        canvas_window,
        width=event.width
    )


canvas.bind(
    "<Configure>",
    resize_frame
)


# Mouse wheel scrolling
def mouse_scroll(event):

    canvas.yview_scroll(
        int(-1 * (event.delta / 120)),
        "units"
    )


canvas.bind_all(
    "<MouseWheel>",
    mouse_scroll
)


# ======================================================
# HEADER
# ======================================================

header_frame = tk.Frame(
    main_frame,
    bg="#241B5A"
)

header_frame.pack(
    fill="x",
    padx=35,
    pady=(25, 10)
)


logo_label = tk.Label(
    header_frame,
    text="🌤️",
    font=("Arial", 28),
    bg="#241B5A",
    fg="white"
)

logo_label.pack(
    side="left"
)


title_label = tk.Label(
    header_frame,
    text="Weather ",
    font=("Arial", 24, "bold"),
    bg="#241B5A",
    fg="white"
)

title_label.pack(
    side="left"
)


india_label = tk.Label(
    header_frame,
    text="India",
    font=("Arial", 24, "bold"),
    bg="#241B5A",
    fg="#FFD447"
)

india_label.pack(
    side="left"
)


# ======================================================
# SEARCH BAR
# ======================================================

search_frame = tk.Frame(
    main_frame,
    bg="#241B5A"
)

search_frame.pack(
    fill="x",
    padx=35,
    pady=15
)


city_entry = tk.Entry(
    search_frame,
    font=("Arial", 15),
    bg="#4938A5",
    fg="#C8C2E8",
    insertbackground="white",
    relief="flat"
)

city_entry.pack(
    side="left",
    fill="x",
    expand=True,
    ipady=12,
    padx=(0, 10)
)


# Placeholder
city_entry.insert(
    0,
    "Enter city name..."
)


# Remove placeholder when clicked
city_entry.bind(
    "<FocusIn>",
    remove_placeholder
)


# Add placeholder when empty
city_entry.bind(
    "<FocusOut>",
    add_placeholder
)


# Search button
search_button = tk.Button(
    search_frame,
    text="Search",
    font=("Arial", 12, "bold"),
    bg="#B447F5",
    fg="white",
    activebackground="#D35CFF",
    activeforeground="white",
    relief="flat",
    cursor="hand2",
    command=search_weather
)

search_button.pack(
    side="right",
    ipadx=15,
    ipady=8
)


# Press Enter
city_entry.bind(
    "<Return>",
    search_weather
)


# ======================================================
# CITY INFORMATION
# ======================================================

city_title = tk.Label(
    main_frame,
    text="Search a City",
    font=("Arial", 26, "bold"),
    bg="#241B5A",
    fg="white"
)

city_title.pack(
    pady=(20, 0)
)


state_title = tk.Label(
    main_frame,
    text="India",
    font=("Arial", 14),
    bg="#241B5A",
    fg="#D5CCFF"
)

state_title.pack()


# ======================================================
# CURRENT WEATHER
# ======================================================

weather_frame = tk.Frame(
    main_frame,
    bg="#302477"
)

weather_frame.pack(
    padx=35,
    pady=20,
    fill="x"
)


weather_icon = tk.Label(
    weather_frame,
    text="🌤️",
    font=("Arial", 65),
    bg="#302477",
    fg="white"
)

weather_icon.pack(
    pady=(20, 5)
)


temperature_label = tk.Label(
    weather_frame,
    text="--°C",
    font=("Arial", 48, "bold"),
    bg="#302477",
    fg="white"
)

temperature_label.pack()


condition_label = tk.Label(
    weather_frame,
    text="Search for weather",
    font=("Arial", 18),
    bg="#302477",
    fg="#E6DDFF"
)

condition_label.pack(
    pady=(0, 20)
)


# ======================================================
# DETAILS CARDS
# ======================================================

details_frame = tk.Frame(
    main_frame,
    bg="#241B5A"
)

details_frame.pack(
    fill="x",
    padx=35,
    pady=5
)


# ---------------- HUMIDITY ---------------- #

humidity_card = tk.Frame(
    details_frame,
    bg="#4938A5"
)

humidity_card.pack(
    side="left",
    expand=True,
    fill="both",
    padx=5
)


tk.Label(
    humidity_card,
    text="💧",
    font=("Arial", 22),
    bg="#4938A5",
    fg="white"
).pack(
    pady=(12, 2)
)


tk.Label(
    humidity_card,
    text="Humidity",
    font=("Arial", 11),
    bg="#4938A5",
    fg="#DCD5FF"
).pack()


humidity_value = tk.Label(
    humidity_card,
    text="--%",
    font=("Arial", 16, "bold"),
    bg="#4938A5",
    fg="white"
)

humidity_value.pack(
    pady=(2, 12)
)


# ---------------- WIND ---------------- #

wind_card = tk.Frame(
    details_frame,
    bg="#4938A5"
)

wind_card.pack(
    side="left",
    expand=True,
    fill="both",
    padx=5
)


tk.Label(
    wind_card,
    text="💨",
    font=("Arial", 22),
    bg="#4938A5",
    fg="white"
).pack(
    pady=(12, 2)
)


tk.Label(
    wind_card,
    text="Wind Speed",
    font=("Arial", 11),
    bg="#4938A5",
    fg="#DCD5FF"
).pack()


wind_value = tk.Label(
    wind_card,
    text="-- km/h",
    font=("Arial", 16, "bold"),
    bg="#4938A5",
    fg="white"
)

wind_value.pack(
    pady=(2, 12)
)


# ======================================================
# 7 DAY FORECAST
# ======================================================

forecast_title = tk.Label(
    main_frame,
    text="7-Day Forecast",
    font=("Arial", 18, "bold"),
    bg="#241B5A",
    fg="white"
)

forecast_title.pack(
    anchor="w",
    padx=40,
    pady=(20, 10)
)


forecast_frame = tk.Frame(
    main_frame,
    bg="#241B5A"
)

forecast_frame.pack(
    fill="x",
    padx=30,
    pady=(0, 40)
)


forecast_day_labels = []
forecast_icons = []
forecast_temp_labels = []
forecast_min_labels = []


for i in range(7):

    card = tk.Frame(
        forecast_frame,
        bg="#4938A5"
    )

    card.pack(
        side="left",
        expand=True,
        fill="both",
        padx=3
    )


    day = tk.Label(
        card,
        text="---",
        font=("Arial", 11, "bold"),
        bg="#4938A5",
        fg="white"
    )

    day.pack(
        pady=(10, 5)
    )


    icon = tk.Label(
        card,
        text="🌤️",
        font=("Arial", 22),
        bg="#4938A5",
        fg="white"
    )

    icon.pack()


    max_temp = tk.Label(
        card,
        text="--°",
        font=("Arial", 13, "bold"),
        bg="#4938A5",
        fg="white"
    )

    max_temp.pack(
        pady=(5, 0)
    )


    min_temp = tk.Label(
        card,
        text="--°",
        font=("Arial", 10),
        bg="#4938A5",
        fg="#C9C2F5"
    )

    min_temp.pack(
        pady=(0, 10)
    )


    forecast_day_labels.append(day)
    forecast_icons.append(icon)
    forecast_temp_labels.append(max_temp)
    forecast_min_labels.append(min_temp)


# ======================================================
# START APPLICATION
# ======================================================

root.mainloop()
