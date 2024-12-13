"""This example can be run safely as it won't change anything in your box configuration."""

import asyncio
import logging
from typing import Any

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
    """Instantiate Livebox class."""
    bbox = Bbox(password=PASSWORD)
    try:
        await bbox.async_login()
    except (AuthorizationError, HttpRequestError) as err:
        logger.error(err)
        return

    try:
        device_info = await bbox.device.async_get_bbox_info()
        logger.info(device_info)
        iptv_info = await bbox.iptv.async_get_iptv_info()
        logger.info(iptv_info)
        ddns_info = await bbox.ddns.async_get_ddns()
        logger.info(ddns_info)
        devices = await bbox.lan.async_get_connected_devices()
        logger.info(devices)
        voicemail = await bbox.voip.async_get_voip_voicemail()
        logger.info(voicemail)
        ftth = await bbox.wan.async_get_wan_ftth()
        logger.info(ftth)

        # Actions
        await bbox.device.async_display(luminosity=50)
        # await bbox.device.async_reboot()

    except BboxException as error:
        logger.error(error)

    await bbox.async_close()


if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    asyncio.run(async_main())
