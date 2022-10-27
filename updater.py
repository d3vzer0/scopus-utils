# import cli.attck as attck
# import cli.sigma as sigma
# import cli.sentinel as sentinel
import cli.aws as aws

import typer

app = typer.Typer()

# app.add_typer(attck.app, name="attck")
# app.add_typer(sigma.app, name="sigma")
# app.add_typer(sentinel.app, name="sentinel")
app.add_typer(aws.app, name="aws")

if __name__ == "__main__":
    app()
