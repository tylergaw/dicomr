import json
from flask import (
    abort,
    Blueprint,
    current_app,
    render_template,
    redirect,
    request,
    jsonify,
    url_for
)
from .utils import process_upload
from .models import Record
from dicomr.common.utils import where

records_app = Blueprint('records_app', __name__)


@records_app.context_processor
def context_processors():
    upload_path = "{}".format(current_app.config["UPLOAD_FOLDER"])

    def record_image_thumb(filename=None):
        thumb_name = list(filename)
        thumb_name[-4] = "{}.".format(current_app.config["THUMBNAIL_PREFIX"])
        return "".join(thumb_name)

    return dict(
        record_image_thumb=record_image_thumb,
        upload_path=upload_path
    )


@records_app.errorhandler(404)
def page_not_found(err):
    return render_template("404.html"), 404


@records_app.route("/")
def index():
    records = Record.query.order_by(Record.created_at.asc()).all()

    records_for_view = []
    where_tag = where("tag")
    for record in records:
        # Creates a clone of the Record dict.
        r = dict(record.__dict__)
        r_json = json.loads(r["dicom_data"])

        r["manufacturer"] = where_tag(r_json, "(0008, 0070)")
        r["modality"] = where_tag(r_json, "(0008, 0060)")
        r["slice_thickness"] = where_tag(r_json, "(0018, 0050)")
        records_for_view.append(r)

    return render_template("index.html", records=records_for_view)


@records_app.route("/records/<int:record_id>")
def record(record_id):
    record = Record.query.filter_by(id=record_id).first_or_404()

    # Display the dicom metadata as JSON. Mostly for dev purposes.
    # e.g; /records/60?json=1
    if request.args.get('json'):
        return jsonify(json.loads(record.dicom_data))

    return render_template(
        "record.html",
        dicom_name=record.dicom_name,
        img_name=record.image_name,
        dicom_data=json.loads(record.dicom_data)
    )


@records_app.route("/upload", methods=["POST"])
def upload():
    upload_results = process_upload(request.files.getlist('files'))

    if request.is_xhr:
        return jsonify(result=upload_results)
    else:
        return redirect(url_for('records_app.index'))
