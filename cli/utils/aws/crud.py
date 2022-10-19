from cli.utils.neograph.nodes import Actor, Technique, Tool, Malware, Data, Action, Detection, AWSConfigItem
from neomodel import db
from neomodel import config
from neomodel import install_all_labels
import os

config.DATABASE_URL = os.environ["NEO4J_BOLT_URL"]

class CRUDAws:
    def __init__(self, resource_id: str = None):
        self.resource_id = resource_id

    def create(self, config):
        aws_node = AWSConfigItem(**config)
        aws_node.save()
