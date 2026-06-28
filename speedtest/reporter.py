"""Вывод результатов в консоль: прогресс в реальном времени и итоговая сводка."""

from __future__ import annotations

from .models import RequestResult, SpeedReport

_COL = 72  # ширина разделителя


def print_header(url: str, num_requests: int) -> None:
    print("=" * _COL)
    print("  Замер скорости интернета")
    print("=" * _COL)
    print(f"  Адрес   : {url}")
    print(f"  Запросов: {num_requests}")
    print("-" * _COL)
    print(f"  {'№':>4}  {'Размер':>8}  {'Время':>8}  {'Скорость':>10}")
    print("-" * _COL)


def print_result(result: RequestResult) -> None:
    print(
        f"  [{result.index:02d}]  "
        f"{result.mb_downloaded:6.2f} МБ  "
        f"{result.elapsed_seconds:6.3f} с  "
        f"  {result.speed_mbps:7.2f} МБ/с"
    )


def print_summary(report: SpeedReport) -> None:
    print("=" * _COL)

    if not report.results:
        failed = report.num_requested
        print(f"  Все {failed} запрос(а/ов) завершились ошибкой. Проверьте URL или соединение.")
        print("=" * _COL)
        return

    failed = report.num_requested - report.success_count
    print(f"  Результаты : {report.success_count}/{report.num_requested} успешно"
          + (f"  ({failed} ошибок)" if failed else ""))
    print(f"  Всего      : {report.total_mb:.2f} МБ скачано")
    print(f"  Ср. время  : {report.avg_time:.3f} с / запрос")
    print("-" * _COL)
    print(f"  Скорость среднее : {report.avg_speed_mbps:>8.2f} МБ/с")
    print(f"           медиана : {report.median_speed_mbps:>8.2f} МБ/с")
    print(f"               мин : {report.min_speed_mbps:>8.2f} МБ/с")
    print(f"               макс: {report.max_speed_mbps:>8.2f} МБ/с")
    if report.stdev_speed_mbps is not None:
        print(f"         отклонение: {report.stdev_speed_mbps:>8.2f} МБ/с")
    print("=" * _COL)
