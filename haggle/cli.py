import click

from haggle.app import socketio, app


@click.group()
def cli():
    """Command line interface for Haggle web app"""
    pass


@cli.command()
@cli.option('-i', '--ip-address', type=str, help='IP Address to host webapp')
def webapp(ip_address):
    """Run the Flask web app"""
    socketio.run(app, debug=True)


@cli.command()
def start_es():
    """Start elasticsearch"""
    pass


@cli.command()
def stop_es():
    """Stop elasticsearch"""
    pass