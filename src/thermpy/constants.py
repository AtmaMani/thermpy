"""Constants used for radiance to thermal modeling."""

# Planck Constant
planck_h = 6.6260693 / 10**34  # J.s Joule second

# velocity of light in m/s
emr_velocity_c = 299792458.0  # m/s

# Boltzmann constant
boltzmann_k = 1.380658 / 10**23  # J/K


# Radiation constants - these are used to simplify blackbody radiance calculation
"""
c1 = 2hc^2 [planck and velocity of light in SI]
c1 = 2*[(6.626* 10^-34)Ws^2] * [(299792458)^2 (m/s)^2]
c1 = 1.1910 * 10^-32 Wm^2

c2 = hc/k [planck, velocity of light divided by Boltzmann constant]
c2 = [6.626 * 10^-34 Ws^2] * [299792458 m/s] / [1.38*10^-23 Ws/K]
c2 = 1.4394 * 10^-10 Km
"""
c1 = 2 * planck_h * (emr_velocity_c**2)
c2 = planck_h * emr_velocity_c / boltzmann_k


# Wavelengths commonly used in thermal remote sensing. The ranges represent wavelength bandwidths
# All units are normalized to micrometers (um). 1 um = 10^-6 m
mwir_l = (3, 5)  # mid-wave IR um
lwir1_l = (5, 8)  # long-wave IR um
lwir2_l = (8, 9.2)  # thermal band 1
lwir3_l = (9.2, 14)  # thermal band 2

# Landsat missions 8, 9 - https://www.usgs.gov/faqs/what-are-band-designations-landsat-satellites
landsat_tirs_b10 = (10.6, 11.19)  # thermal band 10 for TM
landsat_tirs_b11 = (11.5, 12.51)  # thermal band 11 for TM

# Terra and Aqua MODIS thermal emissive bands - https://earthdata.nasa.gov/data/instruments/modis/spectral-bands
modis_b20 = (3.660, 3.840)
modis_b21 = (3.929, 3.989)
modis_b22 = (3.929, 3.989)
modis_b23 = (4.020, 4.080)
modis_b24 = (4.433, 4.498)
modis_b25 = (4.482, 4.549)
modis_b27 = (6.535, 6.895)
modis_b28 = (7.175, 7.475)
modis_b29 = (8.400, 8.700)
modis_b30 = (9.580, 9.880)
modis_b31 = (10.780, 11.280)
modis_b32 = (11.770, 12.270)
modis_b33 = (13.185, 13.485)
modis_b34 = (13.485, 13.785)
modis_b35 = (13.785, 14.085)
modis_b36 = (14.085, 14.385)

# Suomi NPP and NOAA-20 VIIRS thermal bands - https://origin-east-01-www-ospo.woc.noaa.gov/Products/Suites/files/VIIRS_bands_and_bandwidths.pdf
viirs_m12 = (3.61, 3.79)
viirs_m13 = (3.97, 4.13)
viirs_m14 = (8.40, 8.70)
viirs_m15 = (10.26, 11.26)
viirs_m16 = (11.54, 12.49)
viirs_i4 = (3.55, 3.93)  # imagery band
viirs_i5 = (10.50, 12.40)  # imagery band

# Terra ASTER TIR bands - https://www.earthdata.nasa.gov/s3fs-public/2025-12/ASTER_User_Guide_V4.pdf
aster_tir10 = (8.125, 8.475)
aster_tir11 = (8.475, 8.825)
aster_tir12 = (8.925, 9.275)
aster_tir13 = (10.25, 10.95)
aster_tir14 = (10.95, 11.65)

# Sentinel-3 SLSTR thermal channels - https://sentinel.esa.int/web/sentinel/user-guides/Sentinel-3-slstr/resolutions/radiometric
# ESA publishes center wavelength and bandwidth only. Ranges below are derived as center ± bandwidth/2.
slstr_s7 = (3.543, 3.941)  # center 3.742, bandwidth 0.398
slstr_s8 = (10.466, 11.242)  # center 10.854, bandwidth 0.776
slstr_s9 = (11.570, 12.475)  # center 12.0225, bandwidth 0.905

# GOES-R series ABI thermal bands - https://rammb2.cira.colostate.edu/research/goes-r/goes-r_abi_bands_and_bandwidths/
abi_b07 = (3.80, 4.00)
abi_b08 = (5.77, 6.60)
abi_b09 = (6.75, 7.15)
abi_b10 = (7.24, 7.44)
abi_b11 = (8.30, 8.70)
abi_b12 = (9.42, 9.80)
abi_b13 = (10.10, 10.60)
abi_b14 = (10.80, 11.60)
abi_b15 = (11.80, 12.80)
abi_b16 = (13.00, 13.60)
