import subprocess
import click

@click.command()
def notes():
    """Note taking CLI."""
    subprocess.Popen(["vmd", "index.md"])

if __name__ == '__main__':
    notes()