import marimo

__generated_with = "0.25.2"
app = marimo.App(width="medium")


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Exploring Radiance in Remote Sensing
    ## A tour of physical laws that form the foundation of physics of remote sensing, using the `thermpy` library.

    This notebook takes you through some of the foundational concepts in remote sensing, particuarly the physics behind electromagnetic radiation. We visit the foundational laws and explore them in code using the `thermpy` library.
    """)


@app.cell
def _():
    import marimo as mo
    import numpy as np
    import pandas as pd
    import plotly.express as px

    import thermpy

    return mo, np, pd, px, thermpy


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Blackbody radiance
    ... conceptual text ...

    The `radiance_utilities` module of the `thermpy` library provides functions to compute the radiance emitted by a blackbody at a given wavelenth & temperature pair.

    ### Instantaneous energy emitted
    The `blackbody_radiance()` function computes the radiance emitted in any given wavelength by an object at given temperature. All functions use SI units, thus wavelengths are in micrometers and temperature in Kelvin, radiance in $W/m^2/\mu/sr$
    """)


@app.cell
def _(thermpy):
    # Radiance emitted in Near IR by an object at room temperature
    thermpy.radiance_utilities.blackbody_radiance(wavelength_l=950, temperature_k=300)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Cumulative energy emitted
    Physical objects seldem emit in a single wavelength. Instead, they emit in the entire spectrum of EMR (electromagnetic radiation). The `blackbody_radiance()` computes the radiance in a single desired wavelength. To obtain the cumulative energy emitted by the object in a broad (continuous) spectrum of wavelengths, we need to integrate over the range of the wavelengths. The `blackbody_spectral_radiance()` function performs this and returns the cumulative radiant energy in $W/m^2/sr$ emitted within the given lower and higher wavelength bands.
    """)


@app.cell
def _(thermpy):
    # Radiance emitted cumulatively within a given band of wavelengths
    thermpy.radiance_utilities.blackbody_spectral_radiance(
        wavelength_l1=950, wavelength_l2=1200, temperature_k=300
    )


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Visualizing Stephan Boltzmann and Wien's displacement laws

    Once we are able to calculate the radiance emitted by a blackbody, we are just steps away from computing this for the full EMR spectrum and for a variety of temperatures. The snippet below computes that for various temperature ranges and visualizes that data.
    """)


@app.cell(hide_code=True)
def _(np, pd, px, thermpy):
    # Define wavelength spectrum from UV to Thermal IR
    wavelengths = np.arange(0.1, 35, step=0.1)
    # Define temperature steps from below freezing to surface of sun
    temperature_steps = [373, 350, 300, 237, 200]

    # Build DataFrame for Plotly Express
    data = []
    for temp in temperature_steps:
        radiances = [thermpy.radiance_utilities.blackbody_radiance(w, temp) for w in wavelengths]
        # Create temporary rows for each wavelength-temperature pairing
        temp_df = pd.DataFrame(
            {
                "Wavelength": wavelengths,
                "Radiance": radiances,
                "Temperature": f"{temp} K",  # Label for each curve
            }
        )
        data.append(temp_df)

    # Concatenate into a single dataframe
    df = pd.concat(data, ignore_index=True)

    # Plot using Plotly Express
    fig = px.line(
        df,
        x="Wavelength",
        y="Radiance",
        color="Temperature",  # Automatically creates a legend and assigns a color per temperature
        labels={
            "Wavelength": r"Wavelength ($\mu$m)",
            "Radiance": r"Spectral Radiance ($W / m^2 / \mu m$)",
        },
        title="Blackbody Radiation Curves Across Temperature Steps",
        template="plotly_white",
    )

    fig.show()


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
