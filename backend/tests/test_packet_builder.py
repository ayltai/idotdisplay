from src.commands import PowerCommand
from src.packet_builder import PacketBuilder


def test_checksum():
    data              = b'\xAA\x55\xFF\xFF\x0A\x00\x0D\x00\xC1\x02\x04\x02\x00\x01'
    expected_checksum = sum(data) & 0xFFFF

    assert PacketBuilder.checksum(data) == expected_checksum

def test_build_packet():
    command = PowerCommand(on=True)
    builder = PacketBuilder()
    packet  = builder.build_packet(command)

    assert packet.startswith(b'\xAA\x55\xFF\xFF\x0A\x00\x01\x00\xC1\x02\x04\x02\x00\x01')
    assert packet.endswith(b'\xD2\x03')
