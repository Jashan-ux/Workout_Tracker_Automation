import requests
import os
from datetime import datetime as dt
GENDER = "male"
WEIGHT_KG = "51"
HEIGHT_CM = "182"
AGE = "20"

NIX_APP_ID = os.getenv("NIX_APP_ID")
NIX_API_KEY= os.getenv("NIX_API_KEY")
SHEETY_AUTH= os.getenv("SHEETY_AUTH")


EXERCISE_ENDPOINT = "https://trackapi.nutritionix.com/v2/natural/exercise"
SHEETY_ENDPOINT  = "https://api.sheety.co/c97ddcf246b18fca233de42f8722e033/myWorkouts/workouts"

query_input = input("How much did you exercise? (e.g., 'run 100 meters'): ")
headers = {
    "x-app-id" : NIX_APP_ID,
    "x-app-key" : NIX_API_KEY,
    "Content-Type": "application/json"
}
body = {
    
    "query" : query_input,
    "gender": GENDER,
    "weight_kg": WEIGHT_KG,
    "height_cm": HEIGHT_CM,
    "age": AGE

}


response = requests.post(url = EXERCISE_ENDPOINT , json = body , headers= headers )
response.json()



if response.status_code == 200:
    # Process the exercises if the request is successful
    exercises = response.json().get("exercises", [])
    
    today_date = dt.now().strftime("%d/%m/%Y")
    now_time = dt.now().strftime("%X")

    for exercise in exercises:
        
        sheet_inputs = {
            "workout": {
                "date": today_date,
                "time": now_time,
                "exercise": exercise["name"].title(),
                "duration": exercise["duration_min"],
                "calories": exercise["nf_calories"],
                "met" : exercise["met"]
            }
        }
        
        sheet_response = requests.post(
        SHEETY_ENDPOINT,
        json=sheet_inputs,
        auth=(
            os.environ["ENV_SHEETY_USERNAME"],
            os.environ["ENV_SHEETY_PASSWORD"],
        )
    )

    
else:

    print("Error:", response.json())

