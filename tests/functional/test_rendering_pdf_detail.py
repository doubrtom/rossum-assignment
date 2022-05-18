# pylint: disable=invalid-name,unused-argument
from .. import test_constants


def test_uuid_not_in_db_should_return_not_found(test_client, rendering_event):
    """For not-existing event we should get 404."""
    url = f"/rendering-pdf/{test_constants.ANY_UUID}"

    response = test_client.get(url)

    assert response.status_code == 404
    expected_msg = (
        "Rendering PDF event with UUID=b8a8d17f-18c0-4e2c-8a62-65591fb6c57a not found."
    )
    assert response.json["error_message"] == expected_msg


def test_invalid_uuid_should_return_not_found(test_client, rendering_event):
    """For invalid UUID in path we should get 404."""
    url = "/rendering-pdf/this-is-not-uuid"

    response = test_client.get(url)

    assert response.status_code == 404
    expected_msg = (
        "The requested URL was not found on the server. "
        "If you entered the URL manually please check your spelling and try again."
    )
    assert response.json["error_message"] == expected_msg


def test_valid_uuid_should_return_json_with_detail(test_client, rendering_event):
    """For valid should return serialized RenderingPdfEvent model."""
    url = f"/rendering-pdf/{rendering_event.uuid}"

    response = test_client.get(url)

    assert response.status_code == 200
    r_data = response.json
    assert r_data["uuid"] == str(rendering_event.uuid)
    assert r_data["total_page_count"] == rendering_event.total_page_count
    assert r_data["processed_page_count"] == rendering_event.processed_page_count
    assert r_data["status"] == rendering_event.status.value
