"""
Utilities for radiance calculations.
"""

import functools
from typing import NamedTuple

import numpy

from thermpy.constants import c1, c2
from thermpy.defaults import (
    DEFAULT_LWIR_BAND,
    TEMPERATURE_BAND,
    TEMPERATURE_STEP,
    WAVELENGTH_STEP,
)


def blackbody_radiance(
    wavelength_l: float | numpy.ndarray, temperature_k: float
) -> float | numpy.ndarray:
    """
    Compute blackbody radiance for a given wavelength (in micrometers) and temperature (in Kelvin).
    Function uses Planck's law to compute radiance. Radiance is returned in units of W/m^2/micrometer/sr.

    The radiance returned here is the instantaneous value at the given wavelength.

    Usage:
    # Eg: Compute the radiance in thermal IR wavelength for an object at room temperature
    >>> blackbody_radiance(wavelength_l=8.5, temperature_k=300)
    """

    wavelength_m = numpy.asarray(wavelength_l) * 1e-6  # convert to meters
    R = (c1 / (wavelength_m**5)) / (
        numpy.exp(c2 / (wavelength_m * temperature_k)) - 1
    )  # Radiance in W/m^2/m/sr
    # Convert to per micrometer as that is more useful unit
    R2 = R / 10**6
    return R2


@functools.cache
def blackbody_spectral_radiance(
    wavelength_l1: float, wavelength_l2: float, temperature_k: float
) -> float:
    """
    Compute spectral radiance between two wavelengths (in micrometers) for a given temperature. This is the
    integral radiance emitted in the given wavelength range. This algorithm performs numerical integration using
    trapezoidal formula to calculate the effective radiance over the range. This is similar to `area under curve` calculation
    in numerical methods.
    """
    # assert l1 < l2
    assert wavelength_l1 < wavelength_l2

    # between the provided wavelength bands, create a nanometer array of wavelength increments
    wavelengths = numpy.arange(wavelength_l1, wavelength_l2 + WAVELENGTH_STEP, WAVELENGTH_STEP)

    # compute the blackbody radiance for each of the wavelength step
    radiances = blackbody_radiance(wavelengths, temperature_k)

    # integrate using trapezoidal rule
    spectral_radiance = numpy.trapezoid(radiances, wavelengths)

    return spectral_radiance


class Rad2TempLUT(NamedTuple):
    temperature: numpy.ndarray
    radiance: numpy.ndarray
    wavelength_band: tuple[float, float]


@functools.cache
def build_rad2temp_lut(
    wavelength_bands: tuple[float, float] = DEFAULT_LWIR_BAND,
    temperature_band: tuple[float, float] = TEMPERATURE_BAND,
) -> Rad2TempLUT:
    """
    Build a lookup table of blackbody spectral radiance vs temperature. You specify a
    wavelength band and temperature range, typically to match a known sensor / camera and
    temperature range of interest. The LUT can then be passed to Planck inversion functions.

    Parameters:
        wavelength_bands: tuple of start and end wavelengths in micrometers
        temperature_band: tuple of min and max temperatures in Kelvin
    Returns:
        Rad2TempLUT with temperatures and radiances
    """
    lut_temperatures = numpy.arange(
        temperature_band[0], temperature_band[1] + TEMPERATURE_STEP, TEMPERATURE_STEP
    )
    lut_radiances = [blackbody_spectral_radiance(*wavelength_bands, T) for T in lut_temperatures]

    lut_radiances = numpy.asarray(lut_radiances)
    lut_temperatures.setflags(write=False)
    lut_radiances.setflags(write=False)
    return Rad2TempLUT(lut_temperatures, lut_radiances, wavelength_bands)
