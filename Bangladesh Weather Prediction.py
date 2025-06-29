import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime, timedelta
import numpy as np
from scipy import stats

# Load the historical weather data
df = pd.read_csv("query.csv")
df['Data Timestamp'] = pd.to_datetime(df['Data Timestamp'])
df['Month'] = df['Data Timestamp'].dt.month
df['Day'] = df['Data Timestamp'].dt.day

# Calculate monthly climate norms
monthly_norms = df.groupby('Month').agg({
    'TEMP MIN DEG': 'mean',
    'TEMP MAX DEG': 'mean',
    'RH MIN %': 'mean',
    'RH MAX %': 'mean',
    'RAIN SUM MM': 'mean'
}).reset_index()


def determine_condition(rain, humidity):
    """Determine weather condition based on rainfall and humidity"""
    if rain > 20:
        return "Heavy Rain"
    elif rain > 5:
        return "Moderate Rain"
    elif rain > 0.5:
        return "Light Rain"
    elif rain > 0:
        return "Drizzle"
    elif humidity > 85:
        return "Humid and Cloudy"
    elif humidity > 70:
        return "Partly Cloudy"
    else:
        return "Sunny"


def get_seasonal_weather(month, day):
    """Get seasonal weather patterns for any date"""
    # Find similar dates (±15 days) in historical data
    similar_dates = df[
        (df['Month'] == month) &
        (df['Day'].between(max(1, day - 15), min(31, day + 15)))
        ]

    if len(similar_dates) > 0:
        # Calculate weighted average (closer dates have more weight)
        weights = 1 / (1 + abs(similar_dates['Day'] - day))
        temp_min = np.average(similar_dates['TEMP MIN DEG'], weights=weights)
        temp_max = np.average(similar_dates['TEMP MAX DEG'], weights=weights)
        humidity = np.average((similar_dates['RH MIN %'] + similar_dates['RH MAX %']) / 2, weights=weights)
        rain = np.average(similar_dates['RAIN SUM MM'], weights=weights)
    else:
        # Fallback to monthly averages
        month_data = monthly_norms[monthly_norms['Month'] == month]
        if len(month_data) > 0:
            temp_min = month_data['TEMP MIN DEG'].values[0]
            temp_max = month_data['TEMP MAX DEG'].values[0]
            humidity = (month_data['RH MIN %'].values[0] + month_data['RH MAX %'].values[0]) / 2
            rain = month_data['RAIN SUM MM'].values[0]
        else:
            # Default values if no data available
            temp_min, temp_max = 25, 32  # Typical Bangladesh temperatures
            humidity = 75
            rain = 5

    return temp_min, temp_max, humidity, rain


def predict_weather(date_str):
    """Predict weather for any given date"""
    try:
        input_date = datetime.strptime(date_str, "%m-%d-%Y")
        month = input_date.month
        day = input_date.day

        # Check if we have exact historical data
        exact_match = df[df['Data Timestamp'].dt.date == input_date.date()]

        if not exact_match.empty:
            # Use actual historical data if available
            row = exact_match.iloc[0]
            temp_min = row['TEMP MIN DEG']
            temp_max = row['TEMP MAX DEG']
            humidity = (row['RH MIN %'] + row['RH MAX %']) / 2
            rain = row['RAIN SUM MM']
            is_future = False
        else:
            # Predict based on seasonal patterns
            temp_min, temp_max, humidity, rain = get_seasonal_weather(month, day)
            is_future = True

        # Determine weather condition
        condition = determine_condition(rain, humidity)

        # Simulate hourly temperatures (sinusoidal pattern)
        hours = list(range(24))
        base_temp = (temp_min + temp_max) / 2
        temp_range = temp_max - temp_min
        temperatures = [base_temp + (temp_range / 2) * np.sin((h - 6) / 24 * 2 * np.pi) + np.random.uniform(-1, 1) for h
                        in hours]

        # Create the plot
        plt.figure(figsize=(12, 6))

        # Set background color
        ax = plt.gca()
        ax.set_facecolor('#f5f5f5')
        plt.grid(True, color='white', linestyle='-', linewidth=0.5)

        # Plot temperature curve
        plt.plot(hours, temperatures, marker='o', color='#e63946', linewidth=2, markersize=8)

        # Add day/night shading
        sunrise, sunset = 6, 18
        plt.axvspan(0, sunrise, color='#023047', alpha=0.1)
        plt.axvspan(sunset, 24, color='#023047', alpha=0.1)

        # Set title and labels
        title_prefix = "Predicted" if is_future else "Historical"
        plt.title(f"{title_prefix} Weather in Bangladesh on {date_str}\nCondition: {condition}", pad=20)
        plt.xlabel("Hour of Day", labelpad=10)
        plt.ylabel("Temperature (\u00b0C)", labelpad=10)

        # Configure axes
        plt.xticks(hours)
        plt.xlim(0, 23)
        plt.ylim(temp_min - 2, temp_max + 2)

        # Add weather icon
        if "rain" in condition.lower():
            plt.text(22, temp_max + 1, "🌧️", fontsize=20, ha='center')
        elif "sunny" in condition.lower():
            plt.text(22, temp_max + 1, "☀️", fontsize=20, ha='center')
        elif "cloud" in condition.lower():
            plt.text(22, temp_max + 1, "⛅", fontsize=20, ha='center')

        plt.tight_layout()

        # Print weather information
        print(f"\n{'=' * 50}")
        print(f"{title_prefix} Weather in Bangladesh on {date_str}")
        print(f"{'=' * 50}")
        print(f"Condition: {condition}")
        print(f"Temperature Range: {temp_min:.1f}°C to {temp_max:.1f}°C")
        print(f"Average Humidity: {humidity:.0f}%")
        print(f"Rainfall: {rain:.1f} mm")

        # Print recommendations
        print("\nRecommendations:")
        if rain > 10:
            print("⚠️ Heavy rain expected - carry an umbrella and waterproof gear")
        elif rain > 5:
            print("☔ Moderate rain likely - bring an umbrella and waterproof shoes")
        elif rain > 0.1:
            print("🌦️ Light rain possible - consider bringing an umbrella")

        if temp_max > 35:
            print("🥵 Extreme heat warning - stay hydrated and avoid sun exposure")
        elif temp_max > 30:
            print("😓 Hot weather - wear light clothing and use sunscreen")
        elif temp_min < 15:
            print("🧣 Cool temperatures - dress in layers")

        if humidity > 80:
            print("💦 High humidity - expect muggy and uncomfortable conditions")
        elif humidity > 70:
            print("🌫️ Moderate humidity - may feel sticky")

        print(f"\nNote: {'Prediction based on seasonal patterns' if is_future else 'Actual historical data'}")
        plt.show()

    except ValueError:
        print("\nInvalid date format. Please use MM-DD-YYYY format (e.g., 06-15-2018)")
    except Exception as e:
        print(f"\nAn error occurred: {str(e)}")


# Main program
def main():
    print("\n" + "=" * 50)
    print("BANGLADESH WEATHER FORECAST")
    print("=" * 50)
    print("\nHistorical data from 2017-2018 used for predictions")
    print("For dates outside this range, seasonal patterns are used")

    while True:
        date_input = input("\nEnter a date (MM-DD-YYYY) or 'q' to quit: ")
        if date_input.lower() == 'q':
            print("\nThank you for using the Bangladesh Weather Forecast!")
            break

        try:
            input_date = datetime.strptime(date_input, "%m-%d-%Y")
            predict_weather(date_input)
        except ValueError:
            print("\nInvalid date format. Please use MM-DD-YYYY format (e.g., 06-15-2018)")


if __name__ == "__main__":
    main()
