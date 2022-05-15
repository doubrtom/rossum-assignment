import enum


class ProcessingStatus(enum.Enum):
    """Phases in PDF rendering process for one rendering Event."""

    NEW = "new"
    PROCESSING = "processing"
    FAILED = "failed"
    DONE = "done"
