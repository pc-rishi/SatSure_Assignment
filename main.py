# IMPORTING THE LIBRARIES
from sentinelsat import SentinelAPI, read_geojson, geojson_to_wkt
from datetime import date
import geopandas as gpd
import rasterio


def download_sentinel_image(username,password,geojson_path,start,end,out_path):
    # PROVIDE YOUR CREDENTIALS
	api = SentinelAPI(username, password, 'https://scihub.copernicus.eu/dhus')


	# PROVIDE YOUR AREA OF INTEREST
	footprint = geojson_to_wkt(read_geojson(geojson_path))


	# POST THE QUERY
	products = api.query(footprint,
	                     date=(start, end),
	                     platformname='Sentinel-2',
	                     cloudcoverpercentage=(0, 30))


	# STORE THE RESULTS IN DATAFRAME
	gdf = api.to_geodataframe(products)

	#SORT IT BY CLOUD COVER TO GET THE BEST FILE
	gdf_sorted = gdf.sort_values(['cloudcoverpercentage'], ascending=[True])
	target=str(gdf_sorted['uuid'].values[0])

	#DOWNLOAD THE FILE
	api.download(target,directory_path=out_path)


#Sample Inputs for the above function

username='user'
password='pass'
geojson_path='D:\sentinel_data\chennai.geojson'
start='20221201'
end='20221231'
out_path='D:\sentinel_data'

download_sentinel_image(username,password,geojson_path,start,end,out_path)

def preprocess_sentinel_image(input_path, output_path,geojson_path, crs):
    #we might need to perform it twice for each band red and NIR
    with rasterio.open(input_path) as src:
        #Load the shapefile to clip
        bbox = gpd.read_file(geojson_path)
        # Clip image to desired bounds
        out_image, out_transform = rasterio.mask.mask(src, bbox.geometry, crop=True)
        out_meta = src.meta.copy()
        
        # Update metadata for clipped image
        out_meta.update({
            "driver": "GTiff",
            "height": out_image.shape[1],
            "width": out_image.shape[2],
            "transform": out_transform,
            "crs": crs['crs']
        })
        
        # Reproject clipped image to desired CRS
        dst_crs = crs['crs']
        transform, width, height = calculate_default_transform(src.crs, dst_crs, src.width, src.height, *src.bounds)
        out_meta.update({
            'crs': dst_crs,
            'transform': transform,
            'width': width,
            'height': height
        })
        
        # Another preprocessing step that would resample the data that kind of gimmicks building pyramid for faster processing
        with rasterio.open(output_path, 'w', **out_meta) as dst:
            for i in range(1, src.count + 1):
                reproject(
                    source=rasterio.band(src, i),
                    destination=rasterio.band(dst, i),
                    src_transform=src.transform,
                    src_crs=src.crs,
                    dst_transform=transform,
                    dst_crs=dst_crs,
                    resampling=Resampling.nearest)

preprocess_sentinel_image("D:\sentinel_data\IMG_DATA\T44PMV_20221216T050219_B04.jp2", "D:\sentinel_data\red_prep.tif",geojson_path,'EPSG:4326')

# Define function to calculate NDVI index from preprocessed Sentinel 2 image
def calculate_ndvi_index(red_band, nir_band):
    with rasterio.open(input_path) as src:
        # Read red and near-infrared bands
        red = rasterio.open(red_band).read()
        nir = rasterio.open(nir_band).read()
        
        # Calculate NDVI index
        ndvi = (nir - red) / (nir + red)

calculate_ndvi_index("D:\sentinel_data\red_prep.tif","D:\sentinel_data\nir_prep.tif")