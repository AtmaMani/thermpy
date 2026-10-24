"""
Utilities for radiance calculations.
"""

import numpy

from thermpy.constants import c1, c2


def blackbody_radiance(wavelength_l: float, temperature_k: float) -> float:
    """
    Compute blackbody radiance for a given wavelength (in micrometers) and temperature (in Kelvin).
    Function uses Planck's law to compute radiance. Radiance is returned in units of W/m^2/micrometer/sr.

    The radiance returned here is the instantaneous value at the given wavelength.

    Usage:
    # Eg: Compute the radiance in thermal IR wavelength for an object at room temperature
    >>> blackbody_radiance(wavelength_l=8.5, temperature_k=300)
    """

    wavelength_m = wavelength_l * 1e-6  # convert to meters
    R = (c1 / (wavelength_m**5)) / (
        numpy.exp(c2 / (wavelength_m * temperature_k)) - 1
    )  # Radiance in W/m^2/m/sr
    # Convert to per micrometer as that is more useful unit
    R2 = R / 10**6
    return R2


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
    wavelengths = numpy.arange(wavelength_l1, wavelength_l2 + 0.001, 0.001)

    # compute the blackbody radiance for each of the wavelength step
    radiances = [blackbody_radiance(w, temperature_k) for w in wavelengths]

    # integrate using trapezoidal rule
    spectral_radiance = numpy.trapezoid(radiances, wavelengths)

    return spectral_radiance
