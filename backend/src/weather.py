from dataclasses import dataclass
from typing import Optional

from httpx import AsyncClient, AsyncHTTPTransport


@dataclass
class TimedModel:
    time : int


@dataclass
class PartialWeather(TimedModel):
    weather_code : Optional[int]


@dataclass
class Currently(PartialWeather):
    temperature : float


@dataclass
class Daily(PartialWeather):
    temperature_min : Optional[float]
    temperature_max : Optional[float]


@dataclass
class Weather:
    currently : Currently
    daily     : list[Daily]


async def get_weather(latitude: float, longitude: float, timezone: str) -> Weather:
    async with AsyncClient(transport=AsyncHTTPTransport(retries=3), timeout=30) as client:
        response = await client.get('https://api.open-meteo.com/v1/forecast', params={
            'latitude'      : latitude,
            'longitude'     : longitude,
            'current'       : 'weather_code,temperature_2m',
            'daily'         : 'weather_code,temperature_2m_max,temperature_2m_min',
            'forecast_days' : 1,
            'timezone'      : timezone,
            'timeformat'    : 'unixtime',
        })
        response.raise_for_status()

        json = response.json()

        return Weather(
            currently=Currently(
                time=json['current']['time'],
                weather_code=json['current']['weather_code'],
                temperature=json['current']['temperature_2m'],
            ),
            daily=[
                Daily(
                    time=t,
                    weather_code=wc,
                    temperature_min=tmin,
                    temperature_max=tmax,
                )
                for t, wc, tmin, tmax in zip(
                    json['daily']['time'],
                    json['daily']['weather_code'],
                    json['daily']['temperature_2m_min'],
                    json['daily']['temperature_2m_max'],
                )
            ],
        )
