import os
from dataclasses import dataclass

import inquirer
import pycountry
import requests
from pathlib import Path
from dotenv import load_dotenv


@dataclass(frozen=True)
class Coordinates:
    lat: float
    lon: float


class OpenWeatherClient:
    GEOCODING_URL = "https://api.openweathermap.org/geo/1.0/direct"
    WEATHER_URL = "https://api.openweathermap.org/data/2.5/weather"

    def __init__(
        self,
        api_key: str,
        session: requests.Session | None = None,
    ) -> None:
        self.api_key = api_key
        self.session = session or requests.Session()

    def get_coordinates(self, city: str, country_code: str) -> Coordinates:
        response = self.session.get(
            self.GEOCODING_URL,
            params={
                "q": f"{city},{country_code}",
                "limit": 1,
                "appid": self.api_key,
            },
            timeout=10,
        )
        response.raise_for_status()

        results = response.json()
        if not results:
            raise LookupError(f"No coordinates found for {city}, {country_code}.")

        return Coordinates(
            lat=results[0]["lat"],
            lon=results[0]["lon"],
        )

    def get_temperature_celsius(self, coordinates: Coordinates) -> float:
        response = self.session.get(
            self.WEATHER_URL,
            params={
                "lat": coordinates.lat,
                "lon": coordinates.lon,
                "appid": self.api_key,
                "units": "metric",
            },
            timeout=10,
        )
        response.raise_for_status()

        return float(response.json()["main"]["temp"])


class WebhookNotifier:
    def __init__(
        self,
        webhook_url: str,
        session: requests.Session | None = None,
    ) -> None:
        self.webhook_url = webhook_url
        self.session = session or requests.Session()

    def send_temperature(
        self,
        city: str,
        country: str,
        temperature: float,
    ) -> None:
        response = self.session.post(
            self.webhook_url,
            json={
                "city": city,
                "country": country,
                "temperature": temperature,
                "message": "Air conditioning status updated",
            },
            timeout=10,
        )
        response.raise_for_status()


class WeatherApp:
    def __init__(
        self,
        weather: OpenWeatherClient,
        notifier: WebhookNotifier,
    ) -> None:
        self.weather = weather
        self.notifier = notifier

    def run(self) -> None:
        selected_country = inquirer.list_input(
            "Select a country:",
            choices=[country.name for country in pycountry.countries],
        )
        country = pycountry.countries.lookup(selected_country)

        city = input("Enter the city name: ").strip()
        if not city:
            raise ValueError("City name cannot be empty.")

        coordinates = self.weather.get_coordinates(city, country.alpha_2)
        temperature = self.weather.get_temperature_celsius(coordinates)
        print(
            f"Current temperature in {city}, {country.name}: "
            f"{temperature:.2f}°C"
        )

        self.notifier.send_temperature(city, country.name, temperature)
        print("Webhook sent successfully.")


def main() -> None:
    load_dotenv(dotenv_path=Path(__file__).resolve().parent / ".env")
    api_key = os.getenv("OPENWEATHER_API_KEY")
    webhook_url = os.getenv("WEBHOOK_URL")

    if not api_key or not webhook_url:
        raise RuntimeError(
            "Set OPENWEATHER_API_KEY and WEBHOOK_URL environment variables."
        )

    app = WeatherApp(
        weather=OpenWeatherClient(api_key),
        notifier=WebhookNotifier(webhook_url),
    )
    app.run()


if __name__ == "__main__":
    main()
