# from utils.products import import_products
# from utils.sentinel import import_sentinel
from .utils.sentinel import Sentinel
from cli.utils.neograph.crud import CRUDDetection
import neomodel
import typer
app = typer.Typer()


@app.command()
def detections(path: str = typer.Option('./detections/sentinel')):
    typer.echo(f'Started import of Sentinel rules')
    sentinel = Sentinel.from_path(path)
    for detection in sentinel.detections:
        try:
            CRUDDetection().create(detection.dict())
        except neomodel.exceptions.UniqueProperty:
            pass
        except neomodel.core.DoesNotExist:
            pass
    typer.echo(f'Finished import of Sentinel rules')