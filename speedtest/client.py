"""Низкоуровневый HTTP-клиент для скачивания файлов."""

from __future__ import annotations

import time
import urllib.request
from urllib.error import HTTPError, URLError

from .config import TIMEOUT_SEC as DEFAULT_TIMEOUT_SEC
from .models import RequestResult


class DownloadError(Exception):
    """Выбрасывается при любой ошибке во время скачивания."""


def download_once(
    url: str,
    index: int,
    timeout: int = DEFAULT_TIMEOUT_SEC,
) -> RequestResult:
    """Выполняет один HTTP GET, читает тело ответа целиком и возвращает результат.

    Raises:
        DownloadError: при любой сетевой или HTTP-ошибке.
    """
    try:
        start = time.perf_counter()
        with urllib.request.urlopen(url, timeout=timeout) as response:  # noqa: S310
            data: bytes = response.read()
        elapsed = time.perf_counter() - start
    except HTTPError as exc:
        raise DownloadError(f"HTTP {exc.code}: {exc.reason}") from exc
    except URLError as exc:
        raise DownloadError(f"URL error: {exc.reason}") from exc
    except OSError as exc:
        raise DownloadError(str(exc)) from exc

    return RequestResult(
        index=index,
        bytes_downloaded=len(data),
        elapsed_seconds=elapsed,
    )
