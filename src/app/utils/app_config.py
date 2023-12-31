import os

description = """
This API is designed to control and monitor irrigation devices around the house

## Control 
You can control irrigation devices individually or in a group.

## Monitor
You can access the information about the latest status of irrigation devices and their corresponding plants.
"""

APP_PARAMETER_CONFIGS = {
    "title": "Smart Home Irrigation System",
    "summary": "",
    "description": description,
    "version": os.getenv("VERSION"),
}