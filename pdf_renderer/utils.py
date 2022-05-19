from .types import ConvertSize


def get_convert_size_from_pdf_dimensions(
    width: int,
    height: int,
    max_width: int,
    max_height: int,
) -> ConvertSize:
    """Create size parameter for pdf2image converter.

    This creates ConvertSize to respect 1200x1600 image boundaries.
    """
    vert_ratio = max_height / height
    horiz_ratio = max_width / width
    if horiz_ratio < vert_ratio:
        return max_width, None
    return None, max_height
