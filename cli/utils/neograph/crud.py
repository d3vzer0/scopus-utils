from cli.utils.neograph.nodes import Actor, Technique, Tool, Malware, Data, Action, Detection
from neomodel import db
from neomodel import config
from neomodel import install_all_labels
import os

config.DATABASE_URL = os.environ["NEO4J_BOLT_URL"]
install_all_labels()

class CRUDActor:
    def __init__(self, cti_id: str = None):
        self.cti_id = cti_id

    def get_all(self):
        return Actor.nodes.all()

    def create(self, actor):
        actor = Actor(**actor)
        actor.save()


class CRUDTechnique():
    def __init__(self, cti_id: str = None):
        self.cti_id = cti_id

    def get_all(self):
        return Technique.nodes.all()

    def create(self, technique):
        technique = Technique(**technique)
        technique.save()


class CRUDTool():
    def __init__(self, cti_id: str = None):
        self.cti_id = cti_id

    def get_all(self):
        return Tool.nodes.all()

    def create(self, tool):
        tool = Tool(**tool)
        tool.save()


class CRUDMalware():
    def __init__(self, cti_id: str = None):
        self.cti_id = cti_id

    def get_all(self):
        return Malware.nodes.all()

    def create(self, malware):
        malware = Malware(**malware)
        malware.save()


class CRUDAction():
    def __init__(self, cti_id: str = None):
        self.cti_id = cti_id

    def get_all(self):
        return Action.nodes.all()

    def create(self, action):
        action = Action(**action)
        action.save()


class CRUDData():
    def __init__(self, cti_id: str = None):
        self.cti_id = cti_id

    def get_all(self):
        return Data.nodes.all()

    def create(self, data):
        data = Data(**data)
        data.save()


class CRUDDetection():
    def __init__(self, external_id: str = None):
        self.external_id = external_id

    def get_all(self):
        return Malware.nodes.all()

    def create(self, detection):
        detection_node = Detection(**detection)
        detection_node.save()
        if detection['techniques']:
            for technique in detection['techniques']:
                detection_node = Detection.nodes.get(external_id=detection['external_id'])
                technique_node = Technique.nodes.get(technique=technique)
                detection_node.techniques.connect(technique_node)


class CRUDRelation:
    def create(self, relation, cache = None):
        source = relation['source_ref']
        target = relation['target_ref']
        rel = relation['relationship_type']
    
        # If you add enough IF statements it eventually becomes machine learning right?
        # print(cache['uses'])
        if ('malware' in source and 'uses' in rel and 'attack-pattern' in target):
            cache[source].techniques.connect(cache[target])

        # if ('intrusion-set' in source and 'uses' in rel and 'attack-pattern' in target):
        #     cache[source].techniques.connect(cache[target])

        # if ('intrusion-set' in source and 'uses' in rel and 'malware' in target):
        #     cache[source].malware.connect(cache[target])

        # if ('intrusion-set' in source and 'uses' in rel and 'tool' in target):
        #     cache[source].tools.connect(cache[target])

        # if ('tool' in source and 'uses' in rel and 'attack-pattern' in target):
        #     cache[source].techniques.connect(cache[target])

        # if ('x-mitre-data-component' in source and 'detects' in rel and 'attack-pattern' in target):
        #     cache[source].techniques.connect(cache[target])
        
        # if ('attack-pattern' in source and 'subtechnique-of' in rel and 'attack-pattern' in target):
        #     cache[source].techniques.connect(cache[target])
            
        # if ('course-of-action' in source and 'mitigates' in rel and 'attack-pattern' in target):
        #     cache[source].techniques.connect(cache[target])
