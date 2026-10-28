import numpy as np
import pytest

from thermpy.defaults import DEFAULT_LWIR_BAND, TEMPERATURE_BAND
from thermpy.planck_invert import radiance_to_temperature
from thermpy.radiance_utilities import blackbody_spectral_radiance, build_rad2temp_lut


def band_radiance(temperature_k: float, band=DEFAULT_LWIR_BAND) -> float:
    return blackbody_spectral_radiance(band[0], band[1], float(temperature_k))


@pytest.mark.parametrize("temperature_k", [253.0, 260.0, 273.15, 288.5, 293.0])
def test_round_trip_on_lut_grid_is_exact(temperature_k):
    radiance = band_radiance(temperature_k)
    assert radiance_to_temperature(radiance) == pytest.approx(temperature_k, abs=1e-9)


@pytest.mark.parametrize("temperature_k", [254.3721, 275.0345, 290.8888])
def test_round_trip_between_grid_points_is_accurate(temperature_k):
    radiance = band_radiance(temperature_k)
    assert radiance_to_temperature(radiance) == pytest.approx(temperature_k, abs=0.01)


def test_array_input_returns_array_of_same_shape():
    temperatures = np.array([[260.0, 270.0, 280.0], [285.0, 290.0, 293.0]])
    radiances = np.vectorize(band_radiance)(temperatures)
    result = radiance_to_temperature(radiances)
    assert isinstance(result, np.ndarray)
    assert result.shape == temperatures.shape
    np.testing.assert_allclose(result, temperatures, atol=1e-9)


def test_scalar_input_returns_scalar():
    result = radiance_to_temperature(band_radiance(273.15))
    assert np.ndim(result) == 0
    assert result == pytest.approx(273.15, abs=1e-9)


def test_radiance_outside_table_returns_nan():
    below = band_radiance(TEMPERATURE_BAND[0] - 10.0)
    above = band_radiance(TEMPERATURE_BAND[1] + 10.0)
    assert np.isnan(radiance_to_temperature(below))
    assert np.isnan(radiance_to_temperature(above))


def test_nan_outside_table_does_not_affect_inside_values():
    radiances = np.array([0.0, band_radiance(280.0), 1e9])
    result = radiance_to_temperature(radiances)
    assert np.isnan(result[0])
    assert result[1] == pytest.approx(280.0, abs=1e-9)
    assert np.isnan(result[2])


def test_monotonic_radiance_gives_monotonic_temperature():
    temperatures = np.linspace(255.0, 290.0, 50)
    radiances = np.array([band_radiance(t) for t in temperatures])
    result = radiance_to_temperature(radiances)
    assert np.all(np.diff(result) > 0)


def test_list_wavelength_band_is_accepted():
    radiance = band_radiance(275.0)
    result = radiance_to_temperature(radiance, wavelength_band=list(DEFAULT_LWIR_BAND))
    assert result == pytest.approx(275.0, abs=1e-9)


def test_default_band_matches_explicit_band():
    radiance = band_radiance(280.0)
    assert radiance_to_temperature(radiance) == pytest.approx(
        radiance_to_temperature(radiance, wavelength_band=DEFAULT_LWIR_BAND)
    )


def test_custom_lut_is_used_when_band_matches():
    lut = build_rad2temp_lut(wavelength_bands=DEFAULT_LWIR_BAND, temperature_band=(280.0, 320.0))
    result = radiance_to_temperature(
        band_radiance(300.0), wavelength_band=DEFAULT_LWIR_BAND, rad2temp_lut=lut
    )
    assert result == pytest.approx(300.0, abs=1e-9)


def test_custom_lut_narrower_range_returns_nan_outside_it():
    lut = build_rad2temp_lut(wavelength_bands=DEFAULT_LWIR_BAND, temperature_band=(280.0, 320.0))
    result = radiance_to_temperature(
        band_radiance(260.0), wavelength_band=DEFAULT_LWIR_BAND, rad2temp_lut=lut
    )
    assert np.isnan(result)


def test_lut_for_different_band_raises_value_error():
    other_band = (8.0, 14.0)
    lut = build_rad2temp_lut(wavelength_bands=other_band)
    with pytest.raises(ValueError, match="LUT was built for wavelength band"):
        radiance_to_temperature(
            band_radiance(275.0),
            wavelength_band=DEFAULT_LWIR_BAND,
            rad2temp_lut=lut,
        )
