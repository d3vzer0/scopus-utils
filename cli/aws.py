from cli.utils.aws.loader import AWS
from cli.utils.aws.nodes import Node
# from jinja2 import Template
# from cli.utils.neograph.crud import (CRUDAws)
import typer
import os
from collections import defaultdict
from neo4j import GraphDatabase

app = typer.Typer()



# Only used for development, generates a dynamic model template based on the AWS Config json
# @app.command()
# def nodegen(config_path: str, template_path: str = './cli/templates/awsnodes.py.j2'):
#     aws_resources = AWS.node_models(config_path)
#     unique_types = {}
#     typer.echo(f'Generating node models for AWS resources')
#     for resource in aws_resources:
#         if not resource.resource_type in unique_types:
#             unique_types[resource.resource_type] = {}
        
#         for relationship in resource.relationships:
#             unique_types[resource.resource_type][relationship.resource_type] = relationship.relationship_type

#     with open(template_path, 'r') as template_file:
#         template_object = Template(template_file.read())
#         template_rendered = template_object.render(resources=unique_types)

#     typer.echo(template_rendered)


@app.command()
def constraints():
    aws_resources = AWS.node_classess()

    driver = GraphDatabase.driver(os.getenv('NEO_URI','bolt://localhost:7687'),
        auth=(os.getenv('NEO_USER', 'neo4j'), os.getenv('NEO_PASS')))
    for property, config in aws_resources.items():
        query = f'CREATE CONSTRAINT FOR (n:{config.__name__}) REQUIRE n.external_id IS UNIQUE'
        with driver.session(database='attck') as session:
            result = session.run(query)


@app.command()
def from_file(config_path: str):
    aws_resources = AWS.from_config_file(config_path)
   
    typer.echo(f'Started import of AWS resource nodes')
    for resource in aws_resources.resources:
        resource.save()

    typer.echo(f'Started creating relationships between AWS resource nodes')
    for resource in aws_resources.resources:
        abc = resource.connect(node_classess=AWS.node_classess())
   
    typer.echo(f'Done!')

