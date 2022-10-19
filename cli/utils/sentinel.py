
from .reternalapi import ReternalAPI
from pydantic import BaseModel, Field, validator
import glob
import yaml
import asyncio


class SentinelDetection(BaseModel):
    external_id: str = Field(..., alias='id')
    title: str = Field(..., alias='name')
    description: str 
    content: dict
    platform: str = 'sentinel'
    techniques: list = Field(default=None, alias='relevantTechniques') 
    datatypes: list = Field(default=None, alias='requiredDataConnectors')

    @validator('datatypes', pre=True, always=True)
    def set_datatypes(cls, v):
        if v:
            datatypes = [datatype for connector in v if 'dataTypes' in connector for datatype in connector['dataTypes']]
            return datatypes


class Sentinel:
    def __init__(self, config_files = None):
        self.config_files = config_files if config_files else []

    @property
    def detections(self):
        for config in self.config_files:
            with open(config) as yamlfile:
                yaml_object = yaml.load(yamlfile, Loader=yaml.FullLoader)
                yield SentinelDetection(**yaml_object, content=yaml_object)


    @classmethod
    def from_path(cls, path = '../Azure-Sentinel/Detections'):
        config_files = glob.iglob(f'{path}/**/**/*.yaml', recursive=True)
        return cls(config_files)


async def import_sentinel(*args, **kwargs):
    ''' Load sentinel config files and create entry via API '''
    sigma = Sentinel.from_path(kwargs['path'])
    async with ReternalAPI(kwargs['api_url']) as reternal:
        for rule in sigma.rules:
            await reternal.save('/rules/sentinel', rule)


if __name__ == "__main__":
    asyncio.run(import_sentinel())

