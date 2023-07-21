"""Dreo API for controling fans."""

import logging
from typing import TYPE_CHECKING, Dict

from .constant import *
from .pydreobasedevice import PyDreoBaseDevice

_LOGGER = logging.getLogger(LOGGER_NAME)

if TYPE_CHECKING:
    from pydreo import PyDreo


class PyDreoFan(PyDreoBaseDevice):
    """Base class for Dreo Fan API Calls."""

    def __init__(self, fan_definition: PyDreoFanDefinition, details: Dict[str, list], dreo: "PyDreo"):
        """Initialize air devices."""
        super().__init__(details, dreo)

        self._fan_definition = fan_definition

    def __repr__(self):
        # Representation string of object.
        return "<{0}:{1}:{2}>".format(
            self.__class__.__name__, self._device_id, self._name
        )

    def handle_server_update(self, message):
        valPoweron = self.get_server_update_key_value(message, POWERON_KEY)
        if isinstance(valPoweron, bool):
            self._is_on = valPoweron

    @property
    def speed_range(self):
        return self._fan_definition.speed_range

            
    @property
    def is_on(self):
        """Returns `True` if the device is on, `False` otherwise."""
        return self._is_on

    @property
    def fan_speed(self):
        return self._fan_speed


    @property
    def supports_oscillation(self):
        pass

    @property
    def oscillating(self):
        pass
    
    def set_power(self, value: bool):
        _LOGGER.debug("PyDreoFan:set_power")
        self._send_command(POWERON_KEY, value)
    
    def change_fan_speed(self, fan_speed : int) :
        # TODO: Make sure fan speed in range
        self._send_command(WINDLEVEL_KEY, fan_speed)
