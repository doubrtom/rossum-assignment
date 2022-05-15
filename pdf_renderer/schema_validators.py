from marshmallow import ValidationError
from marshmallow.validate import Validator
from werkzeug.datastructures import FileStorage


class MimeTypeValidator(Validator):
    """Validate uploaded file for specified Mime Type."""

    def __init__(self, mime_type: str):
        """Init mime type validator.

        :param mime_type: Mime Type to validate for uploaded file
        """
        self.mime_type = mime_type

    def __call__(self, value: FileStorage, **kwargs) -> True:
        """Validate uploaded file for specified Mime Type."""
        if value.mimetype != self.mime_type:
            raise ValidationError("Invalid file type, you have to upload only PDF.")
        return True
