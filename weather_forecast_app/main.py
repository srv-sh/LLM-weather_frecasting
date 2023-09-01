from fastapi import FastAPI
from pydantic import BaseModel
import requests
import pandas as pd
from datetime import datetime, timedelta
import joblib
from keras.models import load_model
import numpy as np
# Create a FastAPI instance
app = FastAPI()

# Define a request model
class WeatherRequest(BaseModel):
    """
    Request model for weather forecasting.

    Attributes:
        period (int): The number of days to forecast the weather.
    """
        
    period: int

    def data(self):
        """
        Fetches historical weather data from an API.

        Returns:
            DataFrame: A DataFrame containing historical weather data.
        """



        end_date = datetime.now() -timedelta(days=1)
        end_date = end_date.strftime("%Y-%m-%d")
        start_date = "2023-01-10"
        api_url = "https://archive-api.open-meteo.com/v1/archive"

        # Set the latitude and longitude for Dhaka
        latitude = 23.7104
        longitude = 90.4074

        # Define the parameters for the API request
        params = {
            "latitude": latitude,
            "longitude": longitude,
            "start_date": start_date,
            "end_date": end_date,
            "daily": "temperature_2m_max,temperature_2m_min,windspeed_10m_max,windgusts_10m_max",
            "timezone": "auto",
        }

        # Send a GET request to the API
        response = requests.get(api_url, params=params)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            data = response.json()
            df = pd.DataFrame(data['daily'])
            df.dropna(inplace=True)
    
            return df 
        else:
            return {"error": f"Error: {response.status_code}"}





@app.post("/fetch_weather/")
async def fetch_weather(request: WeatherRequest):

    """
    Fetches weather forecasts using historical data and a machine learning model.

    Args:
        request (WeatherRequest): The request containing the forecast period.

    Returns:
        dict: A JSON response with forecasted weather data.
    """

    n_future = 1
    n_past = 14

    scaler = joblib.load('utils/scaler.pkl')
    model = load_model('utils/model.h5')
    dataX = []

    data = request.data()

    cols = list(data)[1:]
    df_for_training = data[cols].astype(float)

    df_for_training_scaled = scaler.transform(df_for_training)

    for i in range(n_past, len(df_for_training_scaled) - n_future +1):
        dataX.append(df_for_training_scaled[i - n_past:i, 0:df_for_training.shape[1]])

    dataX = np.array(dataX)

    n_future = request.period

    train_dates = pd.to_datetime(data["time"])
    forecast_period_dates = pd.date_range(list(train_dates)[-1], periods=n_future, freq='1d').tolist()
    
    forecast = model.predict(dataX[-n_future:])
    
    forecast_copies = np.repeat(forecast,df_for_training.shape[1], axis=-1)
    y_pred_future = scaler.inverse_transform(forecast_copies)[:,0]

    #convert timestamp to date
    forecast_dates= []
    for time_i in forecast_period_dates:
        forecast_dates.append(time_i.date())

    response_data = {
        "forecast_period_dates": forecast_dates,
        "y_pred_future": y_pred_future.tolist() 
    }

    return response_data


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
