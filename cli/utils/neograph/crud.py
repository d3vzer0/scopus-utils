from utils.neograph.nodes import Actor, Technique, Tool, Malware, Data, Action
from neomodel import db
from neomodel import config
import os

config.DATABASE_URL = os.environ["NEO4J_BOLT_URL"]

class CRUDActor:
    def __init__(self, cti_id: str = None):
        self.cti_id = cti_id

    def create(self, actor):
        actor = Actor(**actor)
        actor.save()


class CRUDTechnique():
    def __init__(self, cti_id: str = None):
        self.cti_id = cti_id

    def create(self, technique):
        technique = Technique(**technique)
        technique.save()


class CRUDTool():
    def __init__(self, cti_id: str = None):
        self.cti_id = cti_id

    def create(self, tool):
        tool = Tool(**tool)
        tool.save()


class CRUDMalware():
    def __init__(self, cti_id: str = None):
        self.cti_id = cti_id

    def create(self, malware):
        malware = Malware(**malware)
        malware.save()


class CRUDAction():
    def __init__(self, cti_id: str = None):
        self.cti_id = cti_id

    def create(self, action):
        action = Action(**action)
        action.save()


class CRUDData():
    def __init__(self, cti_id: str = None):
        self.cti_id = cti_id

    def create(self, data):
        data = Data(**data)
        data.save()


class CRUDRelation:
    def create(self, relation):
        source = relation['source_ref']
        target = relation['target_ref']
        rel = relation['relationship_type']

        # If you add enough IF statements it eventually becomes machine learning right?
        if ('malware' in source and 'uses' in rel and 'attack-pattern' in target):
            malware = Malware.nodes.get(cti_id=source)
            technique = Technique.nodes.get(cti_id=target)
            malware.techniques.connect(technique)

        if ('intrusion-set' in source and 'uses' in rel and 'attack-pattern' in target):
            actor = Actor.nodes.get(cti_id=source)
            technique = Technique.nodes.get(cti_id=target)
            actor.techniques.connect(technique)

        if ('intrusion-set' in source and 'uses' in rel and 'malware' in target):
            actor = Actor.nodes.get(cti_id=source)
            malware = Malware.nodes.get(cti_id=target)
            actor.malware.connect(malware)

        if ('intrusion-set' in source and 'uses' in rel and 'tool' in target):
            actor = Actor.nodes.get(cti_id=source)
            tool = Tool.nodes.get(cti_id=target)
            actor.tools.connect(tool)

        if ('tool' in source and 'uses' in rel and 'attack-pattern' in target):
            tool = Tool.nodes.get(cti_id=source)
            technique = Technique.nodes.get(cti_id=target)
            tool.techniques.connect(technique)

        if ('x-mitre-data-component' in source and 'detects' in rel and 'attack-pattern' in target):
            data = Data.nodes.get(cti_id=source)
            technique = Technique.nodes.get(cti_id=target)
            data.techniques.connect(technique)
        
        if ('attack-pattern' in source and 'subtechnique-of' in rel and 'attack-pattern' in target):
            stechnique = Technique.nodes.get(cti_id=source)
            technique = Technique.nodes.get(cti_id=target)
            stechnique.techniques.connect(technique)
            
        if ('course-of-action' in source and 'mitigates' in rel and 'attack-pattern' in target):
            action = Action.nodes.get(cti_id=source)
            technique = Technique.nodes.get(cti_id=target)
            action.techniques.connect(technique)
