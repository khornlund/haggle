import click

from haggle.app import socketio, app


@click.group()
def cli():
    """Command line interface for Haggle web app"""
    pass


@cli.command()
# @click.option('-i', '--ip-address', type=str, help='IP Address to host webapp')
def webapp():
    """Run the Flask web app"""
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)


@cli.command()
def start_es():
    """Start elasticsearch"""
    pass


@cli.command()
def stop_es():
    """Stop elasticsearch"""
    pass
