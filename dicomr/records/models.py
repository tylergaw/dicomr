from datetime import datetime
from dicomr.dicomr import db
from sqlalchemy.dialects.postgresql import JSONB


class Record(db.Model):
    __tablename__ = 'records'

    id = db.Column(db.Integer, primary_key=True)
    study_uid = db.Column(db.String())
    image_name = db.Column(db.String())
    dicom_name = db.Column(db.String())
    dicom_data = db.Column(JSONB)
    created_at = db.Column(db.Date, default=datetime.now)
    updated_at = db.Column(db.Date, onupdate=datetime.now)

    def __init__(
        self,
        study_uid,
        image_name,
        dicom_name,
        dicom_data
    ):
        self.study_uid = study_uid
        self.image_name = image_name
        self.dicom_name = dicom_name
        self.dicom_data = dicom_data

    def __repr__(self):
        return "<id {}".format(self.id)
