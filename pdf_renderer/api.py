from uuid import UUID
from http import HTTPStatus

from flask import Blueprint, request, send_from_directory
from marshmallow.validate import ValidationError

from . import schemas, commands, types
from .models import RenderingPdfEvent

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
    init_schema = schemas.InitPdfRenderingSchema()
    result: types.PdfFileData = init_schema.load(request.files)
    rendering_event: RenderingPdfEvent = commands.start_pdf_processing(result)
    event_schema = schemas.RenderingPdfEventSchema()
    return event_schema.dump(rendering_event), HTTPStatus.CREATED


@api_bp.route("/rendering-pdf/<uuid:event_uuid>", methods=("GET",))
def rendering_pdf_detail(event_uuid: UUID):
    """Return info about pdf processing."""
    rendering_event: RenderingPdfEvent = RenderingPdfEvent.query.get(event_uuid)
    schema = schemas.RenderingPdfEventSchema()
    return schema.dump(rendering_event)


@api_bp.route("/rendering-pdf/<uuid:event_uuid>/<int:page_num>.png", methods=("GET",))
def rendering_pdf_get_image(event_uuid: UUID, page_num: int):
    """Return rendered PNG image for selected PDF page.

    ! This should normally do NGINX (or other web server).
    """
    rendering_event: RenderingPdfEvent = RenderingPdfEvent.query.get(event_uuid)
    return send_from_directory(rendering_event.event_folder, f"{page_num}.png")
