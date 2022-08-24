from utils.attck import import_attck
# from utils.products import import_products
# from utils.sentinel import import_sentinel
# from utils.sigma import import_sigma
import cli.attck as attck
import typer
import asyncio

app = typer.Typer()

@app.command()
def sigma(api_url: str, path: str = typer.Option('../sigma/rules')):
    typer.echo(f'Started import of SIGMA rules')
    asyncio.run(import_sigma(api_url=api_url, path=path))
    typer.echo(f'Finished import of SIGMA rules')