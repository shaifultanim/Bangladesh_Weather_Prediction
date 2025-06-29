
# Bangladesh-Weather-forecasting-
# Bangladesh Weather Forecast Project

## 📌 Overview
This project provides weather forecasting for Bangladesh using historical weather data. It can:
- Display historical weather data when available (2017-2018)
- Predict weather for any date using seasonal patterns
- Generate visual temperature forecasts with weather condition emojis
- Provide weather recommendations (umbrella alerts, heat warnings, etc.)

## 📊 Sample Output
![Sample Weather Forecast](https://github.com/user-attachments/assets/f454e8ad-0536-4602-b1fd-eb201a3b8858)
![17501716059182752258554425528672](https://github.com/user-attachments/assets/8e862ded-f92d-4b37-aa72-1a0f22a14d85)
![17501713978923474674159982778500](https://github.com/user-attachments/assets/e3090a52-487a-488e-a8d0-b87656f808da)



## 🛠️ Tools & Technologies
- **Python 3** (with the following libraries):
  - `pandas` - For data manipulation and analysis
  - `matplotlib` - For data visualization
  - `numpy` - For numerical operations
  - `scipy` - For statistical calculations
  - `datetime` - For date/time handling

## 📂 File Structure
```
bangladesh-weather/
├── weather_forecast.py    # Main Python script
├── query.csv             # Historical weather data
├── README.md             # This file
└── requirements.txt      # Dependencies
```

## ⚙️ Installation
1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/bangladesh-weather.git
   cd bangladesh-weather
   ```

2. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

## 🚀 Usage
Run the script with:
```bash
python weather_forecast.py
```

When prompted, enter a date in MM-DD-YYYY format (e.g., 06-15-2018).

### Features:
- **Historical Data**: Shows actual weather if date is between 2017-2018
- **Predictions**: Estimates weather for other dates using seasonal patterns
- **Visualization**: Displays 24-hour temperature forecast graph
- **Recommendations**: Provides weather-specific advice

## 📝 Data Requirements
The script expects a CSV file named `query.csv` with these columns:
- `Data Timestamp` (datetime)
- `TEMP MIN DEG` (minimum temperature)
- `TEMP MAX DEG` (maximum temperature)
- `RH MIN %` (minimum humidity)
- `RH MAX %` (maximum humidity)
- `RAIN SUM MM` (rainfall in mm)

## 🤝 Contributing
Contributions are welcome! Please open an issue or submit a pull request.

## 📜 License
This project is licensed under the MIT License.
