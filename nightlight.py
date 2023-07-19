#!/usr/bin/env python3

"""Starts a fake lightbulb
"""
import logging
import signal
import random

from pyhap.accessory import Accessory, Bridge
from pyhap.accessory_driver import AccessoryDriver
from pyhap.const import (CATEGORY_FAN,
                         CATEGORY_LIGHTBULB,
                         CATEGORY_GARAGE_DOOR_OPENER,
                         CATEGORY_SENSOR)

from lightshow import LightShow

logging.basicConfig(level=logging.INFO, format="[%(module)s] %(message)s")


class LightBulb(Accessory):
    """Fake lightbulb, logs what the client sets."""

    category = CATEGORY_LIGHTBULB
    lightshow = LightShow()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        serv_light = self.add_preload_service('Lightbulb')
        self.char_on = serv_light.configure_char(
            'On', setter_callback=self.set_bulb)

    def set_bulb(self, value):
        if value:
            self.lightshow.start()
        else:
            self.lightshow.stop()
        logging.info("Bulb value: %s", value)

def get_bridge(driver):
    bridge = Bridge(driver, 'Bridge')

    bridge.add_accessory(LightBulb(driver, 'Night Light'))

    return bridge


driver = AccessoryDriver(port=51826, persist_file='nightlight.state')
driver.add_accessory(accessory=get_bridge(driver))
signal.signal(signal.SIGTERM, driver.signal_handler)
driver.start()
