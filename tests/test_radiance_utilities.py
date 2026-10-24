import math

import numpy
import pytest

from thermpy.radiance_utilities import blackbody_radiance, blackbody_spectral_radiance

STEFAN_BOLTZMANN = 5.670374419e-8  # W/m^2/K^4


def test_blackbody_radiance_matches_known_value_at_10um_300k():
    # Reference value for a 300 K blackbody at 10 um, in W/m^2/sr/um
    assert blackbody_radiance(10.0, 300.0) == pytest.approx(9.92, rel=1e-2)


@pytest.mark.parametrize("wavelength", [3.0, 8.5, 10.0, 14.0])
def test_blackbody_radiance_is_positive_and_finite(wavelength):
    value = blackbody_radiance(wavelength, 300.0)
    assert value > 0
    assert math.isfinite(value)


def test_blackbody_radiance_increases_with_temperature():
    values = [blackbody_radiance(10.0, t) for t in (250.0, 300.0, 350.0, 400.0)]
    assert values == sorted(values)  # monotonic increase
    assert len(set(values)) == len(values)


def test_blackbody_radiance_peak_follows_wien_displacement():
    wavelengths = numpy.linspace(1.0, 50.0, 50_000)
    radiances = [blackbody_radiance(w, 300.0) for w in wavelengths]
    peak = wavelengths[int(numpy.argmax(radiances))]
    # Wien's law: lambda_max = 2898 um*K / T
    assert peak == pytest.approx(2898 / 300, abs=0.05)


def test_spectral_radiance_matches_stefan_boltzmann_over_wide_band():
    # 0.5-100 um covers about 99.5% of the total emission at 300 K
    total = blackbody_spectral_radiance(0.5, 100.0, 300.0)
    expected = STEFAN_BOLTZMANN * 300.0**4 / math.pi
    assert total == pytest.approx(expected, rel=0.02)


def test_spectral_radiance_over_narrow_band_approximates_width_times_radiance():
    l1, l2 = 10.0, 10.1
    spectral = blackbody_spectral_radiance(l1, l2, 300.0)
    midpoint_radiance = blackbody_radiance((l1 + l2) / 2, 300.0)
    assert spectral == pytest.approx(midpoint_radiance * (l2 - l1), rel=5e-3)


def test_spectral_radiance_rejects_inverted_band():
    with pytest.raises(AssertionError):
        blackbody_spectral_radiance(14.0, 8.0, 300.0)
