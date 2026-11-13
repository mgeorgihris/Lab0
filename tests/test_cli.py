
import pytest
from click.testing import CliRunner

from src.cli import cli


# FIXTURE
@pytest.fixture
def runner():
    return CliRunner()


# CLEAN GROUP

def test_remove_missing(runner):
    result = runner.invoke(
        cli, ["clean", "remove-missing", "10", "20", "30"]
    )
    assert result.exit_code == 0
    assert "10" in result.output
    assert "20" in result.output


def test_fill_missing(runner):
    result = runner.invoke(
        cli,
        ["clean", "fill-missing", "10", "", "30", "--fill-value", "99"],
    )
    assert result.exit_code == 0
    assert "99" in result.output


# NUMERIC GROUP

def test_normalize(runner):
    result = runner.invoke(
        cli, ["numeric", "normalize", "0", "5", "10"]
    )
    assert result.exit_code == 0
    assert "0.5" in result.output


def test_standardize(runner):
    result = runner.invoke(
        cli, ["numeric", "standardize", "1", "2", "3"]
    )
    assert result.exit_code == 0
    assert "0.0" in result.output


def test_clip(runner):
    result = runner.invoke(
        cli,
        ["numeric", "clip", "--", "-2", "0.5", "2"]
    )

    assert result.exit_code == 0, result.output

def test_to_integers(runner):
    result = runner.invoke(
        cli, ["numeric", "to-integers", "10", "abc", "20"]
    )
    assert result.exit_code == 0
    assert "[10, 20]" in result.output


def test_log_transform(runner):
    result = runner.invoke(
        cli,
        ["numeric", "log-transform", "--", "1", "0", "-2"]
    )

    assert result.exit_code == 0, result.output

# TEXT GROUP

def test_tokenize(runner):
    result = runner.invoke(
        cli, ["text", "tokenize", "Hello World!"]
    )
    assert result.exit_code == 0
    assert "['hello', 'world']" in result.output


def test_remove_punctuation(runner):
    result = runner.invoke(
        cli, ["text", "remove-punctuation", "Hello, World! 123."]
    )
    assert result.exit_code == 0
    assert "Hello World 123" in result.output


def test_remove_stop_words(runner):
    result = runner.invoke(
        cli,
        [
            "text",
            "remove-stop-words",
            "This is a test",
            "--stop-word",
            "is",
            "--stop-word",
            "a",
        ],
    )
    assert result.exit_code == 0
    assert "this test" in result.output


# STRUCT GROUP

def test_shuffle(runner):
    result = runner.invoke(
        cli,
        ["struct", "shuffle", "10", "20", "30", "--seed", "42"],
    )
    assert result.exit_code == 0
    assert "10" in result.output
    assert "20" in result.output


def test_flatten(runner):
    result = runner.invoke(
        cli, ["struct", "flatten", "[[1, 2], [3, 4]]"]
    )
    assert result.exit_code == 0
    assert "[1, 2, 3, 4]" in result.output


def test_unique(runner):
    result = runner.invoke(
        cli, ["struct", "unique", "10", "20", "10", "30"]
    )
    assert result.exit_code == 0
    assert "['10', '20', '30']" in result.output


# GENERAL CLI

def test_cli_help(runner):
    result = runner.invoke(cli, ["--help"])

    assert result.exit_code == 0
    assert "clean" in result.output
    assert "numeric" in result.output
    assert "text" in result.output
    assert "struct" in result.output

