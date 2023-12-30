import psycopg2
from psycopg2 import extras
from utils import config


class DataBase:

    def __init__(
            self,
            name="smart-home-postgres",
    ):
        self.name = name
        self.config_params = self._get_config_params()
        self.connection, self.cursor = self._connect()

    def execute(self, query, fetch, commit=False):

        self.cursor.execute(query)
        self.connection.commit() if commit else None
        return self._format_response(self.cursor.fetchall()) if fetch else None

    def close(self):
        self.cursor.close()
        self.connection.close()

    def _get_config_params(self):
        if self.name == "smart-home-postgres":
            return config.POSTGRES_DB_CONfIGS

        if self.name == "smart-home-timescaledb":
            return config.TIMESCALE_DB_CONFIGS

    def _connect(self):
        try:
            connection = psycopg2.connect(**self.config_params)
        except psycopg2.OperationalError as e:
            raise ConnectionError(e)

        cursor = connection.cursor(cursor_factory=extras.RealDictCursor)
        return connection, cursor

    @staticmethod
    def _format_response(response):
        return [dict(row) for row in response]
