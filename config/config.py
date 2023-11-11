from dataclasses import dataclass
from environs import Env


@dataclass
class TgBot:
    token: str


@dataclass
class Database:
    host: str
    port: str
    user: str
    password: str
    name: str


@dataclass
class Config:
    tg_bot: TgBot
    database: Database


def load_config() -> Config:

    env: Env = Env()
    env.read_env()

    return Config(
        tg_bot=TgBot(
            token=env('BOT_TOKEN')
        ),
        database=Database(
            host=env('DATABASE_HOST'),
            port=env('DATABASE_PORT'),
            user=env('DATABASE_USER'),
            password=env('DATABASE_PASSWORD'),
            name=env('DATABASE_NAME')
        )
    )
