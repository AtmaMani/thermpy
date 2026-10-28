"""Defining sensible defaults for common remote sensing and
computational thermography applications."""

from thermpy.constants import lwir3_l

TEMPERATURE_UNIT = "K"  # Kelvin
TEMPERATURE_STEP = 0.001  # milli Kelvin
TEMPERATURE_BAND = (253, 293)  # -20 to 20 C

WAVELENGTH_UNIT = "um"  # micrometer
WAVELENGTH_STEP = 0.001  # 1 nanometer

DEFAULT_LWIR_BAND = lwir3_l  # default camera used in examples
