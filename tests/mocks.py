# pylint: disable=invalid-name,unused-argument,missing-function-docstring
import io

from . import test_constants


class PdfFileReaderMock:
    """Mock class for PyPDF2.PdfFileReader."""

    def __init__(self, *args, **kwargs):
        self.numPages = test_constants.PDF_PAGE_NUM
        self.pages = test_constants.PDF_PAGE_NUM * [io.BytesIO(b"page data")]


class PdfFileWriterMock:
    """Mock class for PyPDF2.PdfFileWriter."""

    def __init__(self, *args, **kwargs):
        self.pages = []

    def addPage(self, page):
        self.pages.append(page)

    def write(self, file):
        pass
