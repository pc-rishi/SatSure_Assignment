# SatSure_Assingment

This repository contains code for downloading Sentinel satellite data, preprocessing the data, and calculating the Normalized Difference Vegetation Index (NDVI) for the selected area of interest.

Getting Started
To use this code, you will need to have Python 3 and several packages installed, including:

NumPy
Pandas
Geopandas
Rasterio
sentinelsat
These can be installed using pip or another package manager. You will also need to sign up for a free account on the Copernicus Open Access Hub in order to access the Sentinel data.

Workflow
The code is organized into three steps:

Download Sentinel Data: This step involves downloading the Sentinel data for the area of interest using the Sentinel API. The code takes in several parameters, including the bounding box coordinates for the area of interest, the date range for the data, and the desired resolution.

Preprocessing: This step involves preprocessing the downloaded Sentinel data by clipping it to the area of interest, masking out clouds and shadows, and applying atmospheric corrections. The resulting preprocessed data is saved as a GeoTIFF file.

NDVI Calculation: This step involves calculating the NDVI for the preprocessed data. The NDVI values are saved as a GeoTIFF file, which can be visualized using GIS software.


Contributing
Contributions are welcome! Please open an issue or pull request for any bug fixes, feature requests, or general improvements.
