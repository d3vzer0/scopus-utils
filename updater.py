# from utils.products import import_products
# from utils.sentinel import import_sentinel
# from utils.sigma import import_sigma
import cli.attck as attck
import typer
import asyncio

app = typer.Typer()

app.add_typer(attck.app, name="attck")

if __name__ == "__main__":
    app()
