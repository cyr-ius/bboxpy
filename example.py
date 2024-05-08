"""This example can be run safely as it won't change anything in your box configuration."""

import asyncio
import logging

from bboxpy import Bbox
from bboxpy.exceptions import AuthorizationError, BboxException, HttpRequestError

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
# create console handler and set level to debug
ch = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
ch.setFormatter(formatter)
logger.addHandler(ch)


# mypy: disable-error-code="attr-defined"
async def async_main() -> None:
    """Instantiate Livebox class."""
    bbox = Bbox(password="xxxxx")
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


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(async_main())
