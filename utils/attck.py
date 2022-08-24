import json
import aiohttp
import asyncio
import neomodel

class Technique:
    def __init__(self, technique):
        self.technique = technique

    @classmethod
    def from_cti(cls, technique):
        ''' Format technique to match expected API schema '''
        technique = { 
            'cti_id': technique['id'],
            'name':technique['name'],
            'technique': technique['external_references'][0]['external_id'],
            'description': technique['description'],
            'platforms': [platform for platform in technique['x_mitre_platforms']], 
            'permissions_required': [permission for permission in technique.get('x_mitre_permissions_required', [])],
            'data_sources': [datasource for datasource in technique.get('x_mitre_data_sources', [])],
            'references': technique['external_references'],
            'kill_chain_phases': [phase['phase_name'] for phase in technique['kill_chain_phases']],
            'is_subtechnique': technique.get('x_mitre_is_subtechnique', False),
        }
        return cls(technique)

    def set_magma(self, magma_mapping):
        external_id = self.technique['external_references'][0]['external_id']
        if external_id in self.magma_mapping:
            mapped_usecase = self.magma_mapping[external_id]
            mapped_usecase.pop('external_id')
            self.technique['magma'] = mapped_usecase



class Malware:
    def __init__(self, malware):
        self.malware = malware

    @classmethod
    def from_cti(cls, malware):
        malware = {
            'cti_id': malware['id'],
            'name': malware['name'],
            'platforms': malware.get('x_mitre_platforms'),
            'aliases': malware.get('x_mitre_aliases'),
            'references': malware['external_references'],
            'description': malware['description']
        }
        return cls(malware)


class Tool:
    def __init__(self, tool):
        self.tool = tool

    @classmethod
    def from_cti(cls, tool):
        tool = {
            'cti_id': tool['id'],
            'name': tool['name'],
            'platforms': tool.get('x_mitre_platforms'),
            'aliases': tool.get('x_mitre_aliases'),
            'references': tool['external_references'],
            'description': tool['description']
        }
        return cls(tool)

class Action:
    def __init__(self, action):
        self.action = action

    @classmethod
    def from_cti(cls, action):
        action = {
            'cti_id': action['id'], 
            'name': action['name'],
            'references': action['external_references'],
            'description': action['description']
        }
        return cls(action)

class Data:
    def __init__(self, data):
        self.data = data

    @classmethod
    def from_cti(cls, data):
        data = {
            'cti_id': data['id'], 
            'name': data['name'],
            'description': data['description']
        }
        return cls(data)

class Actor:
    def __init__(self, actor):
        self.actor = actor

    @classmethod
    def from_cti(cls, actor):
        actor = {
            'cti_id': actor['id'], 
            'name': actor['name'],
            'references': actor['external_references'],
            'aliases': [alias for alias in \
                actor.get('aliases', [])],
            'description': actor.get('description', None),
        }
        return cls(actor)


class Relationship:
    def __init__(self, relationship):
        self.relationship = relationship

    @classmethod
    def from_cti(cls, relationship):
        relationship = {
            'source_ref': relationship['source_ref'], 
            'target_ref': relationship['target_ref'],
        }
        return cls(relationship)

class MitreAttck:
    def __init__(self, cti_objects = None):
        self.cti_objects = cti_objects
 
    @property 
    def data(self):
        for entry in self.cti_objects:
            if entry['type'] == 'x-mitre-data-component':
                yield Data.from_cti(entry)

    @property
    def actions(self):
        for entry in self.cti_objects:
            if entry['type'] == 'course-of-action':
                yield Action.from_cti(entry)

    @property
    def tools(self):
        for entry in self.cti_objects:
            if entry['type'] == 'tool':
                yield Tool.from_cti(entry)

    @property
    def malware(self):
        for entry in self.cti_objects:
            if entry['type'] == 'malware':
                yield Malware.from_cti(entry)

    @property
    def actors(self):
        for entry in self.cti_objects:
            if entry['type'] == 'intrusion-set':
                    yield Actor.from_cti(entry)
    @property
    def techniques(self):
        for entry in self.cti_objects:
            if entry['type'] == 'attack-pattern':
                yield Technique.from_cti(entry)

    @property
    def relationships(self):
        for entry in self.cti_objects:
            if entry['type'] == 'relationship':
                yield entry


    @classmethod
    async def from_cti(cls, cti_url='https://raw.githubusercontent.com/mitre/cti/master/enterprise-attack/enterprise-attack.json'):
        # Since github does not return a valid json response header
        # we have to load the response as text first and parse afterwards
        async with aiohttp.ClientSession() as session:
            async with session.get(cti_url) as resp:
                get_entries = await resp.text()

        cti_objects = []
        for entry in json.loads(get_entries)['objects']:
            if entry.get('revoked', False) == False:
                cti_objects.append(entry)
   
        return cls(cti_objects=cti_objects)
    
