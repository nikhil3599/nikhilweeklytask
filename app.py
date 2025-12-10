# app.py
from dotenv import load_dotenv
import os
import requests
import json
import boto3
from botocore.exceptions import NoCredentialsError
import time

# --- Load environment variables ---
load_dotenv()
API_KEY = os.getenv("OPENWEATHER_API_KEY")

# Temporary check
print("API KEY LOADED:", API_KEY)  # Remove after confirming

# --- Configuration ---
CITIES = ["London", "New York", "Tokyo"]
S3_BUCKET = "your-s3-bucket-name"  # Replace with your bucket name
S3_FILE_NAME = "weather_data.json"
UPLOAD_TO_S3 = False  # Set True to upload to S3

# --- Fetch weather data with retry ---
def fetch_weather(city, retries=3, delay=2):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    for attempt in range(1, retries + 1):
        try:
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                return {
                    "city": city,
                    "temperature": data["main"]["temp"],
                    "description": data["weather"][0]["description"]
                }
            else:
                print(f"Attempt {attempt} failed for {city}. Status code: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"Attempt {attempt} error for {city}: {e}")
        time.sleep(delay)
    print(f"Failed to fetch weather for {city} after {retries} attempts.")
    return None

# --- Upload to S3 ---
def upload_to_s3(file_name, bucket, data):
    s3 = boto3.client('s3')
    try:
        s3.put_object(Bucket=bucket, Key=file_name, Body=json.dumps(data))
        print(f"Data uploaded to S3 bucket '{bucket}' as '{file_name}'")
    except NoCredentialsError:
        print("AWS credentials not found or invalid.")

# --- Main script ---
def main():
    all_weather = []

    for city in CITIES:
        print(f"Fetching weather for: {city}")
        weather = fetch_weather(city)
        if weather:
            all_weather.append(weather)
    
    # Save locally
    with open("weather_data.json", "w") as f:
        json.dump(all_weather, f, indent=4)
    
    # Optional S3 upload
    if UPLOAD_TO_S3:
        upload_to_s3(S3_FILE_NAME, S3_BUCKET, all_weather)

    print("Done!")

if __name__ == "__main__":
    main()

