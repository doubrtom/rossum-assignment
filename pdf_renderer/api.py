from flask import (
    Blueprint,
)

api_bp = Blueprint("auth", __name__)


@api_bp.route("/rendering-pdf", methods=("POST",))
def render_pdf_create():
    """Start new rendering of pdf into png files."""
    return "create"


@api_bp.route("/rendering-pdf/<uuid:uuid>", methods=("GET",))
def render_pdf_detail():
    """Return info about pdf processing."""
    return "detail"
