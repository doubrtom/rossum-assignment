import os

from . import db
from .models import RenderingPdfEvent
from .types import PdfFileData


def _save_file(rendering_event: RenderingPdfEvent, data: PdfFileData) -> None:
    """Create event folder for uploaded file and save file there."""
    event_folder = rendering_event.event_folder
    if not os.path.exists(event_folder):
        os.mkdir(event_folder)
    file_path = os.path.join(event_folder, "input.pdf")
    data["pdf_file"].save(file_path)


def start_pdf_processing(data: PdfFileData) -> RenderingPdfEvent:
    """Start processing uploaded PDF file."""
    rendering_event = RenderingPdfEvent()
    db.session.add(rendering_event)
    db.session.commit()
    _save_file(rendering_event, data)

    # here I should send message to work

    return rendering_event
