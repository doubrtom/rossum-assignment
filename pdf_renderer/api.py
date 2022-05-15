from flask import Blueprint, request
from marshmallow.validate import ValidationError

from . import schemas, commands, types


api_bp = Blueprint("auth", __name__)


@api_bp.errorhandler(ValidationError)
def validation_error_handler(err):
    """Convert validation errors into 400 response."""
    # todo(doubravskytomas): logger
    # todo(doubravskytomas): improve error messages
    response_data = {"errors": err.messages, "status": "Validation error"}
    return response_data, 400


@api_bp.route("/rendering-pdf", methods=("POST",))
def rendering_pdf_create():
    """Start new rendering of pdf into png files."""
    schema = schemas.InitPdfRenderingSchema()
    result: types.PdfFileData = schema.load(request.files)
    rendering_event = commands.start_pdf_processing(result)
    return "create - " + str(rendering_event.uuid)


@api_bp.route("/rendering-pdf/<uuid:uuid>", methods=("GET",))
def rendering_pdf_detail():
    """Return info about pdf processing."""
    return "detail"
