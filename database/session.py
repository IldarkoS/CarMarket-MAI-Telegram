from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config.config import Config, load_config

config: Config = load_config()

engine = create_engine(
    url=f"postgresql:"
        f"//{config.database.user}"
        f":{config.database.password}"
        f"@{config.database.host}"
        f":{config.database.port}"
        f"/{config.database.name}",
    echo=False
)

Session = sessionmaker(bind=engine)
