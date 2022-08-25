from utils.attck import import_attck
# from utils.products import import_products
# from utils.sentinel import import_sentinel
# from utils.sigma import import_sigma
import cli.attck as attck
import typer
import asyncio

@app.command()
def sentinel(path: str = typer.Option('../detections/sentinel')):
    typer.echo(f'Started import of Sentinel rules')
    asyncio.run(import_sentinel(api_url=api_url, path=path))
    typer.echo(f'Finished import of Sentinel rules')