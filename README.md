# Weather Webhook Notifier 🌤️🔗

A lightweight Python application designed to demonstrate working with webhooks. It fetches real-time weather data for a user-selected city via the OpenWeatherMap API and dispatches the temperature information as a JSON payload to a configured webhook endpoint (such as Webhook.site).

---

## 🎯 Purpose

The primary goal of this project is to showcase how to integrate external APIs with **Webhooks** in Python using a clean, object-oriented, and modular architecture.

---

## ✨ Features

- **Interactive CLI:** Uses `inquirer` to let users search and select countries interactively.
- **Geocoding & Weather API Integration:** Resolves city coordinates and fetches metric temperatures using OpenWeatherMap.
- **Webhook Integration:** Sends a `POST` request containing weather updates to any designated webhook URL.
- **Clean Architecture:** Built using Python `dataclasses`, explicit type hinting, and reusable `requests.Session` instances.

---

## ⚙️ Setup & Configuration

Before running the application, you need to set up an environment configuration file:

1. Create a `.env` file in the root directory of the project (alongside `main.py`).
2. Add your environment variables to `.env`:

```env
OPENWEATHER_API_KEY="Your_API_Key"
WEBHOOK_URL="https://webhook.site/your-unique-uuid-here"
```

---

## 📋 Prerequisites

Make sure you have Python 3.10+ installed on your system. Install the required dependencies using:

```bash
pip install requests pycountry inquirer python-dotenv
```

---

## 🔑 How to get your keys:
OPENWEATHER_API_KEY: Sign up for a free developer account at [OpenWeatherMap](https://openweathermap.org/) and generate an API key from your account dashboard.

WEBHOOK_URL: Visit [Webhook.site](https://webhook.site/) to automatically generate a free, unique testing URL where you can observe incoming webhook payloads in real time.

---

## 🔄 Execution Flow:

1. Select a country from the interactive list.
2. Enter the target city name.
3. The app fetches the current temperature in Celsius.
4. A POST payload is sent to your WEBHOOK_URL containing the city, country, temperature, and status message.

---

## 📦 Webhook Payload Format
The outgoing POST request payload sent to your webhook URL looks like this:

```JSON
{
  "city": "Lappeenranta",
  "country": "Finland",
  "temperature": 7.5,
  "message": "Air conditioning status updated"
}
```

---

## 📄 License
This project is open-source and available under the MIT License.



