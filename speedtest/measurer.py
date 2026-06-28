"""Организует последовательные замеры скачивания и собирает SpeedReport."""

from __future__ import annotations

import logging
from collections.abc import Callable

from .client import DownloadError, download_once
from .config import NUM_REQUESTS as DEFAULT_NUM_REQUESTS
from .config import TIMEOUT_SEC as DEFAULT_TIMEOUT_SEC
from .models import RequestResult, SpeedReport

logger = logging.getLogger(__name__)


def run_measurements(
    url: str,
    num_requests: int = DEFAULT_NUM_REQUESTS,
    timeout: int = DEFAULT_TIMEOUT_SEC,
    on_result: Callable[[RequestResult], None] | None = None,
) -> SpeedReport:
    """Скачивает *url* последовательно *num_requests* раз и возвращает SpeedReport.

    Args:
        url:          Целевой URL для скачивания.
        num_requests: Количество последовательных запросов.
        timeout:      Таймаут одного запроса в секундах.
        on_result:    Необязательный колбэк, вызываемый после каждого успешного
                      скачивания — используется для вывода прогресса в реальном времени.

    Returns:
        Объект :class:`SpeedReport` со всеми успешными результатами.
    """
    results: list[RequestResult] = []

    for i in range(1, num_requests + 1):
        try:
            result = download_once(url, i, timeout)
        except DownloadError as exc:
            logger.error("Запрос %02d завершился ошибкой: %s", i, exc)
            continue

        results.append(result)

        if on_result is not None:
            on_result(result)

    return SpeedReport(
        url=url,
        num_requested=num_requests,
        results=tuple(results),
    )
