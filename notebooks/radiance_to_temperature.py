import marimo

__generated_with = "0.25.2"
app = marimo.App(width="medium")


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # From Radiance to Temperature
    ## Inverting Planck's law with the `thermpy` library

    A thermal sensor does not measure temperature. It measures the **radiance** reaching it within a band of wavelengths. To recover temperature we invert Planck's law:

    1. Compute the radiance a blackbody would emit in the sensor's band for a fine ladder of temperatures. This forms a **look up table (LUT)** of temperature vs. radiance.
    2. For a measured radiance, **interpolate** the LUT to find the temperature.

    This notebook walks through that workflow using `thermpy.radiance_utilities` and `thermpy.planck_invert`. All units are SI: wavelengths in $\mu m$, temperature in $K$ and band-integrated radiance in $W/m^2/sr$.
    """)


@app.cell
def _():
    import marimo as mo
    import numpy as np
    import plotly.express as px

    from thermpy import constants, defaults, planck_invert, radiance_utilities

    return constants, defaults, mo, np, planck_invert, px, radiance_utilities


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## The sensor band

    Radiance is only meaningful for a given wavelength band, which is determined by your sensor. `thermpy.constants` defines a few common thermal bands, and `thermpy.defaults` picks `DEFAULT_LWIR_BAND` for use in the examples.
    """)


@app.cell
def _(constants, defaults):
    print("Mid-wave IR       :", constants.mwir_l, "um")
    print("Long-wave IR (1)  :", constants.lwir2_l, "um")
    print("Long-wave IR (2)  :", constants.lwir3_l, "um")
    print("Default band      :", defaults.DEFAULT_LWIR_BAND, "um")
    print("Default temp range:", defaults.TEMPERATURE_BAND, "K")


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Step 1: Forward model, temperature to radiance

    `blackbody_spectral_radiance()` integrates Planck's law over the band using the trapezoidal rule. Here is the radiance a blackbody at $293\,K$ (about $20\,°C$) emits in the default band:
    """)


@app.cell
def _(defaults, radiance_utilities):
    band = defaults.DEFAULT_LWIR_BAND
    radiance_293 = radiance_utilities.blackbody_spectral_radiance(*band, temperature_k=293)
    print(f"{radiance_293:.4f} W/m^2/sr")


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Step 2: Inverse model, radiance to temperature

    `radiance_to_temperature()` goes the other way. Feeding in the radiance we just computed should give us back $293\,K$.
    """)


@app.cell
def _(band, planck_invert, radiance_293):
    planck_invert.radiance_to_temperature(radiance_293, wavelength_band=band)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Building and reusing the look up table

    If you don't pass a LUT, `radiance_to_temperature()` builds one for you. Building it is the expensive part, as it integrates Planck's law at every temperature step, so for repeated calls (for example, processing many images) build it once with `build_rad2temp_lut()` and pass it in. Results are also cached for identical arguments.

    The LUT is a `Rad2TempLUT` named tuple of temperature, radiance and the wavelength band it was built for.
    """)


@app.cell
def _(band, defaults, radiance_utilities):
    lut = radiance_utilities.build_rad2temp_lut(
        wavelength_bands=band, temperature_band=defaults.TEMPERATURE_BAND
    )
    print("Wavelength band  :", lut.wavelength_band, "um")
    print("Number of entries:", len(lut.temperature))
    print("Temperature range:", lut.temperature[0], "to", lut.temperature[-1], "K")
    print(
        "Radiance range   :",
        round(lut.radiance[0], 3),
        "to",
        round(lut.radiance[-1], 3),
        "W/m^2/sr",
    )


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Radiance grows monotonically with temperature (Stefan-Boltzmann), which is what makes the inversion by interpolation well defined.
    """)


@app.cell
def _(lut, px):
    px.line(
        x=lut.temperature,
        y=lut.radiance,
        labels={"x": "Temperature (K)", "y": "Band radiance (W/m²/sr)"},
        title="Look up table: blackbody radiance vs. temperature",
        template="plotly_white",
    )


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Converting a single measurement, and many at once

    Both scalars and NumPy arrays of any shape are accepted. Pass the LUT you built to avoid rebuilding it.
    """)


@app.cell
def _(band, lut, planck_invert):
    planck_invert.radiance_to_temperature(45.0, wavelength_band=band, rad2temp_lut=lut)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### A simulated radiance image

    A thermal image is just a 2D array of radiances. Below we simulate a scene whose true temperature rises smoothly from $258\,K$ to $288\,K$ with a warm "hot spot", compute the radiance a sensor would see, then recover the temperature from that radiance alone.
    """)


@app.cell
def _(band, np, radiance_utilities):
    _n = 60
    _y, _x = np.mgrid[0:_n, 0:_n]
    _hot_spot = 6 * np.exp(-(((_x - 40) ** 2 + (_y - 20) ** 2) / 60))
    true_temperature = 258 + 24 * (_x + _y) / (2 * _n) + _hot_spot

    # Forward model on a coarse grid of temperatures, then interpolate. This is
    # only to synthesize the "measured" image quickly.
    _grid = np.linspace(true_temperature.min(), true_temperature.max(), 200)
    _grid_rad = np.array(
        [radiance_utilities.blackbody_spectral_radiance(*band, float(t)) for t in _grid]
    )
    radiance_image = np.interp(true_temperature, _grid, _grid_rad)
    print("Radiance image shape:", radiance_image.shape)


@app.cell
def _(band, lut, planck_invert, radiance_image):
    temperature_image = planck_invert.radiance_to_temperature(
        radiance_image, wavelength_band=band, rad2temp_lut=lut
    )
    print("Temperature image shape:", temperature_image.shape)


@app.cell
def _(mo, px, radiance_image, temperature_image):
    _radiance_fig = px.imshow(
        radiance_image,
        color_continuous_scale="Inferno",
        title="Radiance (W/m²/sr)",
        labels={"color": "W/m²/sr"},
    )
    _temperature_fig = px.imshow(
        temperature_image,
        color_continuous_scale="Inferno",
        title="Temperature (K)",
        labels={"color": "K"},
    )
    mo.hstack([_radiance_fig, _temperature_fig])


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### How accurate is the inversion?

    The look up table has a $1\,mK$ step, so the round trip error is tiny, far below any real sensor's noise. Any residual comes from the coarse grid used to synthesize the image above and from interpolation in the LUT.
    """)


@app.cell
def _(np, temperature_image, true_temperature):
    _error = np.abs(temperature_image - true_temperature)
    print(f"Max absolute error: {np.nanmax(_error) * 1000:.2f} mK")


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Out-of-range radiance returns `NaN`

    The default temperature range is $253$ to $293\,K$ (about $-20$ to $20\,°C$). Radiance outside the LUT is not clamped, it returns `NaN`, so you can't mistake an extrapolation for a measurement. Here, $300\,K$ is warmer than the table allows:
    """)


@app.cell
def _(band, lut, planck_invert, radiance_utilities):
    _warm = radiance_utilities.blackbody_spectral_radiance(*band, temperature_k=300)
    planck_invert.radiance_to_temperature(_warm, wavelength_band=band, rad2temp_lut=lut)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Choosing your own band and temperature range

    For a warmer scene, or a different sensor, build a LUT for your own wavelength band and temperature range. Here is a $8.0\text{-}14.0\,\mu m$ sensor imaging a scene between $250\,K$ and $350\,K$:
    """)


@app.cell
def _(planck_invert, radiance_utilities):
    custom_band = (8.0, 14.0)
    custom_lut = radiance_utilities.build_rad2temp_lut(
        wavelength_bands=custom_band, temperature_band=(250, 350)
    )
    _measured = radiance_utilities.blackbody_spectral_radiance(*custom_band, temperature_k=300)
    planck_invert.radiance_to_temperature(
        _measured, wavelength_band=custom_band, rad2temp_lut=custom_lut
    )


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    A LUT is only valid for the band it was built for. Passing a mismatched LUT raises a `ValueError` instead of silently returning wrong temperatures:
    """)


@app.cell
def _(band, custom_lut, planck_invert):
    try:
        planck_invert.radiance_to_temperature(40.0, wavelength_band=band, rad2temp_lut=custom_lut)
    except ValueError as e:
        print("ValueError:", e)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## What's next

    The radiance here is assumed to be that of a perfect blackbody. Real surfaces emit less than a blackbody at the same temperature (emissivity $\varepsilon < 1$), which biases temperatures low. Upcoming notebooks cover converting georeferenced rasters and applying emissivity correction.
    """)


if __name__ == "__main__":
    app.run()
