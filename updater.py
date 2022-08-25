import cli.attck as attck
import cli.sigma as sigma
import typer

app = typer.Typer()

app.add_typer(attck.app, name="attck")
app.add_typer(sigma.app, name="sigma")

if __name__ == "__main__":
    app()
