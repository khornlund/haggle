import click

from haggle.app import main


@click.group()
def cli():
    """Command line interface for Haggle web app"""
    pass


@cli.command()
@click.option('-h', '--host', type=str, default='0.0.0.0', help='IP Address to host webapp')
@click.option('-p', '--port', type=int, default=5000, help='Port to host webapp')
@click.option('-e', '--elasticsearch-host', type=str, default='es',
              help='Host address of Elasticsearch database')
@click.option('-d', '--debug', is_flag=True, default=False, help='Flag to run in debug mode')
def webapp(host, port, elasticsearch_host, debug):
    """CLI to start the Flask web app"""
    main(host, port, elasticsearch_host, debug)
