# pylint: disable=invalid-name,unused-argument,missing-function-docstring,no-self-use
from . import test_constants


class MediaBox:
    """Mock class for mediaBox of PDF page."""

    def getWidth(self) -> int:
        return 600

    def getHeight(self) -> int:
        return 800


class PageMock:
    """Mock class for one PDF page."""

    def __init__(self, *args, **kwargs):
        self.mediaBox = MediaBox()


class PdfFileReaderMock:
    """Mock class for PyPDF2.PdfFileReader."""

    def __init__(self, *args, **kwargs):
        self.numPages = test_constants.PDF_PAGE_NUM
        self.pages = [PageMock() for __ in range(test_constants.PDF_PAGE_NUM)]


class PdfFileWriterMock:
    """Mock class for PyPDF2.PdfFileWriter."""

    def __init__(self, *args, **kwargs):
        self.pages = []
        self.files = []

    def addPage(self, page):
        self.pages.append(page)

    def write(self, file):
        self.files.append(file)
