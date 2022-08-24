from neomodel import (config, StructuredNode, StringProperty, IntegerProperty,
    UniqueIdProperty, Relationship, RelationshipTo, StructuredRel, RelationshipTo, ArrayProperty, JSONProperty, BooleanProperty)


class Technique(StructuredNode):
    cti_id = UniqueIdProperty()
    technique = StringProperty()
    name = StringProperty(unique_index=True, required=True)
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
    cti_id = UniqueIdProperty()
    name = StringProperty(unique_index=True, required=True)
    description = StringProperty()
    techniques = RelationshipTo('Technique', 'detects')


class Actor(StructuredNode):
    cti_id = UniqueIdProperty()
    name = StringProperty(unique_index=True, required=True)
    aliases = ArrayProperty(StringProperty())
    description = StringProperty()
    references = ArrayProperty(JSONProperty())
    techniques = RelationshipTo('Technique', 'uses')
    tools = RelationshipTo('Tool', 'uses')
    malware = RelationshipTo('Malware', 'uses')


class Action(StructuredNode):
    cti_id = UniqueIdProperty()
    name = StringProperty(unique_index=True, required=True)
    description = StringProperty()
    references = ArrayProperty(JSONProperty())
    techniques = RelationshipTo('Technique', 'mitigates')


class Malware(StructuredNode):
    cti_id = UniqueIdProperty()
    platforms = ArrayProperty(StringProperty())
    aliases = ArrayProperty(StringProperty())
    name = StringProperty(unique_index=True, required=True)
    description = StringProperty()
    references = ArrayProperty(JSONProperty())
    techniques = RelationshipTo('Technique', 'uses')


class Tool(StructuredNode):
    cti_id = UniqueIdProperty()
    platforms = ArrayProperty(StringProperty())
    aliases = ArrayProperty(StringProperty())
    name = StringProperty(unique_index=True, required=True)
    description = StringProperty()
    references = ArrayProperty(JSONProperty())
    techniques = RelationshipTo('Technique', 'uses')
