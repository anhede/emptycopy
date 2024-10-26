# Emptycopy
Emptycopy is a Python CLI-tool that copies the contents of a folder and it's subfolder but leaves the files empty. It's useful for generating folder hierarchies for code tests or for examining how a command will affect a folder without actually changing the files.

For example, the following folder structure:
```bash
$ tree -h my_folder/
[4.0K]  my_folder/
├── [ 21K]  file1.txt
├── [ 59K]  file2.jpg
└── [4.0K]  subfolder
    └── [510K]  file3.mp4

1 directory, 3 files
```
Becomes
```bash
$ tree -h empty_my_folder/
[4.0K]  empty_my_folder/
├── [   0]  file1.txt
├── [   0]  file2.jpg
└── [4.0K]  subfolder
    └── [   0]  file3.mp4

1 directory, 3 files
```

## Installation
### pipx (Recommended)
Emptycopy can be installed using pipx, which is a tool to install Python CLI tools in isolated environments. This is the recommended way to install Emptycopy as it will not interfere with other Python packages on your system.
```bash
pipx install emptycopy
```

### pip
Emptycopy can also be installed using pip, which is the Python package installer. This is not recommended as it will install Emptycopy globally on your system and may interfere with other Python packages.
```bash
pip install emptycopy
```

## Usage
Once installed, Emptycopy can be run from the command line. The basic usage is as follows:
```bash
emptycopy <source> <destination>
```
Where `<source>` is the path to the folder you want to copy and `<destination>` is the path to the new folder where the contents will be copied. If you omit the `<destination>` argument, Emptycopy will create a new folder with the same name and path as the source folder with an `empty_` prefix.

### Depth limit
You can limit the depth of the folder hierarchy that Emptycopy will copy by using the `--depth` or `-d` flag. For example, to copy only the top-level files and folders, you can run:
```bash
emptycopy --depth 1 <source> <destination>
```

## Developers
If you want to contribute to Emptycopy, you can clone the repository and install the development dependencies using poetry. Remember to use the `--with=dev` flag to install the development dependencies.
```bash
git clone
cd emptycopy
poetry install --with=dev   # Installs dev dependencies.
poetry run emptycopy --help # Run the tool!
```

## License
Emptycopy is licensed under the MIT License. See [LICENSE](LICENSE) for more information.