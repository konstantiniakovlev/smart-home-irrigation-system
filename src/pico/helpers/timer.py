import datetime

DATETIME_STR_FORMAT = "%Y-%m-%d %H:%M:%S"
VALID_TIME_TYPES = [datetime.datetime, datetime.date, str]


class Timer:

    def __init__(self):
        self.time_last_watered = None

    def set_time_last_watered(self, updated_time=None):

        if updated_time not in VALID_TIME_TYPES and updated_time is not None:
            raise ValueError("Invalid time provided.")

        if updated_time is None:
            self.time_last_watered = datetime.datetime.now()\
                .strftime(DATETIME_STR_FORMAT)

        else:
            self.time_last_watered = self._format_time(updated_time)

    def _format_time(self, dt_obj):
        if type(dt_obj) in [str]:
            self._check_iso_format(dt_obj)
            return datetime.datetime.fromisoformat(dt_obj)\
                .strftime(DATETIME_STR_FORMAT)

        if type(dt_obj) in [datetime.datetime, datetime.date]:
            return dt_obj.strftime(DATETIME_STR_FORMAT)

        else:
            raise TypeError(f"Provided time object has incorrect object type: "
                            f"{type(dt_obj)}")

    @staticmethod
    def _check_iso_format(datetime_str):
        try:
            datetime.datetime.fromisoformat(datetime_str)
        except ValueError:
            raise ValueError(
                "Incorrect data format.\n"
                "Correct format should be YYYY-MM-DD hh:mm:ss"
            )
