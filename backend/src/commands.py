from uuid import uuid4

FOOTER        : bytes = b'\xC3\x69'
COMMAND_POWER : bytes = b'\x04\x02'
COMMAND_SHOW  : bytes = b'\x08\x02'


class Command:
    def __init__(self, command: bytes, payload: bytes):
        self.command = command
        self.payload = payload

    def to_bytes(self) -> bytes:
        return self.command + self.payload


class PowerCommand(Command):
    def __init__(self, on: bool):
        super().__init__(COMMAND_POWER, b'\x00\x01' if on else b'\x00\x00')


class GifCommand(Command):
    def __init__(self, time: int, data: bytes):
        super().__init__(COMMAND_SHOW, b'\x00\x00\x09\x01\x01\x0c\x01\x00\x1c\x06\x00\x00\x01\x00\x01\x00\x0d\x01\x00\x1d\x09\x00\x00\x00\x00\x20\x00\x20\x00\x00\x09\x01\x01\x0c\x01\x00\x0d\x01\x00\x0e\x01\x00\x14\x03\x01\x0d\x03\x11\x04\x00\x01\x00\x0a\x09\x01\x01\x0c\x01\x00\x0d\x01\x00\x0e\x01\x00\x12\x07\x01\x00\x00\x00\xc0\x03\x00\x13\x82' + len(data).to_bytes(2, 'little', signed=False) + data + b'\x35\x19\x00\x10\x00\x00\x00' + uuid4().bytes + (time & 0xFFFF).to_bytes(2, 'little', signed=False) + FOOTER)
