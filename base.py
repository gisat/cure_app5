from pathlib import Path
import os
from typing import Optional

from pydantic import BaseModel, Field, validator


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


def check_path(path: Path):
    if not path.exists():
        path.mkdir(parents=True, exist_ok=True)


class GrassConfig(BaseModel):
    GISBASE: str = Field(default=r'/usr/local/grass')
    PYGRASS: str = Field(default=r'/usr/local/grass/etc/python')
    GRASSDATA: str = Field(default=r'/grassdata')
    LOCATION: str = Field(default=r'/grassdata/process')


# todo: validate file existence
class Config(BaseModel):
    dem: Path = Field(alias='dem_path')
    river: Optional[Path] = Field(default=None)
    name: str = Field(default='run')
    mount: Path = Field(default=Path(os.environ['mount']))

    @validator('dem', 'river', pre=True)
    def make_path(cls, value):
        if value is not None:
            return Path(value)

    @property
    def output(self):
        path = self.mount / self.name / 'output'
        check_path(path)
        return path

    @property
    def logs(self):
        path = self.output / 'logs'
        check_path(path)
        return path

    @property
    def dem_path(self):
        return self.mount / self.dem

    class Config:
        allow_population_by_field_name = True

