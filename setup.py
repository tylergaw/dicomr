from setuptools import setup

setup(
    name="dicomr",
    version="1.0.0",
    description="A web application for uploading and viewing DICOM images.",
    author="Tyler Gaw",
    author_email="me@tylergaw.com",
    packages=["dicomr"],
    include_package_data=True,
    install_requires=[
        "boto==2.46.1",
        "flask==0.12",
        "Flask-Migrate==2.0.3",
        "Flask-SQLAlchemy===2.2",
        "gunicorn==19.7.0",
        "numpy==1.12.1",
        "pillow==4.0.0",
        "psycopg2==2.7.1",
        "pydicom==0.9.9"
    ],
)
