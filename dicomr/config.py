import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DEBUG = False
    TESTING = False
    LOCAL = False
    CSRF_ENABLED = True
    SECRET_KEY = "secrets-for-the-secrets-god"
    SQLALCHEMY_DATABASE_URI = os.environ["DATABASE_URL"]
    THUMBNAIL_PREFIX = "-thumb"
    AWS_ACCESS_KEY_ID = os.environ["AWS_ACCESS_KEY_ID"]
    AWS_SECRET_ACCESS_KEY = os.environ["AWS_SECRET_ACCESS_KEY"]
    AWS_S3_BUCKET = os.environ["AWS_S3_BUCKET"]
    UPLOAD_FOLDER = "https://s3.amazonaws.com/{}".format(
        os.environ["AWS_S3_BUCKET"])
    USE_S3 = True


class Prod(Config):
    DEBUG = False
    USE_S3 = True


class Local(Config):
    TEMPLATES_AUTO_RELOAD = True
    LOCAL = True
    DEBUG = True


class Test(Config):
    TESTING = True
