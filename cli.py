import logging
import click
from base import Config, GrassConfig, save_json, GRASS_CONFIG
from logger import set_logger
from process import set_up_grass, run_app, Flood
import json

# todo: upravit tvorbu adresa5u v grassdata
@click.command()
@click.option('--dem',  help='Location of the DEM raster relative to the mount volume')
@click.option('--name', default='run', help='Name of the run (default = run)')
@click.option('--debug', default=False, help='Debug mode')
def cli(debug, name, dem):
    # configs
    config = Config(dem=dem, name=name)
    grass_config = GrassConfig(**GRASS_CONFIG, name=name)

    # logger
    logger = set_logger('root', config.logs / f'{name}.log')
    if debug:
        logger.setLevel(logging.DEBUG)

    logger.info('Cure App 5: Save config')
    save_json(config.dict(), 'config.json')

    logger.info('Cure App 5: Set up grass')
    set_up_grass(grass_config=grass_config, config=config)

    logger.info('Cure App 5: Start')
    # flood = Flood(dem=config.dem, output=config.output, name=config.name)
    # flood.process()

    run_app(location=grass_config.LOCATION)

    logger.info('Cure App 5: End')

