from typing import Optional
from pathlib import Path
import os, sys
import logging
from base import GrassConfig, Config, load_json, GRASS_EXTENSION_URL
from pydantic import BaseModel
import grass.script.setup as gsetup
from grass.pygrass.modules import Module
from subprocess import run, CompletedProcess

logger = logging.getLogger('root')

RECODE = """
 -100:0.25:1 
 0.25:0.55:2 
 0.55:1:3
 1:2:4
 2:5:5
"""


def set_location(location: Path, dem: Path) -> None:
    run(['grass78', '-c', str(dem), '-e', str(location)], check=True)


def add_grass_extension(location: Path, extension: str)-> None:
    run(['grass78', f'{str(location / "PERMANENT")}', '--exec', f'g.extension', f'extension={extension}',
         f'url={GRASS_EXTENSION_URL}'], check=True)


def add_grass_extension2(location: Path, extension: str)-> None:
    run(['call', 'g.extension', f'extension="{extension}"'], check=True)


def set_up_grass(grass_config: GrassConfig, config: Config) -> None:
    logger.info('Setup of grass')
    os.environ['GISBASE'] = grass_config.GISBASE
    sys.path.insert(0, grass_config.PYGRASS)
    set_location(location=grass_config.LOCATION, dem=config.dem)
    add_grass_extension(location=grass_config.LOCATION, extension='r.stream.distance')


def run_app(location: Path):
    run(['grass78', f'{str(location / "PERMANENT")}', '--exec', 'python3', '-m', str(Path(__file__).stem)], check=True)


class Flood(BaseModel):
    """class responsible for interaction with grassgis"""
    dem: Path
    output: Path
    name: str
    DTM: str = 'Terrain_model'
    DRAIN: str = 'drain_py2'
    STRE: str = 'str_py2'
    ACUM: str = 'acc_py3'
    THRESHOLD: int = 10000
    WATERLEVEL: int = 5

    def process(self):
        logger.info('Processing started')

        logger.info('Calculation initialization')
        logger.info(f'Calculation parameters: \n {self}')
        Module('r.import', input=str(self.dem), output='Terrain_model', overwrite=True)
        logger.info('Calculation: Terrain model - finished')
        # set computational region

        Module('g.region', raster=self.DTM)
        logger.info('Calculation: Region - finished')

        Module('r.watershed', elevation=self.DTM, accumulation=self.ACUM, drainage=self.DRAIN, stream=self.STRE,
               threshold=self.THRESHOLD, overwrite=True)
        logger.info('Calculation: Watershed - finished')

        Module('r.stream.distance', stream_rast=self.STRE, direction=self.DRAIN, elevation=self.DTM,
               method='downstream', difference='above_py2', overwrite=True)
        logger.info('Calculation: Stream.distance - finished')

        Module('r.lake', elevation='above_py2', water_level=self.WATERLEVEL, lake='flood_py2', seed=self.STRE,
               overwrite=True)
        logger.info('Calculation: Lake - finished')

        Module('r.recode', input='above_py2', output='above_py2_rcls', rules='-', overwrite=True, stdin=RECODE)
        logger.info('Calculation: Recode - finished')

        # output
        # expor - depth raster
        Module('r.out.gdal', input='flood_py2', output=str(self.output / f'{self.name}_DepthHAND.tif'),
               format='GTiff', overwrite=True)

        # expor reclass HAND
        Module('r.out.gdal', input='above_py2_rcls',
               output=str(self.output / f'{self.name}_AP05_FloodExtentHAND.tif'), format='GTiff',
               overwrite=True)
        logger.info('Calculation: Output - finished')


if __name__ == "__main__":
    config = Config(**dict(load_json('config.json')))
    flood = Flood(dem=config.dem, output=config.output, name=config.name)
    flood.process()