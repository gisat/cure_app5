from typing import Optional
from pathlib import Path
import os, sys
import logging
from base import GrassConfig
from pydantic import BaseModel

logger = logging.getLogger('root')

try:
    import grass.script.setup as gsetup
    from grass.pygrass.modules import Module
    logger.debug('Grass python library imported successfully')
except ImportError:
    logger.error('Can not import Grass python library')


def set_up_grass(config: GrassConfig) -> None:
    os.environ['GISBASE'] = config.GISBASE
    sys.path.insert(0, config.PYGRASS)
    gsetup.init(config.GISBASE, config.GRASSDATA, config.LOCATION, 'PERMANENT')


class Flood(BaseModel):
    """class responsible for interaction with grassgis"""
    dem_path: Path
    river: Optional[Path]
    output: Path
    name: str
    DTM: str = 'Terrain_model'
    DRAIN: str = 'drain_py2'
    THRESHOLD: int = 10000
    WATERLEVEL: int = -5

    def process(self):
        logger.info('Processing started')

        if self.river:
            logger.info(f'Custom river lines not implemented. Calculation aborted')
            quit()

        # stre depends if river stresm or not.
        stre = 'str_py2'

        logger.info('Calculation initialization')
        logger.info(f'Calculation parameters: \n {self}')
        Module('r.import', input=str(self.dem_path), output='Terrain_model')
        logger.info('Calculation: Terrain model - finished')
        # set computational region

        Module('g.region', raster=self.DTM)
        logger.info('Calculation: Region - finished')

        Module('r.watershed', elevation=self.DTM, accumulation='acc_py3', drainage='drain_py2', stream='str_py2',
               threshold=self.THRESHOLD)
        logger.info('Calculation: Watershed - finished')

        Module('r.stream.distance', stream_rast=stre, direction=self.DRAIN, elevation=self.DTM, method='downstream',
               difference='above_py2')
        logger.info('Calculation: Stream.distance - finished')

        Module('r.lake', elevation='above_py2', water_level=self.WATERLEVEL, lake='flood_py2', seed=stre)
        logger.info('Calculation: Lake - finished')

        # output
        Module('r.out.gdal', input='flood_py2', output=str(self.output), format='GTiff')
        logger.info('Calculation: Output - finished')
