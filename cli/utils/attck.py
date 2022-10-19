import json
from typing import Optional
import aiohttp
from pydantic import BaseModel, Field

class Malware(BaseModel):
    cti_id: str = Field(..., alias='id')
    name: str = Field(..., alias='name')
    platforms: list[str] = Field(default=None, alias='x_mitre_platforms')
    aliases: list[str] = Field(default=None, alias='x_mitre_aliases')
    references: list[dict] = Field(..., alias='external_references')
    revoked: bool = False
    description: str 


class Technique(BaseModel):
    cti_id: str = Field(..., alias='id')
    name: str = Field(..., alias='name')
    platforms: list[str] = Field(default=None, alias='x_mitre_platforms')
    aliases: list[str] = Field(default=None, alias='x_mitre_aliases')
    references: list[dict] = Field(..., alias='external_references')
    permissions_required: list[dict] = Field(default=None, alias='external_references')
    data_sources: list[dict] = Field(default=None, alias='external_references')
    kill_chain_phases: list[dict] = Field(..., alias='kill_chain_phases')
    description: str
    revoked: bool = False
    is_subtechnique: bool = Field(default=False, alias='x_mitre_is_subtechnique')


# class Technique:
#     def __init__(self, technique):
#         self.technique = technique

#     @classmethod
#     def from_cti(cls, technique):
#         ''' Format technique to match expected API schema '''
#         technique = { 
#             'cti_id': technique['id'],
#             'name':technique['name'],
#             'technique': technique['external_references'][0]['external_id'],
#             'description': technique['description'],
#             'platforms': [platform for platform in technique['x_mitre_platforms']], 
#             'permissions_required': [permission for permission in technique.get('x_mitre_permissions_required', [])],
#             'data_sources': [datasource for datasource in technique.get('x_mitre_data_sources', [])],
#             'references': technique['external_references'],
#             'kill_chain_phases': [phase['phase_name'] for phase in technique['kill_chain_phases']],
#             'is_subtechnique': technique.get('x_mitre_is_subtechnique', False),
#         }
#         return cls(technique)

#     def set_magma(self, magma_mapping):
#         external_id = self.technique['external_references'][0]['external_id']
#         if external_id in self.magma_mapping:
#             mapped_usecase = self.magma_mapping[external_id]
#             mapped_usecase.pop('external_id')
#             self.technique['magma'] = mapped_usecase

class Tool(BaseModel):
    cti_id: str = Field(..., alias='id')
    name: str = Field(..., alias='name')
    platforms: list[str] = Field(default=None, alias='x_mitre_platforms')
    aliases: list[str] = Field(default=None, alias='x_mitre_aliases')
    references: list[dict] = Field(..., alias='external_references')
    revoked: bool = False
    description: str 


class Action(BaseModel):
    cti_id: str = Field(..., alias='id')
    name: str = Field(..., alias='name')
    references: list[dict] = Field(..., alias='external_references')
    revoked: bool = False
    description: str 


class Data(BaseModel):
    cti_id: str = Field(..., alias='id')
    name: str = Field(..., alias='name')
    description: str 
    revoked: bool = False


class Actor(BaseModel):
    cti_id: str = Field(..., alias='id')
    name: str = Field(..., alias='name')
    description: str = None
    references: list[dict] = Field(..., alias='external_references')
    aliases: list[str] = Field(default=None, alias='x_mitre_aliases')
    revoked: bool = False


class Relationship(BaseModel):
    source_ref: str
    target_ref: str
    relationship_type: str 


class MitreAttck:
    def __init__(self, actors: list[Actor] = None, techniques: list[Technique] = None,
        data: list[Data] = None, tools: list[Tool] = None, actions: list[Action] = None,
        malware: list[Malware] = None, relationships: list[Relationship] = None):
    
        # self.cti_objects = cti_objects
        self.actors = actors
        self.techniques = techniques
        self.actions = actions
        self.data = data
        self.tools = tools
        self.malware = malware
        self.relationships = relationships
 

    @classmethod
    async def from_cti(cls, cti_url='https://raw.githubusercontent.com/mitre/cti/master/enterprise-attack/enterprise-attack.json'):
        # Since github does not return a valid json response header
        # we have to load the response as text first and parse afterwards
        async with aiohttp.ClientSession() as session:
            async with session.get(cti_url) as resp:
                get_entries = await resp.text()

        mapped_objects = {
            'relationship': { 'objects': [], 'type': Relationship },
            'attack-pattern': { 'objects': [], 'type': Technique },
            'intrusion-set': { 'objects': [], 'type': Actor, },
            'malware': { 'objects': [], 'type': Malware },
            'tool': { 'objects': [], 'type': Tool },
            'actions': { 'objects': [], 'type': Action },
            'x-mitre-data-component': { 'objects': [], 'type': Data }
        }

        for entry in json.loads(get_entries)['objects']:
            # if entry.get('revoked', False) == False and 
            if entry['type'] in mapped_objects:
                mapped_entry = mapped_objects[entry['type']]
                mapped_entry['objects'].append(mapped_entry['type'](**entry))
   
        return cls(
            malware=mapped_objects['malware']['objects'],
            techniques=mapped_objects['attack-pattern']['objects'],
            tools=mapped_objects['tool']['objects'],
            actions=mapped_objects['actions']['objects'],
            data=mapped_objects['x-mitre-data-component']['objects'],
            actors=mapped_objects['intrusion-set']['objects'],
            relationships=mapped_objects['relationship']['objects']
        )
    
