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

    @property
    def pdf_file_path(self) -> str:
        """Return absolute path to uploaded PDF file.

        Uploaded file is saved in the event_folder with name "input.pdf"
        """
        return os.path.join(self.event_folder, "input.pdf")

    def get_pdf_page_path(self, page_number: int) -> str:
        """Return absolute path to one paged PDF.

        Uploaded PDF file is split by pages and each page is saved
        into event dir.
        """
        return os.path.join(self.event_folder, f"{page_number}.pdf")

    def get_image_path(self, page_number: int) -> str:
        """Return absolute path to one rendered page into PNG image.

        Rendered images are saved into event dir.
        """
        return os.path.join(self.event_folder, f"{page_number}.png")

    def is_processing_done(self) -> bool:
        """Return if all pages was processed.

        ! Refresh data from DB, when calling this function in worker
        """
        return self.processed_page_count == self.total_page_count
