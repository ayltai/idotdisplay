from contextlib import asynccontextmanager
from enum import StrEnum
from os import path
from random import randrange

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from fastapi import FastAPI, File, Response, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from .bluetooth_manager import BluetoothManager
from .clock import draw_clock
from .commands import GifCommand, PowerCommand
from .config import Config
from .constants import PATH_IMAGE_ARTS, PATH_IMAGE_CELEBRITIES, PATH_IMAGE_GAMES, PATH_IMAGE_LANDMARKS, PATH_IMAGE_SEASONS
from .logging import log_error
from .packet_builder import PacketBuilder

JOB_KEEP_ALIVE  : str = 'keep_alive'
JOB_CELEBRITIES : str = 'celebrities'
JOB_CLOCK       : str = 'clock'
JOB_ARTS        : str = 'arts'
JOB_GAMES       : str = 'games'
JOB_LANDMARKS   : str = 'landmarks'
JOB_SEASONS     : str = 'seasons'
JOB_RANDOM      : str = 'random'

config            = Config()
bluetooth_manager = BluetoothManager(config.MAC_ADDRESS)
packet_builder    = PacketBuilder()
scheduler         = AsyncIOScheduler()


class SpaStaticFiles(StaticFiles):
    # pylint: disable=redefined-outer-name
    def lookup_path(self, path: str):
        full_path, stat_result = super().lookup_path(path)
        if stat_result is None:
            full_path, stat_result = super().lookup_path('index.html')
        return full_path, stat_result


class PowerState(StrEnum):
    ON  = 'on'
    OFF = 'off'


@asynccontextmanager
async def lifespan(_: FastAPI):
    await bluetooth_manager.start()

    scheduler.add_job(keep_alive, 'interval', seconds=5, id=JOB_KEEP_ALIVE)
    scheduler.add_job(send_clock, 'cron', minute='*', id=JOB_CLOCK)
    scheduler.add_job(send_arts, 'cron', minute='*', id=JOB_ARTS)
    scheduler.add_job(send_celebrities, 'cron', minute='*', id=JOB_CELEBRITIES)
    scheduler.add_job(send_games, 'cron', minute='*', id=JOB_GAMES)
    scheduler.add_job(send_landmarks, 'cron', minute='*', id=JOB_LANDMARKS)
    scheduler.add_job(send_seasons, 'cron', minute='*', id=JOB_SEASONS)
    scheduler.add_job(start_random, 'cron', minute='*', id=JOB_RANDOM)

    scheduler.start()

    scheduler.pause_job(JOB_ARTS)
    scheduler.pause_job(JOB_CELEBRITIES)
    scheduler.pause_job(JOB_GAMES)
    scheduler.pause_job(JOB_LANDMARKS)
    scheduler.pause_job(JOB_SEASONS)
    scheduler.pause_job(JOB_RANDOM)

    try:
        yield
    finally:
        await bluetooth_manager.stop()


app = FastAPI(title='iDot Display API Server', lifespan=lifespan)
app.add_middleware(CORSMiddleware, allow_headers=['*'], allow_methods=['*'], allow_origins=['*'])
app.mount('/web', SpaStaticFiles(directory=path.join(path.dirname(__file__), '..', 'web'), html=True), name='web')

@app.get('/api/v1/keep-alive')
async def keep_alive():
    try:
        await bluetooth_manager.send_packet(packet_builder.keep_alive_packet())

        return Response(status_code=200)
    # pylint: disable=broad-exception-caught
    except Exception as e:
        log_error(e)


@app.post('/api/v1/power/{state}')
async def set_power(state: PowerState):
    try:
        await bluetooth_manager.send_packet(packet_builder.build_packet(PowerCommand(state == PowerState.ON)))

        return Response(status_code=200)
    # pylint: disable=broad-exception-caught
    except Exception as e:
        log_error(e)


async def _send_gif(data: bytes):
    try:
        await bluetooth_manager.send_packet(packet_builder.build_packet(GifCommand(bluetooth_manager.get_time(), data)))

        return Response(status_code=200)
    # pylint: disable=broad-exception-caught
    except Exception as e:
        log_error(e)


@app.post('/api/v1/gif')
async def send_gif(file: UploadFile = File(...)):
    return await _send_gif(await file.read())


@app.get('/api/v1/arts')
async def send_arts():
    return await _send_gif(PATH_IMAGE_ARTS[randrange(0, len(PATH_IMAGE_ARTS))].read_bytes())


@app.post('/api/v1/arts')
async def start_arts():
    scheduler.pause_job(JOB_CLOCK)
    scheduler.resume_job(JOB_ARTS)
    scheduler.pause_job(JOB_CELEBRITIES)
    scheduler.pause_job(JOB_GAMES)
    scheduler.pause_job(JOB_LANDMARKS)
    scheduler.pause_job(JOB_SEASONS)
    scheduler.pause_job(JOB_RANDOM)

    await send_arts()

    return Response(status_code=200)


@app.delete('/api/v1/arts')
async def stop_arts():
    scheduler.pause_job(JOB_ARTS)

    return Response(status_code=200)


@app.get('/api/v1/celebrities')
async def send_celebrities():
    return await _send_gif(PATH_IMAGE_CELEBRITIES[randrange(0, len(PATH_IMAGE_CELEBRITIES))].read_bytes())


@app.post('/api/v1/celebrities')
async def start_celebrities():
    scheduler.pause_job(JOB_CLOCK)
    scheduler.pause_job(JOB_ARTS)
    scheduler.resume_job(JOB_CELEBRITIES)
    scheduler.pause_job(JOB_GAMES)
    scheduler.pause_job(JOB_LANDMARKS)
    scheduler.pause_job(JOB_SEASONS)
    scheduler.pause_job(JOB_RANDOM)

    await send_celebrities()

    return Response(status_code=200)


@app.delete('/api/v1/celebrities')
async def stop_celebrities():
    scheduler.pause_job(JOB_CELEBRITIES)

    return Response(status_code=200)


@app.get('/api/v1/games')
async def send_games():
    return await _send_gif(PATH_IMAGE_GAMES[randrange(0, len(PATH_IMAGE_GAMES))].read_bytes())


@app.post('/api/v1/games')
async def start_games():
    scheduler.pause_job(JOB_CLOCK)
    scheduler.pause_job(JOB_ARTS)
    scheduler.pause_job(JOB_CELEBRITIES)
    scheduler.resume_job(JOB_GAMES)
    scheduler.pause_job(JOB_LANDMARKS)
    scheduler.pause_job(JOB_SEASONS)
    scheduler.pause_job(JOB_RANDOM)

    await send_games()

    return Response(status_code=200)


@app.delete('/api/v1/games')
async def stop_games():
    scheduler.pause_job(JOB_GAMES)

    return Response(status_code=200)


@app.get('/api/v1/landmarks')
async def send_landmarks():
    return await _send_gif(PATH_IMAGE_LANDMARKS[randrange(0, len(PATH_IMAGE_LANDMARKS))].read_bytes())


@app.post('/api/v1/landmarks')
async def start_landmarks():
    scheduler.pause_job(JOB_CLOCK)
    scheduler.pause_job(JOB_ARTS)
    scheduler.pause_job(JOB_CELEBRITIES)
    scheduler.pause_job(JOB_GAMES)
    scheduler.resume_job(JOB_LANDMARKS)
    scheduler.pause_job(JOB_SEASONS)
    scheduler.pause_job(JOB_RANDOM)

    await send_landmarks()

    return Response(status_code=200)


@app.delete('/api/v1/landmarks')
async def stop_landmarks():
    scheduler.pause_job(JOB_LANDMARKS)

    return Response(status_code=200)


@app.get('/api/v1/seasons')
async def send_seasons():
    return await _send_gif(PATH_IMAGE_SEASONS[randrange(0, len(PATH_IMAGE_SEASONS))].read_bytes())


@app.post('/api/v1/seasons')
async def start_seasons():
    scheduler.pause_job(JOB_CLOCK)
    scheduler.pause_job(JOB_ARTS)
    scheduler.pause_job(JOB_CELEBRITIES)
    scheduler.pause_job(JOB_GAMES)
    scheduler.pause_job(JOB_LANDMARKS)
    scheduler.resume_job(JOB_SEASONS)
    scheduler.pause_job(JOB_RANDOM)

    await send_seasons()

    return Response(status_code=200)


@app.delete('/api/v1/seasons')
async def stop_seasons():
    scheduler.pause_job(JOB_SEASONS)

    return Response(status_code=200)


@app.get('/api/v1/clock')
async def send_clock():
    return await _send_gif(await draw_clock())


@app.post('/api/v1/clock')
async def start_clock():
    scheduler.resume_job(JOB_CLOCK)
    scheduler.pause_job(JOB_ARTS)
    scheduler.pause_job(JOB_CELEBRITIES)
    scheduler.pause_job(JOB_GAMES)
    scheduler.pause_job(JOB_LANDMARKS)
    scheduler.pause_job(JOB_SEASONS)
    scheduler.pause_job(JOB_RANDOM)

    await send_clock()

    return Response(status_code=200)


@app.delete('/api/v1/clock')
async def stop_clock():
    scheduler.pause_job(JOB_CLOCK)

    return Response(status_code=200)


@app.post('/api/v1/random')
async def start_random():
    scheduler.pause_job(JOB_CLOCK)
    scheduler.pause_job(JOB_ARTS)
    scheduler.pause_job(JOB_CELEBRITIES)
    scheduler.pause_job(JOB_GAMES)
    scheduler.pause_job(JOB_LANDMARKS)
    scheduler.pause_job(JOB_SEASONS)

    random_job = randrange(0, 5)

    if random_job == 0:
        await send_clock()
    elif random_job == 1:
        await send_arts()
    elif random_job == 2:
        await send_celebrities()
    elif random_job == 3:
        await send_games()
    elif random_job == 4:
        await send_landmarks()
    elif random_job == 5:
        await send_seasons()

    scheduler.resume_job(JOB_RANDOM)

    return Response(status_code=200)

@app.delete('/api/v1/random')
async def stop_random():
    scheduler.pause_job(JOB_RANDOM)

    return Response(status_code=200)
