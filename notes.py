import subprocess
import click
import os
import pathlib

MARKDOWN_VIEWER = "vmd"

@click.command()
def notes():
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

            depth = root.count('/') + 1

            if os.path.basename(root) != '.':
                # Don't list root directoy as heading
                index.write(f"{'#' * depth} {os.path.basename(root)}\n")

            for file in files:
                name, extension = file.split('.')
                if extension != 'md':
                    continue
                
                name = name.replace('-', ' ').title()
                index.write(f"- [{name}]({root}/{file})\n")


if __name__ == '__main__':
    notes()