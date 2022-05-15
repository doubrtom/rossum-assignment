from . import ma, schema_validators


class InitPdfRenderingSchema(ma.Schema):
    """Schema to init new PDF rendering process."""

    pdf_file = ma.Raw(
        required=True,
        validate=schema_validators.MimeTypeValidator("application/pdf"),
        metadata={"type": "string", "format": "binary"},
    )


class RenderingPdfEventSchema(ma.Schema):
    """Schema for RenderingPdfEvent model."""

    class Meta:  # pylint: disable=missing-class-docstring  # noqa: D106
        fields = ("uuid", "status", "total_page_count", "processed_page_count")
