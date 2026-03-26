from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    MAC_ADDRESS     : str   = 'E0:6E:41:18:56:E9'
    WRITE_UUID      : str   = '49535343-6daa-4d02-abf6-19569aca69fe'
    NOTIFY_UUID     : str   = '49535343-1e4d-4bd9-ba61-23c647249616'
    MAX_PACKET_SIZE : int   = 192
    WRITE_DELAY     : float = 0.1
    RECONNECT_DELAY : int   = 5
    DISPLAY_WIDTH   : int   = 32
    DISPLAY_HEIGHT  : int   = 32
    LATITUDE        : float = 51.365479
    LONGITUDE       : float = 0.211968
    TIMEZONE        : str   = 'Europe/London'

    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')
