"""Dreo API for controling air circulator fans."""
import logging
from typing import Dict
from typing import TYPE_CHECKING

from .pydreofan import PyDreoFan
from .constant import *

if TYPE_CHECKING:
    from pydreo import PyDreo

_LOGGER = logging.getLogger(LOGGER_NAME)

class PyDreoAirCirculatorFan(PyDreoFan):
    """
    Class representing a Dreo Air Circulator Fan
    """

    def __init__(self, fan_definition: PyDreoFanDefinition, details: Dict[str, list], dreoManager: "PyDreo") -> None:
        """Initialize air devices."""
        super().__init__(fan_definition, details, dreoManager)
        self._fan_definition = fan_definition
        self._horizontally_oscillating = None
        self._vertically_oscillating = None

    def handle_server_update(self, message: dict):
        """Handle an incoming WebSocket message."""
        super().handle_server_update(message)

        valHorizontalOscillation = self.get_server_update_key_value(message, HORIZONTAL_OSCILLATION_KEY)
        if isinstance(valHorizontalOscillation, bool):
            self._horizontally_oscillating = valHorizontalOscillation

        valVerticalOscillation = self.get_server_update_key_value(message, VERTICAL_OSCILLATION_KEY)
        if isinstance(valVerticalOscillation, bool):
            self._vertically_oscillating = valVerticalOscillation

    @property
    def is_on(self):
        """Returns `True` if the device is on, `False` otherwise."""
        return self._is_on


    @property
    def oscillating(self):
        """Returns `True` if either horizontal or vertical oscillation is on."""
        return self._horizontally_oscillating or self._vertically_oscillating

    @property
    def horizontally_oscillating(self):
        return self._horizontally_oscillating

    @property
    def vertically_oscillating(self):
        return self._vertically_oscillating

    @property
    def supports_horizontal_oscillation(self):
        return self._horizontally_oscillating is not None

    @property
    def supports_vertical_oscillation(self) -> bool:
        return self._vertically_oscillating is not None

    def oscillate_horizontally(self, oscillating: bool) -> None:
        _LOGGER.debug("PyDreoAirCirculatorFan:oscillate_horizontally")
        self._send_command(HORIZONTAL_OSCILLATION_KEY, oscillating)

    def update_state(self, state: dict):
        _LOGGER.debug("PyDreoAirCirculatorFan:update_state")
        super().update_state(state)

        self._horizontally_oscillating = self.get_state_update_value(state, HORIZONTAL_OSCILLATION_KEY)
        self._vertically_oscillating = self.get_state_update_value(state, VERTICAL_OSCILLATION_KEY)

    # NOTE: some of these fans can oscillate horizontally and vertically
    # since HA's fan entity only supports a single oscillation option,
    # this method prefers horizontal oscillation over vertical oscillation
    # when present.
    # TODO: Create seperate switches in HA to support this.

    @property
    def supports_oscillation(self):
        return self.supports_horizontal_oscillation or self.supports_vertical_oscillation
        
    def oscillate(self, oscillating: bool) -> None:
        """Enable oscillation.  Perfer horizontal if supported."""
        _LOGGER.debug("PyDreoAirCirculatorFan:oscillate")
        if self.supports_horizontal_oscillation:
            self.oscillate_horizontally(oscillating)
        elif self.supports_vertical_oscillation:
            self.oscillate_vertically(oscillating)
        else:
            _LOGGER.error("This device does not support oscillation")

    def oscillate_vertically(self, oscillating: bool) -> None:
        """Enable or disable vertical oscillation"""
        _LOGGER.debug("PyDreoAirCirculatorFan:oscillate_vertically")
        self._send_command(VERTICAL_OSCILLATION_KEY, oscillating)

    def set_horizontal_oscillation_angle(self, angle: int) -> None:
        """Set the horizontal oscillation angle."""
        _LOGGER.debug("PyDreoAirCirculatorFan:set_horizontal_oscillation_angle")
        if not self.supports_horizontal_oscillation:
            _LOGGER.error("This device does not support horizontal oscillation")
            return
        self._send_command(HORIZONTAL_OSCILLATION_ANGLE_KEY, angle)

    def set_vertical_oscillation_angle(self, angle: int) -> None:
        """Set the vertical oscillation angle."""
        _LOGGER.debug("PyDreoAirCirculatorFan:set_vertical_oscillation_angle")
        if not self.supports_vertical_oscillation:
            _LOGGER.error("This device does not support vertical oscillation")
            return

        self._send_command(VERTICAL_OSCILLATION_ANGLE_KEY, angle)
