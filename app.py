"""Точка входа для замерятеля скорости интернета.

Запуск:
    python app.py

Все параметры (URL, количество запросов, таймаут) настраиваются
в файле speedtest/config.py.
"""

from __future__ import annotations

import logging
import sys

from speedtest import print_header, print_result, print_summary, run_measurements
import speedtest.config as cfg


def main() -> int:
    logging.basicConfig(
        level=logging.WARNING,
        format="%(levelname)s %(name)s: %(message)s",
    )

    print_header(cfg.URL, cfg.NUM_REQUESTS)

    report = run_measurements(
        url=cfg.URL,
        num_requests=cfg.NUM_REQUESTS,
        timeout=cfg.TIMEOUT_SEC,
        on_result=print_result,
    )

    print_summary(report)

    return 0 if report.results else 1


if __name__ == "__main__":
    sys.exit(main())

