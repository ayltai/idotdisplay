from contextlib import asynccontextmanager
from enum import StrEnum

from fastapi import FastAPI, File, Response, UploadFile
from fastapi.middleware.cors import CORSMiddleware

from .bluetooth_manager import BluetoothManager
from .commands import GifCommand, PowerCommand
from .config import Config
from .logging import log_error
from .packet_builder import PacketBuilder

config            = Config()
bluetooth_manager = BluetoothManager(config.MAC_ADDRESS)
packet_builder    = PacketBuilder()


class PowerState(StrEnum):
    ON  = 'on'
    OFF = 'off'


@asynccontextmanager
async def lifespan(_: FastAPI):
    await bluetooth_manager.start()

    try:
        yield
    finally:
        await bluetooth_manager.stop()


app = FastAPI(title='iDot Display API Server', lifespan=lifespan)
app.add_middleware(CORSMiddleware, allow_headers=['*'], allow_methods=['*'], allow_origins=['*'])


@app.post('/api/v1/power/{state}')
async def set_power(state: PowerState):
    try:
        await bluetooth_manager.send_packet(packet_builder.build_packet(PowerCommand(state == PowerState.ON)))

        return Response(status_code=200)
    # pylint: disable=broad-exception-caught
    except Exception as e:
        log_error(e)


@app.post('/api/v1/gif')
async def send_gif(file: UploadFile = File(...)):
    try:
        await bluetooth_manager.send_packet(packet_builder.build_packet(GifCommand(bluetooth_manager.get_time(), await file.read())))

        return Response(status_code=200)
    # pylint: disable=broad-exception-caught
    except Exception as e:
        log_error(e)
