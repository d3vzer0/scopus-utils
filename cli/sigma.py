# from utils.products import import_products
# from utils.sentinel import import_sentinel
from cli.utils.sigma import Sigma
from cli.utils.neograph.crud import CRUDDetection
import typer

app = typer.Typer()

@app.command()
def rules(path: str = typer.Option('./detections/sigma')):
    typer.echo(f'Started import of SIGMA rules')
    sigma = Sigma.from_path(path)
    for rule in sigma.rules:
        CRUDDetection().create(rule)
    typer.echo(f'Finished import of SIGMA rules')