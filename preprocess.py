from pathlib import Path
import rioxarray
from xarray import DataArray
from shapely.geometry import Polygon
from pyproj import Proj, Transformer, CRS
from shapely.ops import transform
from base import BBOX_CRS, Config

def check_crs(raster: DataArray)-> bool:
    return raster.rio.crs == BBOX_CRS


def transform_vector_crs(vector: Polygon, src_crs: CRS, target_crs: CRS) -> Polygon:
    project = Transformer.from_crs(src_crs, target_crs)
    return transform(project.transform, vector)


def load_raster(path: Path) -> DataArray:
    return rioxarray.open_rasterio(path)


def clip_raster(raster: DataArray, bbox: tuple) -> DataArray:
    # return raster.rio.clip([geometry], all_touched=True)
    return raster.rio.clip_box(*bbox, crs="EPSG:4326")


def save_raster(raster: DataArray, path: Path) -> None:
    raster.rio.to_raster(path, compress='LZMA')


def preprocess_input_raster(config: Config):
    raster = load_raster(config.dem)
    clipped = clip_raster(raster, config.bbox)
    config.dem = config.output / 'cliped.tif'
    save_raster(clipped, config.dem)
