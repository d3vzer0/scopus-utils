from pydantic import BaseModel, Field, root_validator, validator
from datetime import datetime
from neo4j import GraphDatabase
import botocore
import boto3
import json

# Example connection, replace this
driver = GraphDatabase.driver('bolt://localhost:7687', auth=('neo4j', 'examplepassshouldgohere'))
client = boto3.client('lambda')

class Node:

    def __run(self, query: str, params: dict = None):
        ''' Execute neo4j query '''
        with driver.session(database='attck') as session:
            result = session.run(query, params)
            return result


    def get(self):
        query = f'MATCH (n:{self.__class__.__name__}) '
        query_params = ''.join([
            f'WHERE n.{key}=${key} ' for key in self.__dict__.keys()
        ])
        return self.__run(f'{query}{query_params} RETURN n', self.__dict__)


    def connect(self, node_classess = None):
        ''' Create relationship between two AWS resource nodes '''
        for relationship in self.relationships:
            if relationship.resource_type in node_classess and relationship.resource_type in self.relationship_types:
                rel_type = self.relationship_types[relationship.resource_type]
                query = f'MATCH (a:{self.__class__.__name__}),(b:{node_classess[relationship.resource_type].__name__}) WHERE a.external_id = $source_id AND b.external_id = $target_id CREATE (a)-[r:{rel_type}]->(b) RETURN type(r)'
        
                query_params = {
                    'target_id': relationship.external_id,
                    'source_id': self.external_id
                }
                self.__run(f'{query}', query_params)


    def save(self):
        ''' Resource AWS resource node '''
        query = f'CREATE (n:{self.__class__.__name__}) '
        set_values = ''.join([
            f'SET n.{key}=${key} ' for key in self.__dict__.keys() if key not in ['relationships', 'relationship_types']
        ])
        query_params = {key: value for key, value in self.__dict__.items() if key not in ['relationships', 'relationship_types']}
        return self.__run(f'{query}{set_values}RETURN n.id', query_params)


class RelationshipItem(BaseModel):
    external_id: str = None
    resource_id:  str = Field(None, alias='resourceId')
    name:  str = Field(default=None, alias='resourceName')
    resource_type: str = Field(..., alias='resourceType')
    relationship_type: str = Field(..., alias='name')

    @validator('external_id')
    def set_external_id(cls, value, values, **kwargs):
        value = value if value else \
            f'{values["resource_type"]}{values["resource_id"]}{values["name"]}'
        return value


class ConfigItem(BaseModel):
    external_id: str = Field(None, unique=True)
    resource_id:  str = Field(None, alias='resourceId', unique=True)
    snapshot_date: str = Field(..., alias='configurationItemCaptureTime')
    creation_date: str = Field(default=None, alias='resourceCreationTime')
    zone: str = Field(default=None, alias='availabilityZone')
    region: str = Field(..., alias='awsRegion')
    name:  str = Field(default=None, alias='resourceName')
    resource_type:  str = Field(..., alias='resourceType')
    account: str = Field(..., alias='awsAccountId')
    arn: str = Field(default=None, alias='ARN')
    relationships: list[RelationshipItem] = Field(None, alias='relationships')


class BaseAWSResource(BaseModel):
    external_id: str =  Field(None, unique=True)
    resource_id:  str = Field(None, alias='resourceId', unique=True)
    snapshot_date: str = Field(..., alias='configurationItemCaptureTime')
    creation_date: str = Field(default=None, alias='resourceCreationTime')
    zone: str = Field(default=None, alias='availabilityZone')
    region: str = Field(..., alias='awsRegion')
    name:  str = Field(default=None, alias='resourceName')
    resource_type:  str = Field(..., alias='resourceType')
    account: str = Field(..., alias='awsAccountId')
    arn: str = Field(default=None, alias='ARN')
    relationships: list[RelationshipItem] = Field(None, alias='relationships')

    @validator('external_id')
    def set_external_id(cls, value, values, **kwargs):
        value = value if value else \
            f'{values["resource_type"]}{values["resource_id"]}{values["name"]}'
        return value


class AWS_CloudWatch_Alarm(BaseAWSResource, Node):
    __alias__ = 'AWS::CloudWatch::Alarm'
    __type__ = 'AWSResource'

    relationship_types: dict[str, str] = None

    @validator('relationship_types', pre=True, always=True)
    def set_relationship_types(cls, value):
        value = { }
        return value


class AWS_CodeDeploy_DeploymentConfig(BaseAWSResource, Node):
    __alias__ = 'AWS::CodeDeploy::DeploymentConfig'
    __type__ = 'AWSResource'

    relationship_types: dict[str, str] = None

    @validator('relationship_types', pre=True, always=True)
    def set_relationship_types(cls, value):
        value = { }
        return value


class AWS_CloudTrail_Trail(BaseAWSResource, Node):
    __alias__ = 'AWS::CloudTrail::Trail'
    __type__ = 'AWSResource'

    relationship_types: dict[str, str] = None

    @validator('relationship_types', pre=True, always=True)
    def set_relationship_types(cls, value):
        value = { }
        return value


class AWS_CodeBuild_Project(BaseAWSResource, Node):
    __alias__ = 'AWS::CodeBuild::Project'
    __type__ = 'AWSResource'

    relationship_types: dict[str, str] = None

    @validator('relationship_types', pre=True, always=True)
    def set_relationship_types(cls, value):
        value = {'AWS::IAM::Role': 'is_associated_with_role' }
        return value


class AWS_CloudFormation_Stack(BaseAWSResource, Node):
    __alias__ = 'AWS::CloudFormation::Stack'
    __type__ = 'AWSResource'

    relationship_types: dict[str, str] = None

    @validator('relationship_types', pre=True, always=True)
    def set_relationship_types(cls, value):
        value = {'AWS::IAM::Role': 'contains_' }
        return value


class AWS_EC2_RouteTable(BaseAWSResource, Node):
    __alias__ = 'AWS::EC2::RouteTable'
    __type__ = 'AWSResource'

    relationship_types: dict[str, str] = None

    @validator('relationship_types', pre=True, always=True)
    def set_relationship_types(cls, value):
        value = {'AWS::EC2::VPC': 'is_contained_in_vpc','AWS::EC2::Subnet': 'contains_subnet' }
        return value


class AWS_DynamoDB_Table(BaseAWSResource, Node):
    __alias__ = 'AWS::DynamoDB::Table'
    __type__ = 'AWSResource'

    relationship_types: dict[str, str] = None

    @validator('relationship_types', pre=True, always=True)
    def set_relationship_types(cls, value):
        value = { }
        return value


class AWS_EC2_NetworkInterface(BaseAWSResource, Node):
    __alias__ = 'AWS::EC2::NetworkInterface'
    __type__ = 'AWSResource'

    relationship_types: dict[str, str] = None

    @validator('relationship_types', pre=True, always=True)
    def set_relationship_types(cls, value):
        value = {'AWS::EC2::SecurityGroup': 'is_associated_with_securitygroup','AWS::EC2::Subnet': 'is_contained_in_subnet','AWS::EC2::VPC': 'is_contained_in_vpc' }
        return value


class AWS_EC2_NetworkAcl(BaseAWSResource, Node):
    __alias__ = 'AWS::EC2::NetworkAcl'
    __type__ = 'AWSResource'

    relationship_types: dict[str, str] = None

    @validator('relationship_types', pre=True, always=True)
    def set_relationship_types(cls, value):
        value = {'AWS::EC2::Subnet': 'is_attached_to_subnet','AWS::EC2::VPC': 'is_contained_in_vpc' }
        return value


class AWS_EC2_FlowLog(BaseAWSResource, Node):
    __alias__ = 'AWS::EC2::FlowLog'
    __type__ = 'AWSResource'

    relationship_types: dict[str, str] = None

    @validator('relationship_types', pre=True, always=True)
    def set_relationship_types(cls, value):
        value = { }
        return value


class AWS_EC2_InternetGateway(BaseAWSResource, Node):
    __alias__ = 'AWS::EC2::InternetGateway'
    __type__ = 'AWSResource'

    relationship_types: dict[str, str] = None

    @validator('relationship_types', pre=True, always=True)
    def set_relationship_types(cls, value):
        value = {'AWS::EC2::VPC': 'is_attached_to_vpc' }
        return value


class AWS_IAM_Group(BaseAWSResource, Node):
    __alias__ = 'AWS::IAM::Group'
    __type__ = 'AWSResource'

    relationship_types: dict[str, str] = None

    @validator('relationship_types', pre=True, always=True)
    def set_relationship_types(cls, value):
        value = {'AWS::IAM::User': 'contains_user','AWS::IAM::Policy': 'is_attached_to_customermanagedpolicy' }
        return value


class AWS_IAM_Policy(BaseAWSResource, Node):
    __alias__ = 'AWS::IAM::Policy'
    __type__ = 'AWSResource'

    relationship_types: dict[str, str] = None

    @validator('relationship_types', pre=True, always=True)
    def set_relationship_types(cls, value):
        value = {'AWS::IAM::Role': 'is_attached_to_role','AWS::IAM::User': 'is_attached_to_user','AWS::IAM::Group': 'is_attached_to_group' }
        return value


class AWS_EC2_SecurityGroup(BaseAWSResource, Node):
    __alias__ = 'AWS::EC2::SecurityGroup'
    __type__ = 'AWSResource'

    relationship_types: dict[str, str] = None

    @validator('relationship_types', pre=True, always=True)
    def set_relationship_types(cls, value):
        value = {'AWS::EC2::NetworkInterface': 'is_associated_with_networkinterface','AWS::EC2::VPC': 'is_contained_in_vpc' }
        return value


class AWS_EC2_Subnet(BaseAWSResource, Node):
    __alias__ = 'AWS::EC2::Subnet'
    __type__ = 'AWSResource'

    relationship_types: dict[str, str] = None

    @validator('relationship_types', pre=True, always=True)
    def set_relationship_types(cls, value):
        value = {'AWS::EC2::NetworkAcl': 'is_attached_to_networkacl','AWS::EC2::NetworkInterface': 'contains_networkinterface','AWS::EC2::RouteTable': 'is_contained_in_routetable','AWS::EC2::VPC': 'is_contained_in_vpc' }
        return value


class AWS_EC2_VPC(BaseAWSResource, Node):
    __alias__ = 'AWS::EC2::VPC'
    __type__ = 'AWSResource'

    relationship_types: dict[str, str] = None

    @validator('relationship_types', pre=True, always=True)
    def set_relationship_types(cls, value):
        value = {'AWS::EC2::NetworkAcl': 'contains_networkacl','AWS::EC2::NetworkInterface': 'contains_networkinterface','AWS::EC2::InternetGateway': 'is_attached_to_internetgateway','AWS::EC2::RouteTable': 'contains_routetable','AWS::EC2::SecurityGroup': 'contains_securitygroup','AWS::EC2::Subnet': 'contains_subnet' }
        return value


class AWS_GuardDuty_Detector(BaseAWSResource, Node):
    __alias__ = 'AWS::GuardDuty::Detector'
    __type__ = 'AWSResource'

    relationship_types: dict[str, str] = None

    @validator('relationship_types', pre=True, always=True)
    def set_relationship_types(cls, value):
        value = { }
        return value


class AWS_IAM_Role(BaseAWSResource, Node):
    __alias__ = 'AWS::IAM::Role'
    __type__ = 'AWSResource'

    relationship_types: dict[str, str] = None

    @validator('relationship_types', pre=True, always=True)
    def set_relationship_types(cls, value):
        value = {'AWS::IAM::Policy': 'is_attached_to_customermanagedpolicy' }
        return value


class AWS_KMS_Key(BaseAWSResource, Node):
    __alias__ = 'AWS::KMS::Key'
    __type__ = 'AWSResource'

    relationship_types: dict[str, str] = None

    @validator('relationship_types', pre=True, always=True)
    def set_relationship_types(cls, value):
        value = { }
        return value


class AWS_IAM_User(BaseAWSResource, Node):
    __alias__ = 'AWS::IAM::User'
    __type__ = 'AWSResource'

    relationship_types: dict[str, str] = None

    @validator('relationship_types', pre=True, always=True)
    def set_relationship_types(cls, value):
        value = {'AWS::IAM::Policy': 'is_attached_to_customermanagedpolicy','AWS::IAM::Group': 'is_attached_to_group' }
        return value


class AWS_Lambda_Function(BaseAWSResource, Node):
    __alias__ = 'AWS::Lambda::Function'
    __type__ = 'AWSResource'

    relationship_types: dict[str, str] = None

    @validator('relationship_types', pre=True, always=True)
    def set_relationship_types(cls, value):
        value = {'AWS::IAM::Role': 'is_associated_with_role', 
            'AWS::S3::Bucket': 'invoked_by'}
        return value

    @validator('relationships', pre=True, always=True)
    def get_dynamic_relationships(cls, v, values, **kwargs):
        rel_mapping = { 'lambda:InvokeFunction': 'invoked_by' }
        try:
            get_policy = client.get_policy(
                FunctionName=values['name'])
            policy = json.loads(get_policy['Policy'])
            rels = [{
                'relationship_type': rel_mapping[val['Action']],
                'arn': val['Condition']['ArnLike']['AWS:SourceArn']
            } for val in policy['Statement']]

        # botocore.exceptions.ResourceNotFoundException
        except Exception as err:
            pass

        return rels

    
class AWS_Kinesis_Stream(BaseAWSResource, Node):
    __alias__ = 'AWS::Kinesis::Stream'
    __type__ = 'AWSResource'

    relationship_types: dict[str, str] = None

    @validator('relationship_types', pre=True, always=True)
    def set_relationship_types(cls, value):
        value = { }
        return value


class AWS_RDS_DBClusterSnapshot(BaseAWSResource, Node):
    __alias__ = 'AWS::RDS::DBClusterSnapshot'
    __type__ = 'AWSResource'

    relationship_types: dict[str, str] = None

    @validator('relationship_types', pre=True, always=True)
    def set_relationship_types(cls, value):
        value = {'AWS::RDS::DBCluster': 'is_associated_with_rds_cluster' }
        return value


class AWS_RDS_DBSecurityGroup(BaseAWSResource, Node):
    __alias__ = 'AWS::RDS::DBSecurityGroup'
    __type__ = 'AWSResource'

    relationship_types: dict[str, str] = None

    @validator('relationship_types', pre=True, always=True)
    def set_relationship_types(cls, value):
        value = { }
        return value


class AWS_Redshift_ClusterSnapshot(BaseAWSResource, Node):
    __alias__ = 'AWS::Redshift::ClusterSnapshot'
    __type__ = 'AWSResource'

    relationship_types: dict[str, str] = None

    @validator('relationship_types', pre=True, always=True)
    def set_relationship_types(cls, value):
        value = {'AWS::Redshift::Cluster': 'is_associated_with_cluster' }
        return value


class AWS_Redshift_Cluster(BaseAWSResource, Node):
    __alias__ = 'AWS::Redshift::Cluster'
    __type__ = 'AWSResource'

    relationship_types: dict[str, str] = None

    @validator('relationship_types', pre=True, always=True)
    def set_relationship_types(cls, value):
        value = {'AWS::Redshift::ClusterParameterGroup': 'is_associated_with_clusterparametergroup','AWS::Redshift::ClusterSubnetGroup': 'is_associated_with_clustersubnetgroup','AWS::EC2::SecurityGroup': 'is_associated_with_securitygroup' }
        return value


class AWS_RDS_DBSubnetGroup(BaseAWSResource, Node):
    __alias__ = 'AWS::RDS::DBSubnetGroup'
    __type__ = 'AWSResource'

    relationship_types: dict[str, str] = None

    @validator('relationship_types', pre=True, always=True)
    def set_relationship_types(cls, value):
        value = {'AWS::EC2::Subnet': 'is_associated_with_subnet' }
        return value


class AWS_RDS_DBSnapshot(BaseAWSResource, Node):
    __alias__ = 'AWS::RDS::DBSnapshot'
    __type__ = 'AWSResource'

    relationship_types: dict[str, str] = None

    @validator('relationship_types', pre=True, always=True)
    def set_relationship_types(cls, value):
        value = { }
        return value


class AWS_Redshift_ClusterParameterGroup(BaseAWSResource, Node):
    __alias__ = 'AWS::Redshift::ClusterParameterGroup'
    __type__ = 'AWSResource'

    relationship_types: dict[str, str] = None

    @validator('relationship_types', pre=True, always=True)
    def set_relationship_types(cls, value):
        value = { }
        return value


class AWS_Redshift_ClusterSubnetGroup(BaseAWSResource, Node):
    __alias__ = 'AWS::Redshift::ClusterSubnetGroup'
    __type__ = 'AWSResource'

    relationship_types: dict[str, str] = None

    @validator('relationship_types', pre=True, always=True)
    def set_relationship_types(cls, value):
        value = {'AWS::EC2::Subnet': 'is_associated_with_subnet' }
        return value


class AWS_S3_Bucket_Policy(BaseAWSResource, Node):
    __alias__ = 'AWS::S3::BucketPolicy'
    __type__ = 'AWSCustomResource'

    sid: str
    effect: str
    principle: str
    action: str
    resource: list[str]
    cidition: str
    relationship_types: dict[str, str] = None

    @validator('relationship_types', pre=True, always=True)
    def set_relationship_types(cls, value):
        value = { }
        return value


class AWS_S3_Bucket(BaseAWSResource, Node):
    __alias__ = 'AWS::S3::Bucket'
    __type__ = 'AWSResource'

    relationship_types: dict[str, str] = None

    @validator('relationship_types', pre=True, always=True)
    def set_relationship_types(cls, value):
        value = { 'AWS::S3::BucketPolicy': 'has_policy' }
        return value


class AWS_Route53Resolver_ResolverRuleAssociation(BaseAWSResource, Node):
    __alias__ = 'AWS::Route53Resolver::ResolverRuleAssociation'
    __type__ = 'AWSResource'

    relationship_types: dict[str, str] = None

    @validator('relationship_types', pre=True, always=True)
    def set_relationship_types(cls, value):
        value = { }
        return value


class AWS_SNS_Topic(BaseAWSResource, Node):
    __alias__ = 'AWS::SNS::Topic'
    __type__ = 'AWSResource'

    relationship_types: dict[str, str] = None

    @validator('relationship_types', pre=True, always=True)
    def set_relationship_types(cls, value):
        value = { }
        return value


class AWS_Route53Resolver_ResolverRule(BaseAWSResource, Node):
    __alias__ = 'AWS::Route53Resolver::ResolverRule'
    __type__ = 'AWSResource'

    relationship_types: dict[str, str] = None

    @validator('relationship_types', pre=True, always=True)
    def set_relationship_types(cls, value):
        value = { }
        return value


class AWS_SageMaker_NotebookInstanceLifecycleConfig(BaseAWSResource, Node):
    __alias__ = 'AWS::SageMaker::NotebookInstanceLifecycleConfig'
    __type__ = 'AWSResource'

    relationship_types: dict[str, str] = None

    @validator('relationship_types', pre=True, always=True)
    def set_relationship_types(cls, value):
        value = { }
        return value