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
