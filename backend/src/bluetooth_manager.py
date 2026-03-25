from asyncio import CancelledError, create_task, Event, Lock, sleep, Task
from time import time

from bleak import BleakClient

from .config import Config
from .logging import log_debug, log_error

config = Config()


class BluetoothManager:
    def __init__(self, mac_address: str):
        self.mac_address   : str                = mac_address
        self._client       : BleakClient | None = None
        self._connect_task : Task | None        = None
        self._write_lock   : Lock               = Lock()
        self._stop_event   : Event              = Event()
        self._start_time   : float              = 0.0

    def get_time(self) -> int:
        return round((time() - self._start_time if self._start_time else 0.0) * 1000)

    async def send_packet(self, packet: bytes) -> None:
        async with self._write_lock:
            if not self._client or not self._client.is_connected:
                raise RuntimeError('Not connected to Bluetooth device.')

            for i in range(0, len(packet), config.MAX_PACKET_SIZE):
                chunk = packet[i:i + config.MAX_PACKET_SIZE]

                log_debug(f'Sending packet chunk: {chunk.hex()}')

                await self._client.write_gatt_char(config.WRITE_UUID, chunk, response=True)

                await sleep(config.WRITE_DELAY)

    async def start(self) -> None:
        self._stop_event.clear()

        self._connect_task = create_task(self._connection_loop())

    async def stop(self) -> None:
        self._stop_event.set()

        if self._connect_task:
            self._connect_task.cancel()

            try:
                await self._connect_task
            except CancelledError:
                pass

        if self._client and self._client.is_connected:
            await self._client.disconnect()

    async def _connection_loop(self) -> None:
        while not self._stop_event.is_set():
            try:
                if self._client and self._client.is_connected:
                    await sleep(1)

                    continue

                log_debug(f'Connecting to Bluetooth device at {self.mac_address}...')

                self._client = BleakClient(self.mac_address)

                await self._client.connect()

                log_debug('Connected to Bluetooth device.')

                self._start_time = time()

                await self._client.start_notify(config.NOTIFY_UUID, self._notification_handler)

                log_debug('Subscribed to notifications.')
            # pylint: disable=broad-exception-caught
            except Exception as e:
                log_error(e)

                await self._safe_disconnect()

                await sleep(config.RECONNECT_DELAY)

    @staticmethod
    def _notification_handler(sender, data: bytearray) -> None:
        log_debug(f'Received notification from {sender.uuid}: {data.hex()}')

    async def _safe_disconnect(self) -> None:
        try:
            if self._client and self._client.is_connected:
                await self._client.stop_notify(config.NOTIFY_UUID)

                log_debug('Unsubscribed from notifications.')

                await self._client.disconnect()

                log_debug('Disconnected from Bluetooth device.')
        # pylint: disable=broad-exception-caught
        except Exception as e:
            log_error(e)
