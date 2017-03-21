"""
    Dicomr
    ======

    A web application for uploading and viewing DICOM images.
"""

from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app(config_object):
    app = Flask(__name__)
    app.config.from_object(config_object)
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)
    migrate = Migrate(app, db)

    from .records.views import records_app
    app.register_blueprint(records_app)

    @app.cli.command()
    def clear_records():
        from .records.models import Record
        Record.query.delete()
        db.session.commit()

    return app
