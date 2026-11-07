import marimo

__generated_with = "0.25.2"
app = marimo.App(width="medium")


@app.cell(hide_code=True)
def _():
    import marimo as mo

    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # thermpy

    Thermal image processing in Python: converting the radiance recorded by a thermal sensor into temperature using Planck's law. The library was originally written in 2011 and has been rebuilt for modern Python.

    The pages below are static renderings of [marimo](https://marimo.io) notebooks from the [thermpy repository](https://github.com/AtmaMani/thermpy). The source for each lives in the `notebooks/` folder.

    ## Notebooks

    ### [Exploring radiance in remote sensing](radiance.html)
    The physics behind thermal remote sensing: blackbody radiance, Planck's law, the Stefan-Boltzmann and Wien displacement laws. Start here if you want the background.

    ### [From radiance to temperature](radiance_to_temperature.html)
    How to invert Planck's law with `thermpy`: building a look up table for a sensor band, converting single values and whole images, and what happens to out-of-range values.
    """)


if __name__ == "__main__":
    app.run()
