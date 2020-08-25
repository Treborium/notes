# Minimalistic Note-Taking CLI

## Installation

1. Clone this repository and `cd` into it

   ```bash
   git clone https://github.com/Treborium/notes
   cd notes
   ```

2. Install the CLI for the current user

   ```bash
   pip install --user .
   ```

## Development

1. Clone this repository and `cd` into it

   ```bash
   git clone https://github.com/Treborium/notes
   cd notes
   ```

2. Create a virtual python environment and activate it

   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

3. Install requirements

   ```bash
   pip install -r requirements.txt
   ```


## Future Features

- [x] open/edit files from anywhere inside the notes directory with
      `notes edit <file_name>`
- [x] when calling `notes edit <file_name>` also spawn a _vmd_ window in
      addition to the default text editor
- [x] list all files in the console to quickly see what's available `notes list`
- [ ] add support for autocomplete with for example `fzf`
- [ ] ignore certain folders, files or file extensions (same as `.gitignore`)
- [ ] automaticaly link to topics/notes/files that already exist based on their
      name or maybe tags
- [ ] auto create ToC for a selection of files
