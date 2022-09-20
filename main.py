from cli import cli
from process import GrassConfig, set_up_grass

if __name__ == '__main__':
    cli()
    grass_config = GrassConfig()
    set_up_grass(grass_config)