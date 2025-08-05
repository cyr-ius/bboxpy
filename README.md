# bboxpy

Manage your Bouygues Bbox in Python

Easily manage your Bbox in Python.
Check your config, configure your dhcp, disable your wifi, monitor your LAN activity and many others, on LAN or remotely.

bboxpy is a python library implementing fir the Bbox.

This project is based on stilllman/aiofreepybox, which provides the same features as aiofreepybox in a synchronous manner.

## Install

Use the PIP package manager

```bash
$ pip install bboxpy
```

Or manually download and install the last version from github

```bash
$ git clone https://github.com/cyr-ius/bboxpy.git
$ python setup.py install
```

## Get started

```python
# Import the bboxpy package.
from bboxpy import Bbox
from bboxpy.exceptions import BboxException

async def async_main():
    # Instantiate the Sysbus class using default options.
    bbox = Bbox(password='xxxxxx')

    # Connect. (optional)
    await bbox.async_login()

    try:
        device_info = await bbox.device.async_get_bbox_info()
        print(device_info)
    except BboxException as error:
        pass

    # Do something useful, rebooting your bbox for example.
    await bbox.device.async_reboot()

    # Properly close the session.
    await bbox.async_logout()
    await bbox.async_close()

    #Call api (raw mode)
    summary = await bbox.async_raw_request(method="get", path="device/summary")
    print(summary)


if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    asyncio.run(async_main())

```
