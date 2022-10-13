from pathlib import Path
import os
import logging
from pydantic import BaseModel, Field, validator
import json


GRASS_CONFIG = {'GISBASE': r'/usr/local/grass',
                'PYGRASS': r'/usr/local/grass/etc/python',
                'GRASSDATA': r'/grassdata'}

MOUNT = Path(os.environ['mount'])
# MOUNT = Path.cwd()

GRASS_EXTENSION_URL = 'http://svn.osgeo.org/grass/grass-addons/grass7'

logger = logging.getLogger('root')


class PosixPathEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Path):
            # if the obj is uuid, we simply return the value of uuid
            return str(obj)
        return json.JSONEncoder.default(self, obj)


def check_path(path: Path):
    if not path.exists():
        path.mkdir(parents=True, exist_ok=True)


def save_json(data: dict, path: str) -> None:
    with open(path, 'w') as file:
        json.dump(data, file, cls=PosixPathEncoder)


def load_json(path: str) -> dict:
    with open(path, 'r') as file:
        return json.load(file)


class GrassConfig(BaseModel):
    GISBASE: str
    PYGRASS: str
    GRASSDATA: str
    name: str

    @property
    def LOCATION(self):
        return Path(self.GRASSDATA) / self.name


# todo: validate file existence
class Config(BaseModel):
    dem: Path = Field(alias='dem_path')
    name: str = Field(default='run')
    mount: Path = Field(default=MOUNT)
    waterlevel: float = Field(default=5)

    @validator('dem', pre=True)
    def set_path(cls, value):
        return MOUNT / Path(value)

    @property
    def output(self):
        path = self.mount / self.name
        check_path(path)
        return path

    @property
    def logs(self):
        path = self.output / 'logs'
        check_path(path)
        return path

    class Config:
        allow_population_by_field_name = True

if __name__ == "__main__":
    pass