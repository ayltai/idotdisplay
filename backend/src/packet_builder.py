from .commands import Command

HEADER        : bytes = b'\xAA\x55\xFF\xFF'
COMMAND_TYPE  : bytes = b'\xC1\x02'


class PacketBuilder:
    sequence_number: int = 0

    def next_sequence(self) -> int:
        self.sequence_number = (self.sequence_number + 1) & 0xFFFF
        return self.sequence_number

    def build_packet(self, command: Command):
        sequence_number = self.next_sequence().to_bytes(2, 'little', signed=False)
        command_bytes   = command.to_bytes()
        data_length     = (2 + 2 + len(command_bytes) + 2).to_bytes(2, 'little', signed=False)
        packet          = HEADER + data_length + sequence_number + COMMAND_TYPE + command_bytes
        checksum        = self.checksum(packet).to_bytes(2, 'little', signed=False)

        return packet + checksum

    @staticmethod
    def checksum(data: bytes) -> int:
        return sum(data) & 0xFFFF
