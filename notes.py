import json
import os
import subprocess
import signal
import threading
from pathlib import Path

import click
from bullet import Bullet

MARKDOWN_VIEWER = "vmd"
CONFIG_FILE_NAME = ".config.json"


@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx):
    """Note taking CLI."""
    config_file = get_config()
    root_directory = Path(config_file['root'])

    create_index(root_directory)

    if ctx.invoked_subcommand is None:
        # Only open index if invoked without any subcommand
        subprocess.Popen(
            [MARKDOWN_VIEWER, root_directory.joinpath('index.md')])


def get_config() -> dict:
    config_path = find_config_file(Path.cwd())
    return read_config_file(config_path)


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
        for root, _, files in os.walk(root_directory):
            depth = root.count('/') - str(root_directory).count('/') + 1

            # Don't list root directoy as heading
            if os.path.basename(root) != '.':
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
@click.argument('file_name',)
@click.option('--no-preview', is_flag=True, help="Don't open markdown preview along with editor")
def edit(file_name, no_preview):
    """Open FILE_NAME in the default system editor

    FILE_NAME is the exact name of the file to open
    """
    if '.md' not in file_name:
        file_name = file_name + '.md'

    if not os.path.isfile(file_name):
        possible_files = find_possible_files(file_name)
        file_name = select_file(possible_files)

    open_file_in_editor(file_name, not no_preview)


def find_possible_files(file_name: str) -> list:
    config = get_config()
    possible_files = list()
    for root, _, files in os.walk(Path(config['root'])):
        if file_name in files:
            possible_files.append(f"{root}/{file_name}")
    return possible_files


def select_file(files: list) -> str:
    if len(files) == 0:
        raise FileNotFoundError(f"Could not find file.")
    elif len(files) == 1:
        return files[0]

    # Start bullet selection and return choice
    return Bullet(
        prompt='Please select which file to open:',
        choices=files).launch()


def open_file_in_editor(file_path: str, open_preview=True):
    if open_preview:
        vmd_process = subprocess.Popen([MARKDOWN_VIEWER, file_path])

    subprocess.run([os.environ['EDITOR'], file_path])

    if open_preview:
        os.killpg(os.getpgid(vmd_process.pid), signal.SIGTERM)


@click.command()
@click.option('-i', '--interactive', is_flag=True, help='list files in interactive prompt and start selected file in default editor')
def ls(interactive):
    """List all files"""
    config = get_config()
    all_files = list()
    for root, _, files in os.walk(Path(config['root'])):
        all_files += [f"{root}/{file}" for file in files]

    sorted_files = sorted(all_files)
    format_row = "{}\n" * (len(sorted_files) + 1)
    if interactive:
        choice = Bullet(
            prompt='Select file to open in editor',
            choices=sorted_files).launch()
        open_file_in_editor(choice)
    else:
        format_row = "{}\n" * (len(sorted_files) + 1)
        print(format_row.format("", *sorted_files))


@click.command()
def init():
    """Initializes the current directory as the root directory"""

    with open(CONFIG_FILE_NAME, 'w') as config_file:
        data = {'root': os.getcwd()}
        json.dump(data, config_file)


cli.add_command(edit)
cli.add_command(init)
cli.add_command(ls)
