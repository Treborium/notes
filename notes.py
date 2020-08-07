import subprocess
import click
import os
import pathlib

from rich.console import Console
from rich.markdown import Markdown

MARKDOWN_VIEWER = "vmd"


@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx):
    """Note taking CLI."""
    create_index()

    if ctx.invoked_subcommand is None:
        # Only open index if invoked without any subcommand
        subprocess.Popen([MARKDOWN_VIEWER, "index.md"])


def create_index():
    with open('index.md', 'w') as index_file:
        index_file.write("# Index\n")

        for root, _, files in os.walk('.'):
            depth = root.count('/') + 1

            if os.path.basename(root) != '.':
                # Don't list root directoy as heading
                # Write categories as titles
                index_file.write(f"{'#' * depth} {os.path.basename(root)}\n")

            write_list_of_notes(files, index_file, root)


def write_list_of_notes(files, index_file, root):
    for file in files:
        try:
            name, extension = file.split('.')

            if extension == 'md':
                # Only list markdown files
                name = name.replace('-', ' ').title()
                index_file.write(f"- [{name}]({root}/{file})\n")
        except:
            continue


@click.command()
@click.argument('file_name')
def edit(file_name):
    subprocess.run([os.environ['EDITOR'], file_name])


cli.add_command(edit)
