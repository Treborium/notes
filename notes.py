import subprocess
import click
import os
from pathlib import Path
import json

MARKDOWN_VIEWER = "vmd"
CONFIG_FILE_NAME = ".config.json"

@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx):
    """Note taking CLI."""
    config_file_path = find_config_file(Path.cwd())
    config_file = read_config_file(config_file_path)
    root_directory = Path(config_file['root'])

    create_index(root_directory)

    if ctx.invoked_subcommand is None:
        # Only open index if invoked without any subcommand
        subprocess.Popen([MARKDOWN_VIEWER, root_directory.joinpath('index.md')])


def find_config_file(path: Path) -> str:
    for file in os.listdir(path):
        file_path = Path(path).joinpath(file)
        if file_path.is_file() and file == CONFIG_FILE_NAME:
            return file_path

    return find_config_file(path.parent)


def read_config_file(path: Path) -> dict:
    with open(path) as config_file:
        return json.load(config_file)


def create_index(root_directory: Path):
    with open(root_directory.joinpath('index.md'), 'w') as index_file:
        index_file.write("# Index\n")

        for root, _, files in os.walk(root_directory):
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


@click.command()
def init():
    """Initializes the current directory as the root directory"""

    with open(CONFIG_FILE_NAME, 'w') as config_file:
        data = { 'root': os.getcwd() }
        json.dump(data, config_file)


cli.add_command(edit)
cli.add_command(init)