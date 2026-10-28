"""Invert Planck's law, to go from radiance to temperature.
Using Planck's law, we first compute the blackbody radiance for the
given bandwidth of the camera's bands. Then we use this as a look up table
to find the temperature for a measured radiance. Hence, Planck's inversion.
"""

import numpy as np

from thermpy.defaults import DEFAULT_LWIR_BAND, TEMPERATURE_BAND
from thermpy.radiance_utilities import (
    Rad2TempLUT,
    build_rad2temp_lut,
)


def radiance_to_temperature(
    radiance: float | np.ndarray,
    wavelength_band: tuple[float, float] = DEFAULT_LWIR_BAND,
    rad2temp_lut: Rad2TempLUT | None = None,
) -> float | np.ndarray:
    """
    Convert radiance to temperature by inverting Planck's law.

    The temperature is linearly interpolated from a lookup table. Radiance outside the
    table's range returns NaN rather than being clamped to the table's end temperatures.

    Parameters
    ----------
    radiance : float or np.ndarray
        Measured integral radiance in W/m^2/sr in the given wave band
    wavelength_band : tuple of start and end wavelengths in micrometers of
        the instrument or camera that recorded the radiance
    rad2temp_lut : optional lookup table for inversion. Use radiance_utilities.build_rad2temp_lut() for this.
        If omitted, a table is built for wavelength_band over TEMPERATURE_BAND.

    Returns
    -------
    float or np.ndarray
        Temperature in kelvin corresponding to the radiance.

    Raises
    ------
    ValueError
        If rad2temp_lut was built for a different wavelength_band.
    """
    wavelength_band = (float(wavelength_band[0]), float(wavelength_band[1]))
    if rad2temp_lut is None:
        rad2temp_lut = build_rad2temp_lut(
            wavelength_bands=wavelength_band, temperature_band=TEMPERATURE_BAND
        )
    if tuple(rad2temp_lut.wavelength_band) != wavelength_band:
        raise ValueError(
            f"LUT was built for wavelength band {rad2temp_lut.wavelength_band}, "
            f"not {wavelength_band}"
        )

    return np.interp(
        radiance,
        rad2temp_lut.radiance,
        rad2temp_lut.temperature,
        left=np.nan,
        right=np.nan,
    )
