import subprocess
import click
import os
import pathlib

MARKDOWN_VIEWER = "vmd"

@click.group(invoke_without_command=True)
def cli():
    """Note taking CLI."""
    create_index()
    subprocess.Popen([MARKDOWN_VIEWER, "index.md"])


def create_index():
    with open('index.md', 'w') as index:
        index.write("# Index\n")

        for root, dirs, files in os.walk('.'):
            if 'venv' in dirs:
                dirs.remove('venv')
            if '.vscode' in dirs:
                dirs.remove('.vscode')
            if '.git' in dirs:
                dirs.remove('.git')
            if 'notes.egg-info' in dirs:
                dirs.remove('notes.egg-info')
            if 'pycache' in dirs:
                dirs.remove('pycache')

            depth = root.count('/') + 1

            if os.path.basename(root) != '.':
                # Don't list root directoy as heading
                index.write(f"{'#' * depth} {os.path.basename(root)}\n")

            for file in files:
                try:
                    name, extension = file.split('.')

                    if extension == 'md':
                        name = name.replace('-', ' ').title()
                        index.write(f"- [{name}]({root}/{file})\n")
                except:
                    continue