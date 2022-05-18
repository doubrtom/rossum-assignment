# pylint: disable=invalid-name,unused-argument
import os
from http import HTTPStatus

from flask import Response

from .. import test_constants


def test_uuid_not_in_db_should_return_not_found(test_client, rendering_event):
    """For not-existing event we should go 404."""
    url = f"/rendering-pdf/{test_constants.ANY_UUID}/1.png"

    response = test_client.get(url)

    assert response.status_code == 404
    expected_msg = (
        "Rendering PDF event with UUID=b8a8d17f-18c0-4e2c-8a62-65591fb6c57a not found."
    )
    assert response.json["error_message"] == expected_msg


def test_invalid_page_num_should_return_not_found(test_client, rendering_event):
    """For not-existing page number we should go 404."""
    url = f"/rendering-pdf/{rendering_event.uuid}/123.png"

    response = test_client.get(url)

    assert response.status_code == 404
    expected_msg = (
        "The requested URL was not found on the server. "
        "If you entered the URL manually please check your spelling and try again."
    )
    assert response.json["error_message"] == expected_msg


def test_server_should_send_file_from_correct_location(
    test_client, mocker, rendering_event
):
    """App should send rendered image from correct location."""
    send_mock = mocker.patch("pdf_renderer.api.send_from_directory")
    send_mock.return_value = Response(status=HTTPStatus.OK)
    url = f"/rendering-pdf/{rendering_event.uuid}/1.png"

    response = test_client.get(url)

    correct_folder = os.path.join("data", str(rendering_event.uuid))
    assert response.status_code == HTTPStatus.OK
    assert send_mock.call_args.args[0].endswith(correct_folder)
    assert send_mock.call_args.args[1] == "1.png"
