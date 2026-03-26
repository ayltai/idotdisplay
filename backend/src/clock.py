from datetime import datetime
from io import BytesIO

from PIL import Image, ImageDraw, ImageFont

from .config import Config
from .constants import PATH_FONT, PATH_IMAGE_WEATHER
from .logging import log_error
from .weather import get_weather

config = Config()


async def draw_clock() -> bytes:
    image = Image.new('RGB', (config.DISPLAY_WIDTH, config.DISPLAY_HEIGHT), (0, 0, 0))
    draw  = ImageDraw.Draw(image)

    try:
        font = ImageFont.truetype(str(PATH_FONT), 5)
    # pylint: disable=broad-exception-caught
    except Exception as e:
        log_error(e)

        font = ImageFont.load_default()

    now     = datetime.now()
    weather = await get_weather(config.LATITUDE, config.LONGITUDE, config.TIMEZONE)
    date    = now.strftime('%d-%m').upper()
    weekday = now.strftime('%a').upper()
    time    = now.strftime('%I:%M').upper()
    part    = 'A' if now.hour < 12 else 'P'

    temperature_max = str(round(weather.daily[0].temperature_max))
    temperature_min = str(round(weather.daily[0].temperature_min))
    temperature     = str(round(weather.currently.temperature))

    with Image.open(PATH_IMAGE_WEATHER[weather.currently.weather_code]) as icon:
        icon = icon.convert('RGB')

        image.paste(icon, (1, 0))

    draw.fontmode = '0'

    draw.text((17 if len(temperature_max) > 1 else 21, 3), f'{temperature_max}\'C', fill=(255, 204, 128), font=font)
    draw.text((17 if len(temperature_min) > 1 else 21, 12), f'{temperature_min}\'C', fill=(100, 181, 246), font=font)
    draw.text((2 if len(temperature) > 1 else 6, 12), f'{temperature}\'C', fill=(255, 255, 255), font=font)
    draw.text((0, 19), date, fill=(144, 164, 174), font=font)
    draw.text((21, 19), weekday, fill=(79, 195, 247) if now.weekday() == 5 else (244, 67, 54) if now.weekday() == 6 else (76, 175, 80), font=font)
    draw.text((2, 26), time, fill=(255, 255, 255), font=font)
    draw.text((21, 26), part, fill=(255, 255, 255), font=font)

    buffer = BytesIO()
    image.convert('P', palette=Image.Palette.ADAPTIVE, colors=8).save(buffer, format='GIF')

    return buffer.getvalue()
