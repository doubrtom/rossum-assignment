# pylint: disable=invalid-name,unused-argument
import io
import os

from dramatiq import Message
from dramatiq.brokers.stub import StubBroker

from pdf_renderer.commands import split_pdf
from pdf_renderer.enums import ProcessingStatus
from pdf_renderer.models import RenderingPdfEvent
from .. import test_constants
from ..mocks import PdfFileReaderMock


def test_upload_not_pdf_should_return_validation_errors(test_client):
    """Allowed files for upload are only PDF documents."""
    file_name = "my_file.txt"
    data = {"pdf_file": (io.BytesIO(b"testing data"), file_name)}

    response = test_client.post("/rendering-pdf", data=data)

    assert response.status_code == 400
    assert response.json["error_message"] == "Validation error"
    first_err_msg = response.json["errors"]["pdf_file"][0]
    assert first_err_msg == "Invalid file type, you have to upload only PDF."


def test_upload_pdf_should_create_new_pdf_rendering_event(test_client, init_db, mocker):
    """For PDF i should get rendering event info."""
    mocker.patch("werkzeug.datastructures.FileStorage.save")
    mocker.patch("os.mkdir")
    mocker.patch("uuid.uuid4", new=lambda: test_constants.EVENT_UUID)
    mocker.patch("pdf_renderer.commands.PdfFileReader", new=PdfFileReaderMock)
    file_name = "my_file.pdf"
    data = {"pdf_file": (io.BytesIO(b"testing data"), file_name)}

    response = test_client.post("/rendering-pdf", data=data)

    assert response.status_code == 201
    response_data = response.json
    assert response_data["status"] == ProcessingStatus.NEW.value
    assert response_data["total_page_count"] == test_constants.PDF_PAGE_NUM
    assert response_data["processed_page_count"] == 0
    assert response_data["uuid"] == str(test_constants.EVENT_UUID)
    assert RenderingPdfEvent.query.count() == 1


def test_uploaded_pdf_should_be_saved_into_event_folder(test_client, init_db, mocker):
    """PDF should be saved into correct folder and with correct name."""
    file_save = mocker.patch("werkzeug.datastructures.FileStorage.save")
    mocker.patch("os.mkdir")
    mocker.patch("uuid.uuid4", new=lambda: test_constants.EVENT_UUID)
    mocker.patch("pdf_renderer.commands.PdfFileReader", new=PdfFileReaderMock)
    file_name = "my_file.pdf"
    data = {"pdf_file": (io.BytesIO(b"testing data"), file_name)}

    test_client.post("/rendering-pdf", data=data)

    correct_path = os.path.join("data", str(test_constants.EVENT_UUID), "input.pdf")
    assert file_save.call_args.args[0].endswith(correct_path)


def test_valid_request_should_enqueue_split_pdf_task(
    test_client,
    init_db,
    mock_external_api_for_workers,
    stub_broker: StubBroker,
):
    """On valid request server should send async task split_pdf."""
    file_name = "my_file.pdf"
    data = {"pdf_file": (io.BytesIO(b"testing data"), file_name)}

    test_client.post("/rendering-pdf", data=data)

    enqueued_message_data = stub_broker.queues[split_pdf.queue_name].get(timeout=1)
    message: Message = Message.decode(enqueued_message_data)
    assert message.actor_name == "split_pdf"
    assert message.args == (str(test_constants.EVENT_UUID),)


def test_valid_request_should_save_all_rendered_images_into_event_folder(
    test_client,
    init_db,
    mock_external_api_for_workers,
    stub_broker: StubBroker,
    stub_worker,
):
    """
    On valid request server should run async tasks
    and save all rendered images into event folder.
    """
    __, image_mock = mock_external_api_for_workers
    file_name = "my_file.pdf"
    data = {"pdf_file": (io.BytesIO(b"testing data"), file_name)}

    test_client.post("/rendering-pdf", data=data)
    stub_broker.join(split_pdf.queue_name)
    stub_worker.join()

    assert image_mock.save.call_count == test_constants.PDF_PAGE_NUM
    saved_images_paths = sorted(
        [call.args[0] for call in image_mock.save.call_args_list]
    )
    for page_num in range(1, test_constants.PDF_PAGE_NUM + 1):
        expected_image_path = os.path.join(
            "data", str(test_constants.EVENT_UUID), f"{page_num}.png"
        )
        saved_images_paths[page_num - 1].endswith(expected_image_path)


def test_valid_request_should_process_all_tasks_and_set_rendering_event_done(
    test_client,
    init_db,
    mock_external_api_for_workers,
    stub_broker: StubBroker,
    stub_worker,
):
    """
    On valid request server should send async tasks,
    process uploaded PDF and set event done, when all tasks are done.
    """
    file_name = "my_file.pdf"
    data = {"pdf_file": (io.BytesIO(b"testing data"), file_name)}

    test_client.post("/rendering-pdf", data=data)
    stub_broker.join(split_pdf.queue_name)
    stub_worker.join()

    rendering_event = RenderingPdfEvent.query.get(test_constants.EVENT_UUID)
    assert rendering_event.status == ProcessingStatus.DONE
