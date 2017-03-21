import dicom
import json
import os
from flask import current_app
from werkzeug.utils import secure_filename
from dicomr.common.utils import (
    list_from_dataset,
    save_images,
    image_from_dataset
)
from dicomr.dicomr import db
from .models import Record


def process_upload(files):
    """
    Attempt to read one or more DICOM files. Extract metadata. Create and save
    preview image(s). Persist Record to DB.

    TODO: Save original DICOM.
    TODO: This function does too much.

    :param files: A dict of FileStorage objects from a form or ajax post.
    """
    records = []
    errors = []

    # Filter out any non-file objects
    valid_files = [
        file
        for file in files
        if file.filename
    ]

    for file in valid_files:
        processable = True
        filename = secure_filename(file.filename)

        try:
            ds = dicom.read_file(file)
            study_uid = ds.StudyInstanceUID
        except dicom.errors.InvalidDicomError:
            processable = False
            pass

        if processable:
            new_filename = None
            dicom_data = list_from_dataset(ds)

            try:
                new_filename = save_images(filename, image_from_dataset(ds))

            except NotImplementedError as err:
                error_msg = """You can view the metadata for this DICOM, but \
                we're unable to render it as an image. We don't know how to \
                work with the compression format yet."""
                pass
            except TypeError as err:
                error_msg = """You can view the metadata for this DICOM, but \
                we're unable to render it as an image. It's possible its  \
                pixel data is formatted in a way we don't understand yet."""
                pass

            record = Record(
                study_uid,
                new_filename,
                filename,
                json.dumps(dicom_data)
            )

            db.session.add(record)
            db.session.commit()

            records.append({
                "newFilename": new_filename,
                "id": record.id,
                "dicomData": dicom_data,
                "studyUid": study_uid
            })
        else:
            errors.append({
                "error": True,
                "filename": filename,
                "errMessage": """There was an error reading the file. Make \
                sure it's a valid DICOM file."""
            })

    return {
        "records": records,
        "errors": errors
    }
