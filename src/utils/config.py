import os


def get_config_params(name="smart-home-postgres"):
    if name == "smart-home-postgres":
        config_params = {
            "host": str(os.getenv("POSTGRES_HOST")),
            "port": str(os.getenv("POSTGRES_PORT")),
            "user": str(os.getenv("POSTGRES_USER")),
            "password": str(os.getenv("POSTGRES_PASSWORD")),
            "database": str(os.getenv("POSTGRES_DB")),
        }

    elif name == "smart-home-timescaledb":
        config_params = {
            "host": str(os.getenv("TIMESCALE_HOST")),
            "port": str(os.getenv("TIMESCALE_PORT")),
            "user": str(os.getenv("TIMESCALE_USER")),
            "password": str(os.getenv("TIMESCALE_PASSWORD")),
            "database": str(os.getenv("TIMESCALE_DB")),
        }

    return config_params
