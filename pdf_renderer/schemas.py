from marshmallow_enum import EnumField

from . import ma, schema_validators
from .models import RenderingPdfEvent
from .enums import ProcessingStatus


class InitPdfRenderingSchema(ma.Schema):
    """Schema to init new PDF rendering process."""

    pdf_file = ma.Raw(
        required=True,
        validate=schema_validators.MimeTypeValidator("application/pdf"),
        metadata={"type": "string", "format": "binary"},
    )


class RenderingPdfEventSchema(ma.SQLAlchemyAutoSchema):
    """Schema for RenderingPdfEvent model."""

    status = EnumField(ProcessingStatus, by_value=True)

    class Meta:  # pylint: disable=missing-class-docstring  # noqa: D106
        model = RenderingPdfEvent
        fields = ("uuid", "status", "total_page_count", "processed_page_count")
