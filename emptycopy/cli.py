#!/usr/bin/env python
import click
import pathlib


@click.command()
@click.argument(
    "source",
    type=click.Path(
        exists=True,
        file_okay=True,
        dir_okay=True,
        readable=True,
        path_type=pathlib.Path,
    ),
)
@click.argument(
    "target",
    required=False,
    type=click.Path(file_okay=False, dir_okay=True, path_type=pathlib.Path),
)
@click.option("--depth", "-d", type=int, default=0, help="Max depth to copy")
@click.version_option()
@click.help_option()
def cli(source: pathlib.Path, target: pathlib.Path | None, depth: int) -> None:
    """Makes a complete copy of a directory and all it's subdirectories but with
    all files empty."""
    source = source.absolute()
    if not target:
        # if no target is provided, create a new directory with 'empty' prefix
        target = source.with_name(f"empty_{source.name}")
    if not target.exists():
        # if the target directory does not exist, create it
        target.mkdir()

    main(source, target, depth)


def main(source: pathlib.Path, target: pathlib.Path | None, depth) -> None:
    if not source.exists():
        # can't copy what doesn't exist
        raise FileNotFoundError(f"Source {source} does not exist")

    if source.is_file():
        # just copy the file but empty
        target.touch()

    if source.is_dir():
        # copy the directory and all it's subdirectories
        breadth_first_copy(source, target, depth)


def breadth_first_copy(source: pathlib.Path, target: pathlib.Path, depth: int):
    # create the target directory
    target.mkdir(exist_ok=True)

    # create a queue of directories to copy, starting at depth 0
    queue = [(source, target, 0)]

    while queue:
        source_dir, target_dir, current_depth = queue.pop(0)

        # If the current depth exceeds the maximum depth, skip further processing
        if depth != 0 and current_depth >= depth:
            continue

        for source_child in source_dir.iterdir():
            target_child = target_dir / source_child.name

            if source_child.is_file():
                # just copy the file but empty
                target_child.touch()

            if source_child.is_dir():
                # create the target directory
                target_child.mkdir(exist_ok=True)

                # add the directory to the queue with incremented depth
                queue.append((source_child, target_child, current_depth + 1))
