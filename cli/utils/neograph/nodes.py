from neomodel import (config, StructuredNode, StringProperty, IntegerProperty,
    UniqueIdProperty, Relationship, RelationshipTo, StructuredRel, RelationshipTo, ArrayProperty, JSONProperty, BooleanProperty)


class Technique(StructuredNode):
    uid = UniqueIdProperty()
    cti_id = StringProperty(unique=True, unique_index=True, required=True)
    technique = StringProperty(unique_index=True)
    name = StringProperty(required=True)
    aliases = ArrayProperty(StringProperty())
    platforms = ArrayProperty(StringProperty())
    description = StringProperty()
    references = ArrayProperty(JSONProperty())
    kill_chain_phases = ArrayProperty(StringProperty())
    is_subtechnique = BooleanProperty()
    data_sources = ArrayProperty(StringProperty())
    permissions_required = ArrayProperty(StringProperty())
    techniques = Relationship('Technique', 'subtechnique')


class Data(StructuredNode):
    uid = UniqueIdProperty()
    cti_id = StringProperty(unique=True, unique_index=True, required=True)
    name = StringProperty(required=True)
    description = StringProperty()
    techniques = RelationshipTo('Technique', 'covers')


class Actor(StructuredNode):
    uid = UniqueIdProperty()
    cti_id = StringProperty(unique=True, unique_index=True, required=True)
    name = StringProperty(required=True)
    aliases = ArrayProperty(StringProperty())
    description = StringProperty()
    references = ArrayProperty(JSONProperty())
    techniques = RelationshipTo('Technique', 'uses')
    tools = RelationshipTo('Tool', 'uses')
    malware = RelationshipTo('Malware', 'uses')


class Action(StructuredNode):
    uid = UniqueIdProperty()
    cti_id = StringProperty(unique=True, unique_index=True, required=True)
    name = StringProperty(unique_index=True, required=True)
    description = StringProperty()
    references = ArrayProperty(JSONProperty())
    techniques = RelationshipTo('Technique', 'mitigates')


class Malware(StructuredNode):
    uid = UniqueIdProperty()
    cti_id = StringProperty(unique=True, unique_index=True, required=True)
    platforms = ArrayProperty(StringProperty())
    aliases = ArrayProperty(StringProperty())
    name = StringProperty(required=True)
    description = StringProperty()
    references = ArrayProperty(JSONProperty())
    techniques = RelationshipTo('Technique', 'uses')


class Tool(StructuredNode):
    uid = UniqueIdProperty()
    cti_id = StringProperty(unique=True, unique_index=True, required=True)
    platforms = ArrayProperty(StringProperty())
    aliases = ArrayProperty(StringProperty())
    name = StringProperty(required=True)
    description = StringProperty()
    references = ArrayProperty(JSONProperty())
    techniques = RelationshipTo('Technique', 'uses')


class Detection(StructuredNode):
    uid = UniqueIdProperty()
    external_id = StringProperty(unique=True, unique_index=True, required=True)
    title = StringProperty(required=True)
    platform = StringProperty(required=True)
    description = StringProperty()
    content = StringProperty(required=True)
    categories = ArrayProperty(StringProperty())
    tags = ArrayProperty(StringProperty())
    techniques = RelationshipTo('Technique', 'detects')
