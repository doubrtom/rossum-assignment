import uuid
import datetime
import os

from sqlalchemy.dialects.postgresql import UUID
from flask import current_app

from . import db
from .enums import ProcessingStatus


class RenderingPdfEvent(db.Model):
    """Event to hold information about rendering PDF into PNG images.

    :cvar uuid: UUID of event
    :cvar status: Status in which phase event currently is
    :cvar total_page_count: Number of pages in rendered PDF
    :cvar processed_page_count: Number of pages already processed
    :cvar created_at: Datetime when event was created
    """

    uuid = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    status = db.Column(db.Enum(ProcessingStatus), default=ProcessingStatus.NEW)
    total_page_count = db.Column(db.Integer, nullable=True, default=None)
    processed_page_count = db.Column(db.Integer, nullable=False, default=0)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    @property
    def event_folder(self) -> str:
        """Return absolute path to event folder.

        Event folder is folder where are saved all data for rendering PDF event.
        It is inside DATA_DIR see config to change path.
        """
        return os.path.join(current_app.config["DATA_DIR"], str(self.uuid))
