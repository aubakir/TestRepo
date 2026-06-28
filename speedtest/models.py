"""Доменные модели результатов замера скорости."""

from __future__ import annotations

import statistics
from dataclasses import dataclass, field
from datetime import datetime


@dataclass(frozen=True, slots=True)
class RequestResult:
    """Результат одного HTTP-запроса на скачивание."""

    index: int
    bytes_downloaded: int
    elapsed_seconds: float
    timestamp: datetime = field(default_factory=datetime.now)

    @property
    def mb_downloaded(self) -> float:
        return self.bytes_downloaded / (1024 * 1024)

    @property
    def speed_mbps(self) -> float:
        return self.mb_downloaded / self.elapsed_seconds if self.elapsed_seconds > 0 else 0.0


@dataclass(frozen=True, slots=True)
class SpeedReport:
    """Сводный отчёт по всем выполненным запросам."""

    url: str
    num_requested: int
    results: tuple[RequestResult, ...]

    # ------------------------------------------------------------------ вычисляемые поля

    @property
    def success_count(self) -> int:
        return len(self.results)

    @property
    def total_bytes(self) -> int:
        return sum(r.bytes_downloaded for r in self.results)

    @property
    def total_mb(self) -> float:
        return self.total_bytes / (1024 * 1024)

    @property
    def total_time(self) -> float:
        return sum(r.elapsed_seconds for r in self.results)

    @property
    def avg_time(self) -> float:
        return self.total_time / len(self.results) if self.results else 0.0

    @property
    def avg_speed_mbps(self) -> float:
        return self.total_mb / self.total_time if self.total_time > 0 else 0.0

    @property
    def min_speed_mbps(self) -> float:
        return min((r.speed_mbps for r in self.results), default=0.0)

    @property
    def max_speed_mbps(self) -> float:
        return max((r.speed_mbps for r in self.results), default=0.0)

    @property
    def median_speed_mbps(self) -> float:
        speeds = [r.speed_mbps for r in self.results]
        return statistics.median(speeds) if speeds else 0.0

    @property
    def stdev_speed_mbps(self) -> float | None:
        speeds = [r.speed_mbps for r in self.results]
        return statistics.stdev(speeds) if len(speeds) >= 2 else None
