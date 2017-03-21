"""
    dicomr.common.utils
    ======

    common tasks
"""

import dicom
import io
import os
import json
from PIL import Image
from flask import current_app
from .s3 import s3_create_object


def vr_lookup(vr=None):
    """
    Given a two-letter VR code, get the full name.

    :param vr: A valid VR code
    ftp://dicom.nema.org/medical/DICOM/2013/output/chtml/part05/sect_6.2.html
    """

    # Pulled from Mudicom:
    # https://github.com/neurosnap/mudicom/blob/master/mudicom/lookup.py
    definitions = {
        "AE": "Application Entity",
        "AS": "Age String",
        "AT": "Attribute Tag",
        "CS": "Code String",
        "DA": "Date",
        "DS": "Decimal String",
        "DT": "Date/Time",
        "FL": "Floating Point Single (4 bytes)",
        "FD": "Floating Point Double (8 bytes)",
        "IS": "Integer String",
        "LO": "Long String",
        "LT": "Long Text",
        "OB": "Other Byte",
        "OF": "Other Float",
        "OW": "Other Word",
        "PN": "Person Name",
        "SH": "Short String",
        "SL": "Signed Long",
        "SQ": "Sequence of Items",
        "SS": "Signed Short",
        "ST": "Short Text",
        "TM": "Time",
        "UI": "Unique Identifier",
        "UL": "Unsigned Long",
        "UN": "Unknown",
        "US": "Unsigned Short",
        "UT": "Unlimited Text"
    }

    if vr is not None:
        if vr.upper() in definitions:
            return definitions[vr.upper()]

    return None


def dict_from_data_elem(elem):
    """
    Create a dict of a dicom data element suitable for json serialization.

    :param elem: A pydicom DataElement
    """
    if type(elem.value) == dicom.sequence.Sequence:
        value = [list_from_dataset(e) for e in elem.value]
    else:
        value = repr(elem.value).strip("'")

    return {
        "tagName": elem.name,
        "tag": repr(elem.tag),
        "value": value,
        "vr": elem.VR,
        "vrDefinition": vr_lookup(elem.VR)
    }


def list_from_dataset(ds):
    """
    Create a list of a dicom dataset suitable for json serialization.

    :param ds: A pydicom DataSet
    """
    ignore = ['Pixel Data', 'File Meta Information Version']
    return [
        dict_from_data_elem(elem)
        for elem in ds
        if elem.name not in ignore
    ]


def image_from_dataset(dataset):
    """
    Create an image from a DICOM file using Pillow.

    :param file: A DICOM file
    """

    if ("PixelData" not in dataset):
        raise TypeError("""This DICOM image does not have pixel data. You can \
        view metadata about it, but you can't view the image.""")

    img = None
    size = (512, 512)

    if 'WindowWidth' in dataset and 'WindowCenter' in dataset:
        img = Image.fromarray(dataset.pixel_array).convert("L")
        img = img.resize(size)
    else:
        mode = "L"
        img = Image.frombuffer(
            mode, size, dataset.PixelData, "raw", mode, 0, 1)

    return img


def str_from_image(img, img_format="PNG"):
    """
    Using BytesIO convert a PIL image to a string suitable for writing to file.
    :param img: A PIL image.
    """
    img_str = io.BytesIO()
    img.save(img_str, img_format)
    img_str.seek(0)
    return img_str


def save_images(filename, img):
    """
    Saves a full size and a thumb image to the configured uploaded directory

    :param filename: The name of the file.
    :param img: A PIL.Image
    """

    new_filename = "{}.png".format(filename)
    thumb = img.resize((100, 100))
    thumb_name = "{}{}.png".format(
        filename, current_app.config["THUMBNAIL_PREFIX"])

    if current_app.config["USE_S3"]:
        headers = {"Content-Type": "image/png"}
        full_img_str = str_from_image(img)
        s3_create_object(new_filename, full_img_str.getvalue(), headers)
        full_img_str.close()

        thumb_img_str = str_from_image(thumb)
        s3_create_object(thumb_name, thumb_img_str.getvalue(), headers)
        full_img_str.close()
    else:
        upload_path = os.path.join(
            current_app.root_path, current_app.config["UPLOAD_FOLDER"])
        img.save(os.path.join(upload_path, new_filename), "PNG")
        thumb.save(os.path.join(upload_path, thumb_name), "PNG")

    return new_filename


def where(key):
    """
    HOF. Create lookup functions for finding a dict in a list by the given
    value of a key.

    :usage: where_foo = where("foo")
            where_foo(my_dict, "bar")

            You can also use it without creating the var:
            where("foo")(my_dict, "bar")
    """
    def f(d, val):
        return next((i for i in d if i[key] == val), None)
    return f
