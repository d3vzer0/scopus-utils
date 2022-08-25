from cli.utils.attck import MitreAttck
from cli.utils.neograph.crud import (CRUDActor, CRUDTechnique,
    CRUDMalware, CRUDData, CRUDAction, CRUDRelation, CRUDTool)
import typer
import neomodel
import asyncio

app = typer.Typer()


@app.command()
def actors(cti_url: str = typer.Option('https://raw.githubusercontent.com/mitre/cti/master/enterprise-attack/enterprise-attack.json'), cti_data=None):
    mitre_attck = cti_data if cti_data else asyncio.run(MitreAttck.from_cti(cti_url))
    typer.echo(f'Started import of ATTCK CTI actors')
    for actor in mitre_attck.actors:
        try:
            CRUDActor().create(actor.actor)
        except neomodel.exceptions.UniqueProperty as exc:
            pass
    typer.echo(f'Finished import of ATTCK CTI actors')


@app.command()
def actions(cti_url: str = typer.Option('https://raw.githubusercontent.com/mitre/cti/master/enterprise-attack/enterprise-attack.json'), cti_data=None):
    mitre_attck = cti_data if cti_data else asyncio.run(MitreAttck.from_cti(cti_url))
    typer.echo(f'Started import of ATTCK CTI actions')
    for action in mitre_attck.actions:
        try:
            CRUDAction().create(action.action)
        except neomodel.exceptions.UniqueProperty as exc:
            pass
    typer.echo(f'Finished import of ATTCK CTI actions')


@app.command()
def techniques(cti_url: str = typer.Option('https://raw.githubusercontent.com/mitre/cti/master/enterprise-attack/enterprise-attack.json'), cti_data=None):
    mitre_attck = cti_data if cti_data else asyncio.run(MitreAttck.from_cti(cti_url))
    typer.echo(f'Started import of ATTCK CTI techniques')
    for technique in mitre_attck.techniques:
        try:
            CRUDTechnique().create(technique.technique)
        except neomodel.exceptions.UniqueProperty as exc:
            pass
    typer.echo(f'Finished import of ATTCK CTI techniques')


@app.command()
def tools(cti_url: str = typer.Option('https://raw.githubusercontent.com/mitre/cti/master/enterprise-attack/enterprise-attack.json'), cti_data = None):
    mitre_attck = cti_data if cti_data else asyncio.run(MitreAttck.from_cti(cti_url))
    typer.echo(f'Started import of ATTCK CTI tools')
    for tool in mitre_attck.tools:
        try:
            CRUDTool().create(tool.tool)
        except neomodel.exceptions.UniqueProperty as exc:
            pass
    typer.echo(f'Finished import of ATTCK CTI tools')


@app.command()
def malware(cti_url: str = typer.Option('https://raw.githubusercontent.com/mitre/cti/master/enterprise-attack/enterprise-attack.json'), cti_data = None):
    mitre_attck = cti_data if cti_data else asyncio.run(MitreAttck.from_cti(cti_url))
    typer.echo(f'Started import of ATTCK CTI malware')
    for malware in mitre_attck.malware:
        try:
            CRUDMalware().create(malware.malware)
        except neomodel.exceptions.UniqueProperty as exc:
            pass
    typer.echo(f'Finished import of ATTCK CTI malware')


@app.command()
def datasources(cti_url: str = typer.Option('https://raw.githubusercontent.com/mitre/cti/master/enterprise-attack/enterprise-attack.json'), cti_data = None):
    mitre_attck = cti_data if cti_data else asyncio.run(MitreAttck.from_cti(cti_url))
    typer.echo(f'Started import of ATTCK CTI datasources')
    for data in mitre_attck.data:
        try:
            CRUDData().create(data.data)
        except neomodel.exceptions.UniqueProperty as exc:
            pass
    typer.echo(f'Finished import of ATTCK CTI datasources')


@app.command()
def relationships(cti_url: str = typer.Option('https://raw.githubusercontent.com/mitre/cti/master/enterprise-attack/enterprise-attack.json'), cti_data = None):
    mitre_attck = cti_data if cti_data else asyncio.run(MitreAttck.from_cti(cti_url))
    typer.echo(f'Started import of ATTCK CTI relationships')
    for relation in mitre_attck.relationships:
        try:
            CRUDRelation().create(relation)
        except Exception as err:
            print(relation)
            print(err)
    typer.echo(f'Finished import of ATTCK CTI relationships')


@app.command()
def all(cti_url: str = typer.Option('https://raw.githubusercontent.com/mitre/cti/master/enterprise-attack/enterprise-attack.json')):
    mitre_attck = asyncio.run(MitreAttck.from_cti(cti_url))
    typer.echo(f'Started import of full ATTCK CTI dataset')
    techniques(cti_data=mitre_attck)
    actors(cti_data=mitre_attck)
    actions(cti_data=mitre_attck)
    malware(cti_data=mitre_attck)
    tools(cti_data=mitre_attck)
    datasources(cti_data=mitre_attck)
    relationships(cti_data=mitre_attck)
    typer.echo(f'Finished import of full ATTCK CTI dataset')



