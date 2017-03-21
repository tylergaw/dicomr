import os
from .dicomr import create_app

app = create_app(os.environ["APP_SETTINGS"])
