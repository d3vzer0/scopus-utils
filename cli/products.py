# @app.command()
# def products(api_url: str, path: str = typer.Option('./mitre/datasource_mapping.json'),
#     access_token: str = typer.Option(..., prompt=True, hide_input=True, envvar="RT_TOKEN")):
#     typer.echo(f'Started import of products and datasource mapping')
#     asyncio.run(import_products(api_url=api_url, path=path, access_token=access_token))
#     typer.echo(f'Finished import of products and datasource mapping')
