import subprocess
import click
import os
import pathlib

@click.command()
def notes():
    """Note taking CLI."""
    index_notes()
    subprocess.Popen(["vmd", "index.md"])


def index_notes():
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
                index.write(f"{'#' * depth} {os.path.basename(root)}\n")

            for file in files:
                name, extension = file.split('.')
                if extension != 'md':
                    continue

                index.write(f"- [{name}]({root}/{file})\n")


if __name__ == '__main__':
    notes()