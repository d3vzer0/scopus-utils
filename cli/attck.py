from utils.attck import MitreAttck
from utils.neograph.crud import (CRUDActor, CRUDTechnique,
    CRUDMalware, CRUDData, CRUDAction, CRUDRelation, CRUDTool)
import typer
import asyncio

app = typer.Typer()

@app.command()
def actors(cti_url: str = typer.Option('https://raw.githubusercontent.com/mitre/cti/master/enterprise-attack/enterprise-attack.json')):
    mitre_attck = asyncio.run(MitreAttck.from_cti(cti_url))
    typer.echo(f'Started import of ATTCK CTI actors')
    for actor in mitre_attck.actors:
         CRUDActor().create(actor.actor)
    typer.echo(f'Finished import of ATTCK CTI actors')


@app.command()
def actions(cti_url: str = typer.Option('https://raw.githubusercontent.com/mitre/cti/master/enterprise-attack/enterprise-attack.json')):
    mitre_attck = asyncio.run(MitreAttck.from_cti(cti_url))
    typer.echo(f'Started import of ATTCK CTI actions')
    for action in mitre_attck.actions:
         CRUDAction().create(action.action)
    typer.echo(f'Finished import of ATTCK CTI actions')


@app.command()
def techniques(cti_url: str = typer.Option('https://raw.githubusercontent.com/mitre/cti/master/enterprise-attack/enterprise-attack.json')):
    mitre_attck = asyncio.run(MitreAttck.from_cti(cti_url))
    typer.echo(f'Started import of ATTCK CTI techniques')
    for technique in mitre_attck.techniques:
        CRUDTechnique().create(technique.technique)
    typer.echo(f'Finished import of ATTCK CTI techniques')


@app.command()
def tools(cti_url: str = typer.Option('https://raw.githubusercontent.com/mitre/cti/master/enterprise-attack/enterprise-attack.json')):
    mitre_attck = asyncio.run(MitreAttck.from_cti(cti_url))
    typer.echo(f'Started import of ATTCK CTI tools')
    for tool in mitre_attck.tools:
        CRUDTool().create(tool.tool)
    typer.echo(f'Finished import of ATTCK CTI tools')


@app.command()
def malware(cti_url: str = typer.Option('https://raw.githubusercontent.com/mitre/cti/master/enterprise-attack/enterprise-attack.json')):
    mitre_attck = asyncio.run(MitreAttck.from_cti(cti_url))
    typer.echo(f'Started import of ATTCK CTI malware')
    for malware in mitre_attck.malware:
        CRUDMalware().create(malware.malware)
    typer.echo(f'Finished import of ATTCK CTI malware')


@app.command()
def datasources(cti_url: str = typer.Option('https://raw.githubusercontent.com/mitre/cti/master/enterprise-attack/enterprise-attack.json')):
    mitre_attck = asyncio.run(MitreAttck.from_cti(cti_url))
    typer.echo(f'Started import of ATTCK CTI datasources')
    for data in mitre_attck.data:
        CRUDData().create(data.data)
    typer.echo(f'Finished import of ATTCK CTI datasources')


@app.command()
def relationships(cti_url: str = typer.Option('https://raw.githubusercontent.com/mitre/cti/master/enterprise-attack/enterprise-attack.json')):
    mitre_attck = asyncio.run(MitreAttck.from_cti(cti_url))
    typer.echo(f'Started import of ATTCK CTI relationships')
    for relation in mitre_attck.relationships:
        CRUDRelation().create(relation)
    typer.echo(f'Finished import of ATTCK CTI relationships')



