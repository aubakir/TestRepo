"""speedtest — пакет для замера скорости интернет-соединения."""

from .measurer import run_measurements
from .models import RequestResult, SpeedReport
from .reporter import print_header, print_result, print_summary

__all__ = [
    "run_measurements",
    "RequestResult",
    "SpeedReport",
    "print_header",
    "print_result",
    "print_summary",
]
