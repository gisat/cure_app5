import logging
import click
from base import Config, GrassConfig, save_json, GRASS_CONFIG
from logger import set_logger
from process import set_up_grass, run_app
from preprocess import preprocess_input_raster

@click.command()
@click.option('--dem',  help='Location of the DEM raster relative to the mount volume')
@click.option('--waterlevel', default=5, help='Height of the water level (m)', type=float)
@click.option('--name', default='run', help='Name of the run (default = run)')
@click.option('--bbox', help='Bounding box of AOI in order west, south, east, north. Optional parameter'
                             ' used to clip the DEM extent', nargs=4, type=float)
@click.option('--debug', default=False, help='Debug mode')
def cli(debug, name, dem, waterlevel, bbox):
    # configs
    config = Config(dem=dem, name=name, waterlevel=waterlevel, bbox=bbox)
    grass_config = GrassConfig(**GRASS_CONFIG, name=name)

    # logger
    logger = set_logger('root', config.logs / f'{name}.log')
    if debug:
        logger.setLevel(logging.DEBUG)

    if config.bbox:
        logger.info('Cure App 5: Raster Preprocess')
        preprocess_input_raster(config)

    logger.info('Cure App 5: Save config')
    save_json(config.dict(), 'config.json')
    logger.info('Cure App 5: Set up grass')
    set_up_grass(grass_config=grass_config, config=config)

    logger.info('Cure App 5: Start')

    run_app(location=grass_config.LOCATION)

    logger.info('Cure App 5: End')

