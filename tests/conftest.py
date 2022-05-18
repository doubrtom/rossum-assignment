# pylint: disable=invalid-name,unused-argument
from unittest.mock import MagicMock, mock_open

import pytest
from dramatiq import Worker
from dramatiq.brokers.stub import StubBroker
from flask_migrate import upgrade
from sqlalchemy.orm import close_all_sessions

from pdf_renderer import create_app, db, dramatiq
from pdf_renderer.models import RenderingPdfEvent
from . import test_constants
from .mocks import PdfFileReaderMock, PdfFileWriterMock


@pytest.fixture(name="flask_app")
def flask_app_fixture():
    """Create flask app for testing."""
    flask_app = create_app("testing")
    yield flask_app


@pytest.fixture()
def test_client(flask_app):
    """Create flask test client."""
    with flask_app.test_client() as testing_client:
        with flask_app.app_context():
            yield testing_client


@pytest.fixture(name="init_db")
def init_db_fixture(flask_app):
    """Init and clear DB for testing."""
    with flask_app.app_context():
        upgrade()
        yield
        db.session.commit()
        close_all_sessions()
        db.drop_all()
        db.engine.execute("DROP TABLE alembic_version")
        db.engine.execute("DROP TYPE IF EXISTS processingstatus")


@pytest.fixture()
def rendering_event(init_db) -> RenderingPdfEvent:
    """Create one PDF rendering event for testing."""
    event = RenderingPdfEvent(
        uuid=test_constants.EVENT_UUID, total_page_count=test_constants.PDF_PAGE_NUM
    )
    db.session.add(event)
    db.session.commit()
    return event


@pytest.fixture(name="stub_broker")
def stub_broker_fixture() -> StubBroker:
    """Create stub broker for testing."""
    broker: StubBroker = dramatiq.broker
    broker.emit_after("process_boot")
    yield broker
    broker.flush_all()
    broker.close()


@pytest.fixture()
def stub_worker(stub_broker) -> Worker:
    """Create stub worker for testing."""
    worker = Worker(stub_broker, worker_timeout=100)
    worker.start()
    yield worker
    worker.stop()


@pytest.fixture()
def mock_external_api_for_workers(mocker):
    """Mock all externals API for async workers running during PDF rendering.

    API mocked for:
    - builtins "open"
    - os: mkdir
    - PyPDF2: PdfFileReader, PdfFileWriter
    - pdf2image: convert_from_path
    - werkzeug: FileStorage (used when Flask got uploaded file)
    """
    file_save_mock = mocker.patch("werkzeug.datastructures.FileStorage.save")
    mocker.patch("os.mkdir")
    mocker.patch("uuid.uuid4", new=lambda: test_constants.EVENT_UUID)
    mocker.patch("pdf_renderer.commands.PdfFileReader", new=PdfFileReaderMock)
    mocker.patch("pdf_renderer.commands.PdfFileWriter", new=PdfFileWriterMock)
    convert_mock = mocker.patch("pdf_renderer.commands.convert_from_path")
    image_mock = MagicMock()
    convert_mock.return_value = [image_mock]
    open_mock = mock_open()
    mocker.patch("builtins.open", open_mock)
    return file_save_mock, image_mock
