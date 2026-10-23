# thermpy
Thermal image processing tooling - radiance to temperature conversion. 

## Some history
This repository has been unearthed from an earlier, archived repository hosted on **Google Code** back in 2011. Google Code has since been shut down. Over the course of time, Python and the scientific Python ecosystem has evolved quite a bit. The syntax, libraries of this project relied on Python 2, which has since been entirely discontinued. Hence, this project has been rewritten to work with modern tools.

## What it does
In thermal remote sensing, sensors such as infrared cameras don't capture temperature directly. Rather, they record radiance - or radiant temperature. This project helps convert radiant temperature to kinetic temperature - the physical temperature we feel when we touch and use in all practical cases. This project uses numerical methods and develops algorithms to perform Plank's law calculations.

You can use this library `thermpy` to convert a list of radiance values to temperatures. You can also provide it a path to an image file and conver the entire image from radiance values to temperatures.

