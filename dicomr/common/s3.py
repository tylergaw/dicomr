import boto
import os
from boto.s3.key import Key

# TODO: Might be better to using current_app.config, but ran into trouble
# with that late, so let it go for now.
AWS_KEY = os.environ["AWS_ACCESS_KEY_ID"]
AWS_SECRET = os.environ["AWS_SECRET_ACCESS_KEY"]
BUCKET = os.environ["AWS_S3_BUCKET"]

s3_conn = boto.connect_s3(AWS_KEY, AWS_SECRET)
bucket = s3_conn.get_bucket(BUCKET)


def s3_create_object(name, contents, headers=None):
    obj = Key(bucket)
    obj.key = name
    obj.set_contents_from_string(contents, headers)
