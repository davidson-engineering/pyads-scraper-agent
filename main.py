#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Created By  : Matthew Davidson
# Created Date: 2024-01-01
# version ='0.0.1'
# ---------------------------------------------------------------------------
"""a_short_project_description"""
# ---------------------------------------------------------------------------

import asyncio
import logging
from logging.config import dictConfig

from pyads_scraper_agent import PyAdsScraperAgent
from config_loader import load_configs

logger = logging.getLogger(__name__)

CONFIG = load_configs(
    ["config/application.toml", "config/logging.yaml", "config/ads_targets.yaml"]
)
dictConfig(CONFIG["logging"])


async def main():
    buffer = []
    scrapers = [
        PyAdsScraperAgent(buffer, name, **target)
        for name, target in CONFIG["ads_targets"].items()
    ]
    asyncio.gather(*[scraper.do_work_periodically() for scraper in scrapers])
    # print(scraper._buffer)


if __name__ == "__main__":
    asyncio.run(main())
