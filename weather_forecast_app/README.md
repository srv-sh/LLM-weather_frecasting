<div align="center">

# Weather Forecast APP
| Version Info | [![Python](https://img.shields.io/badge/python-v3.9.0-green)](https://www.python.org/downloads/release/python-3913/) [![Platform](https://img.shields.io/badge/Platforms-Ubuntu%2022.04.1%20LTS%2C%20win--64-orange)](https://releases.ubuntu.com/20.04/) |
| ------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Author       | [![LinkedIn-profile](https://img.shields.io/badge/LinkedIn-Profile-informational?logo=linkedin)](https://www.linkedin.com/in/sourav-saha-3968031b8/) [![GitHub-profile](https://img.shields.io/badge/GitHub-Profile-informational?logo=github)](https://github.com/srv-sh)
---

</div>

## Overview
The Advanced Weather Forecast App is a cutting-edge weather prediction application that leverages the power of LSTM (Long Short-Term Memory) neural networks to offer users highly accurate and reliable weather forecasts. This innovative app not only provides current weather conditions but also forecasts for the upcoming days with a level of precision and detail that sets it apart from traditional weather apps.

## Installation

#### Step 1: Clone this repository
```bash
git https://github.com/srv-sh/stativ_task.git
cd stativ_task/weather_forecast_app
```
#### Step 2: Create virtual environment

*Conda environment:*
```
conda create -n rc python==3.9.0
conda activate rc
```
#### Step 3: Install dependencies

```bash
pip install -r requirements.txt
```
> Run the [`weatherforecasting.ipynb`](weatherforecasting.ipynb) file in jupyter notebook to train timeseries model.



 ## Inferance

 To infer the model just run below command 

 ```bash
sudo docker compose run  
```

> When executing the command, a UVicorn route will become accessible at a URL like http://0.0.0.0:8000/docs. This route prompts you to specify the desired forecast time period, and upon submission, it returns a JSON containing a collection of dates representing forecast periods paired with their corresponding predicted weather values in Celsius degrees.


> NOTE: Please note that the URL "https://archive-api.open-meteo.com/v1/archive" is not up to date, and as a result, the forecasting results cannot be based on data from the current date up to the specified forecast period.