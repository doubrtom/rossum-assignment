import pytest

from pdf_renderer.utils import get_convert_size_from_pdf_dimensions


@pytest.mark.parametrize(
    "width, height, expected",
    [
        (4, 400, (None, 1600)),  # Fit by height, up-scaling
        (400, 4, (1200, None)),  # Fit by width, up-scaling
        (4000, 40_000, (None, 1600)),  # Fit by height, down-scaling
        (40_000, 4000, (1200, None)),  # Fit by width, down-scaling
    ],
)
def test_get_convert_size_from_pdf_dimensions_should_return_correct_values(
    width,
    height,
    expected,
):
    """Test function return expected ConvertSize."""
    max_width = 1200
    max_height = 1600

    convert_size = get_convert_size_from_pdf_dimensions(
        width, height, max_width, max_height
    )

    assert convert_size == expected
