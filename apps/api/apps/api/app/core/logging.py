import logging
import sys

def setup_logging(level: str = "INFO") -> None:
    """
    Simple structured-ish logger for hackathon/demo.
    You can replace this with structlog later.
    """
    logging.basicConfig(
        level=getattr(logging, level.upper(), logging.INFO),
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        handlers=[logging.StreamHandler(sys.stdout)],
    )

logger = logging.getLogger("eduequity")
