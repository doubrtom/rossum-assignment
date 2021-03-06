import os
import uuid

from PyPDF2 import PdfFileReader, PdfFileWriter
from pdf2image import convert_from_path
from flask import current_app

from . import db, dramatiq
from .models import RenderingPdfEvent
from .types import PdfFileData
from .enums import ProcessingStatus
from .utils import get_convert_size_from_pdf_dimensions


def _save_file(rendering_event: RenderingPdfEvent, data: PdfFileData) -> None:
    """Create event folder for uploaded file and save file there."""
    event_folder = rendering_event.event_folder
    if not os.path.exists(event_folder):
        os.mkdir(event_folder)
    data["pdf_file"].save(rendering_event.pdf_file_path)


def start_pdf_processing(data: PdfFileData) -> RenderingPdfEvent:
    """Start processing of uploaded PDF document."""
    rendering_event = RenderingPdfEvent(uuid=uuid.uuid4())
    _save_file(rendering_event, data)
    pdf_reader = PdfFileReader(rendering_event.pdf_file_path)
    rendering_event.total_page_count = pdf_reader.numPages
    db.session.add(rendering_event)
    db.session.commit()

    split_pdf.send(str(rendering_event.uuid))

    return rendering_event


@dramatiq.actor(priority=0)
def split_pdf(event_uuid: str):
    """Split PDF by pages and run rendering for each page.

    Each PDF page is saved as individual PDF file and send
    for rendering into next dramatiq worker.
    """
    event: RenderingPdfEvent = RenderingPdfEvent.query.get(event_uuid)
    event.status = ProcessingStatus.PROCESSING
    db.session.commit()

    pdf_reader = PdfFileReader(event.pdf_file_path)
    for page_num, page in enumerate(pdf_reader.pages, start=1):
        pdf_writer = PdfFileWriter()
        pdf_writer.addPage(page)
        with open(event.get_pdf_page_path(page_num), "wb") as file:
            pdf_writer.write(file)
        render_pdf_page.send(
            event_uuid,
            page_num,
            int(page.mediaBox.getWidth()),  # This can be Double convert to int
            int(page.mediaBox.getHeight()),  # This can be Double convert to int
        )


@dramatiq.actor(priority=50)
def render_pdf_page(event_uuid: str, page: int, page_width: int, page_height: int):
    """Take PDF with single page and render it into PNG file."""
    event: RenderingPdfEvent = RenderingPdfEvent.query.get(event_uuid)

    convert_size = get_convert_size_from_pdf_dimensions(
        page_width,
        page_height,
        current_app.config["IMAGE_MAX_WIDTH"],
        current_app.config["IMAGE_MAX_HEIGHT"],
    )
    images = convert_from_path(
        event.get_pdf_page_path(page), fmt="png", single_file=True, size=convert_size
    )
    for image in images:
        image.save(event.get_image_path(page), "PNG")

    # Use column to increment in DB:
    event.processed_page_count = RenderingPdfEvent.processed_page_count + 1
    db.session.commit()

    # This can be improved by dramatiq.Group and add_completion_callback
    db.session.refresh(event)
    if event.is_processing_done():
        event.status = ProcessingStatus.DONE
        db.session.commit()
