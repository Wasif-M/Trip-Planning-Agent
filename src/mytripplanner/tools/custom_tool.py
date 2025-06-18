from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
from src.mytripplanner.utilies.weather_api import get_day_weather_forecast
import json
class WeatherForecastToolInput(BaseModel):
    location: str = Field(..., description="Location for the weather forecast (city name, coordinates, etc.)")
    days: int = Field( description="Number of days for which the weather information should be fetched (1-10)")

class WeatherForecastTool(BaseTool):
    name: str = "Weather Forecast Tool"
    description: str = (
        "Fetches real-time weather for a given location and number of days (up to 10) using WeatherAPI.com. "
        "Returns a summary of the forecast."
    )
    args_schema: Type[BaseModel] = WeatherForecastToolInput

    def _run(self, location: str, days: int ) -> str:
        data = get_day_weather_forecast(location, days)
        if "error" in data:
            return data["error"]
        forecast_days = data.get("forecast", {}).get("forecastday", [])
        summary = []
        for day in forecast_days:
            date = day.get("date")
            condition = day.get("day", {}).get("condition", {}).get("text", "N/A")
            max_temp = day.get("day", {}).get("maxtemp_c", "N/A")
            min_temp = day.get("day", {}).get("mintemp_c", "N/A")
            summary.append(f"{date}: {condition}, High: {max_temp}°C, Low: {min_temp}°C")
        return "\n".join(summary) if summary else json.dumps(data)
