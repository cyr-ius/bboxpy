"""This example can be run safely as it won't change anything in your box configuration."""

import asyncio
from contextlib import suppress
import logging
from typing import Any, Callable

import yaml  # type: ignore

from bboxpy import Bbox
from bboxpy.exceptions import AuthorizationError, BboxException, HttpRequestError

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
ch.setFormatter(formatter)
logger.addHandler(ch)


# Fill out the secrets in secrets.yaml, you can find an example
# _secrets.yaml file, which has to be renamed after filling out the secrets.
with open("./secrets.yaml", encoding="UTF-8") as file:
    secrets: dict[str, Any] = yaml.safe_load(file)

PASSWORD = secrets["PASSWORD"]  # mandatory


# mypy: disable-error-code="attr-defined"
async def async_main() -> None:
    """Instantiate class."""
    bbox = Bbox(password=PASSWORD)

    # Explicit login (Optional)
    try:
        await bbox.async_login()
    except (AuthorizationError, HttpRequestError) as err:
        logger.error(err)
        return

    # Simple example.
    info = await bbox.device.async_get_bbox_info()
    logger.info(info)

    # Executes all methods available in bboxpy
    async def call(func: Callable[..., Any], *args: Any) -> None:
        rslt: (
            dict[Any, Any]
            | list[Any]
            | set[Any]
            | float
            | int
            | str
            | tuple[Any, ...]
            | Any
        ) = {}
        with suppress(Exception):
            rsp = await func(*args)
            rslt = (
                rsp
                if isinstance(rsp, dict | list | set | float | int | str | tuple)
                else vars(rsp)
            )
        logger.inf(f"{func.__name__}: {rslt}")

    await call(bbox.device.async_get_bbox_info)
    await call(bbox.iptv.async_get_iptv_info)
    await call(bbox.ddns.async_get_ddns)
    await call(bbox.lan.async_get_connected_devices)
    await call(bbox.lan.async_get_the_list_of_user_alerts)
    await call(bbox.voip.async_get_voip_voicemail)
    await call(bbox.wan.async_get_wan_ftth)
    await call(bbox.wan.async_get_wan_ip_stats)
    await call(bbox.services.async_get_bbox_services)
    await call(bbox.services.async_get_events_notification_service)
    await call(bbox.remote.async_get_wakeonlan_configuration)
    await call(bbox.wifi.async_get_wireless)
    await call(bbox.wifi.async_get_stats_5)
    await call(bbox.wifi.async_get_stats_24)
    await call(bbox.wifi.async_get_wps)
    await call(bbox.wifi.async_get_repeater)

    # Actions
    try:
        await bbox.device.async_display(luminosity=50)
        # await bbox.device.async_reboot()
    except BboxException as error:
        logger.error(error)

    await bbox.async_close()


if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    asyncio.run(async_main())
