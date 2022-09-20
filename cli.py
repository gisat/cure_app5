import logging
import click
from base import Config, GrassConfig
from logger import set_logger
from process import set_up_grass, Flood

@click.command()
@click.option('--debug', default=False, help='Debug mode')
@click.option('--dem',  help='Location of the DEM raster relative to the mount volume')
@click.option('--river', default=None, help='Location of the river streamlines vector '
                                            'layer relative to the mount volume')
@click.option('--name', default='run', help='Name of the run (default = run)')
def cli(debug, name, dem, river):
    # configs
    grass_config = GrassConfig()
    config = Config(dem=dem, river=river, name=name)

    # setup grass
    set_up_grass(grass_config)

    # logger
    logger = set_logger('root', config.logs / f'{name}.log')
    if debug:
        logger.setLevel(logging.DEBUG)
    logger.info('Cure App 5: Start')

    flood = Flood(dem_path=config.dem_path, output=config.output, river=config.river, name=config.name)
    flood.process()
    logger.info('Cure App 5: End')

