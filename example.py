"""This example can be run safely as it won't change anything in your box configuration."""

import asyncio
import logging

from bboxpy import Bbox
from bboxpy.exceptions import AuthorizationError, BboxException

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
# create console handler and set level to debug
ch = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
ch.setFormatter(formatter)
logger.addHandler(ch)


async def async_main() -> None:
    """Instantiate Livebox class."""
    bbox = Bbox(password="xxxxx")
    try:
        await bbox.async_login()
    except AuthorizationError as err:
        logger.error(err)
        return

    try:
        device_info = await bbox.device.async_get_bbox_info()
        logger.info(device_info)
    except BboxException as error:
        logger.error(error)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(async_main())
