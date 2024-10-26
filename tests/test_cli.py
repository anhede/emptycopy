import pytest
from click.testing import CliRunner
from emptycopy.cli import cli


# Helper function to create files and directories for testing
def create_structure(base_dir, structure):
    for path, content in structure.items():
        target_path = base_dir / path
        if content is None:  # directory
            target_path.mkdir(parents=True, exist_ok=True)
        else:  # file
            target_path.parent.mkdir(parents=True, exist_ok=True)
            with target_path.open("w") as f:
                f.write(content)


@pytest.fixture
def setup_tmpdir(tmp_path):
    return tmp_path


def test_copy_directory_with_files_and_subdirs(setup_tmpdir):
    src = setup_tmpdir / "src_dir"
    target = setup_tmpdir / "target_dir"
    structure = {
        "file1.txt": "This is a test file.",
        "subdir1/file2.txt": "Another test file.",
    }
    create_structure(src, structure)

    runner = CliRunner()
    result = runner.invoke(cli, [str(src), str(target)])

    assert result.exit_code == 0
    assert (target / "file1.txt").exists()
    assert (target / "file1.txt").stat().st_size == 0
    assert (target / "subdir1/file2.txt").exists()
    assert (target / "subdir1/file2.txt").stat().st_size == 0


def test_copy_empty_directory(setup_tmpdir):
    src = setup_tmpdir / "empty_dir"
    target = setup_tmpdir / "target_empty_dir"
    src.mkdir()

    runner = CliRunner()
    result = runner.invoke(cli, [str(src), str(target)])

    assert result.exit_code == 0
    assert target.exists()
    assert list(target.iterdir()) == []


def test_copy_nested_directories_with_files(setup_tmpdir):
    src = setup_tmpdir / "nested_dir"
    target = setup_tmpdir / "target_nested_dir"
    structure = {"level1/level2/file3.txt": "Deep nested file."}
    create_structure(src, structure)

    runner = CliRunner()
    result = runner.invoke(cli, [str(src), str(target)])

    assert result.exit_code == 0
    assert (target / "level1/level2/file3.txt").exists()
    assert (target / "level1/level2/file3.txt").stat().st_size == 0


def test_source_path_does_not_exist(setup_tmpdir):
    src = setup_tmpdir / "non_existent_dir"
    target = setup_tmpdir / "target_non_existent"

    runner = CliRunner()
    result = runner.invoke(cli, [str(src), str(target)])

    assert result.exit_code != 0


def test_copy_with_depth_limit(setup_tmpdir):
    src = setup_tmpdir / "dir_with_depth"
    target = setup_tmpdir / "target_with_depth"
    structure = {"level1/level2/file4.txt": "Test file with depth."}
    create_structure(src, structure)

    runner = CliRunner()
    result = runner.invoke(cli, [str(src), str(target), "--depth", "1"])

    assert result.exit_code == 0
    assert (target / "level1").exists()
    assert not (target / "level1/level2/file4.txt").exists()


def test_default_target_directory(setup_tmpdir):
    src = setup_tmpdir / "default_dir"
    structure = {"file5.txt": "Another test file."}
    create_structure(src, structure)

    runner = CliRunner()
    result = runner.invoke(cli, [str(src)])

    assert result.exit_code == 0
    assert (src.parent / f"empty_{src.name}").exists()
    assert (src.parent / f"empty_{src.name}/file5.txt").stat().st_size == 0
