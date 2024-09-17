#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Created By  : Matthew Davidson
# Created Date: 2023-01-23
# version ='1.0'
# ---------------------------------------------------------------------------
"""a_short_module_description"""
# ---------------------------------------------------------------------------

import asyncio
from typing import Union
from collections import deque
from pathlib import Path
import logging

from ads_client import ADSConnection

logger = logging.getLogger(__name__)


class GetRequestUnsuccessful(Exception):
    pass


class PyAdsScraperAgent:

    def __init__(
        self,
        buffer: Union[list, deque],
        name: str = None,
        ams_net_id=None,
        ip_address=None,
        ams_net_port=None,
        data_names=None,
        update_interval: int = 1,
    ):
        self._buffer = buffer
        self.target = ADSConnection(
            ams_net_id=ams_net_id, ip_address=ip_address, ams_net_port=ams_net_port
        )
        self.update_interval = 1
        self.data_names = data_names

    async def do_work_periodically(self, *args, update_interval=None, **kwargs):
        update_interval = update_interval or self.update_interval
        while True:
            await self.do_work(args, kwargs)
            await asyncio.sleep(update_interval)

    async def do_work(self, *args, **kwargs):

        # Get data in form of dict to load to the buffer
        read_data = self.target.read_list_by_name(data_names=self.data_names)

        # Add to input buffer
        if read_data:
            logger.info(f"Adding {len(read_data)} metrics to queue")
            if isinstance(read_data, (tuple, list)):
                self._buffer.extend(read_data)
            else:
                self._buffer.append(read_data)
