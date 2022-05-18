from setuptools import setup, find_packages

setup(
    name="pdf_renderer",
    version="1.0",
    description="PDF Rendering Application - Rossum assignment",
    author="Tomas Doubravsky",
    author_email="doubravskytomas@gmail.com",
    url="https://github.com/doubrtom/rossum-assignment",
    packages=find_packages(include=["pdf_renderer"]),
    install_requires=[
        "flask",
        "sqlalchemy",
        "flask-sqlalchemy",
        "dramatiq[rabbitmq,redis,watch]",
        "flask-migrate",
        "marshmallow",
        "flask-marshmallow",
        "marshmallow-sqlalchemy",
        "flasgger",
        "psycopg2",
        "pypdf2",
        "flask-dramatiq",
        "pika",
        "pdf2image",
        "marshmallow-enum",
    ],
)
