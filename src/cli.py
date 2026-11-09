
import click
import json

import preprocessing


# =====================================================
# GENERAL CLI GROUP
# =====================================================

@click.group()
def cli():
    """Command-line interface for the data preprocessing project."""
    pass


# =====================================================
# 1. CLEAN GROUP
# =====================================================

@cli.group()
def clean():
    """Commands for cleaning data and handling missing values."""
    pass


@clean.command("remove-missing")
@click.argument("values", nargs=-1, type=str)
def remove_missing(values):
    """
    Remove missing values from a list.

    Example:
    python cli.py clean remove-missing 10 20 "" 30
    """
    result = preprocessing.remove_missing_values(list(values))
    click.echo(f"Result: {result}")


@clean.command("fill-missing")
@click.argument("values", nargs=-1, type=str)
@click.option(
    "--fill-value",
    default="0",
    show_default=True,
    help="Value used to replace missing values."
)
def fill_missing(values, fill_value):
    """
    Replace missing values with a specified value.

    Example:
    python cli.py clean fill-missing 10 "" 30 --fill-value 99
    """
    result = preprocessing.fill_missing_values(
        list(values), fill_value
    )
    click.echo(f"Result: {result}")


# =====================================================
# 2. NUMERIC GROUP
# =====================================================

@cli.group()
def numeric():
    """Commands for processing numerical attributes."""
    pass


@numeric.command("normalize")
@click.argument("values", nargs=-1, type=float)
@click.option(
    "--new-min",
    default=0.0,
    show_default=True,
    help="Minimum value of the new range."
)
@click.option(
    "--new-max",
    default=1.0,
    show_default=True,
    help="Maximum value of the new range."
)
def normalize(values, new_min, new_max):
    """
    Normalize numerical values using min-max normalization.

    Example:
    python cli.py numeric normalize 10 20 30 40
    """
    result = preprocessing.normalize(
        list(values), new_min, new_max
    )
    click.echo(f"Result: {result}")


@numeric.command("standardize")
@click.argument("values", nargs=-1, type=float)
def standardize(values):
    """
    Standardize numerical values using the z-score method.

    Example:
    python cli.py numeric standardize 10 20 30 40
    """
    result = preprocessing.standardize(list(values))
    click.echo(f"Result: {result}")


@numeric.command("clip")
@click.argument("values", nargs=-1, type=float)
@click.option(
    "--min-value",
    default=0.0,
    show_default=True,
    help="Minimum value allowed."
)
@click.option(
    "--max-value",
    default=1.0,
    show_default=True,
    help="Maximum value allowed."
)
def clip(values, min_value, max_value):
    """
    Clip numerical values to a specified range.

    Example:
    python cli.py numeric clip -2 0.5 2 --min-value 0 --max-value 1
    """
    result = preprocessing.clip_values(
        list(values), min_value, max_value
    )
    click.echo(f"Result: {result}")


@numeric.command("to-integers")
@click.argument("values", nargs=-1, type=str)
def to_integers(values):
    """
    Convert numerical strings into integers.

    Example:
    python cli.py numeric to-integers 10 abc 20 30
    """
    result = preprocessing.convert_to_integers(list(values))
    click.echo(f"Result: {result}")


@numeric.command("log-transform")
@click.argument("values", nargs=-1, type=float)
def log_transform(values):
    """
    Transform positive numerical values using the natural logarithm.

    Example:
    python cli.py numeric log-transform 1 2 10 100
    """
    result = preprocessing.logarithmic_transform(list(values))
    click.echo(f"Result: {result}")


# =====================================================
# 3. TEXT GROUP
# =====================================================

@cli.group()
def text():
    """Commands for processing textual information."""
    pass


@text.command("tokenize")
@click.argument("input_text", type=str)
def tokenize(input_text):
    """
    Tokenize text into lowercase alphanumeric words.

    Example:
    python cli.py text tokenize "Hello World Python"
    """
    result = preprocessing.tokenize_text(input_text)
    click.echo(f"Result: {result}")


@text.command("remove-punctuation")
@click.argument("input_text", type=str)
def remove_punctuation(input_text):
    """
    Remove punctuation and non-alphanumeric characters from text.

    Example:
    python cli.py text remove-punctuation "Hello, World! 123."
    """
    result = preprocessing.select_alphanumeric(input_text)
    click.echo(f"Result: {result}")


@text.command("remove-stop-words")
@click.argument("input_text", type=str)
@click.option(
    "--stop-word",
    multiple=True,
    help="A stop word to remove. Can be specified multiple times."
)
def remove_stop_words(input_text, stop_word):
    """
    Remove specified stop words from lowercase text.

    Example:
    python cli.py text remove-stop-words "this is a test" --stop-word is --stop-word a
    """
    result = preprocessing.remove_stop_words(
        input_text, list(stop_word)
    )
    click.echo(f"Result: {result}")


# =====================================================
# 4. STRUCT GROUP
# =====================================================

@cli.group()
def struct():
    """Commands for manipulating data structures."""
    pass


@struct.command("shuffle")
@click.argument("values", nargs=-1, type=str)
@click.option(
    "--seed",
    type=int,
    default=None,
    help="Integer seed for reproducible shuffling."
)
def shuffle(values, seed):
    """
    Randomly shuffle a list of values.

    Example:
    python cli.py struct shuffle 10 20 30 40 --seed 42
    """
    result = preprocessing.shuffle_values(list(values), seed)
    click.echo(f"Result: {result}")


@struct.command("flatten")
@click.argument("values", type=str)
def flatten(values):
    """
    Flatten a list of lists into a single list.

    Provide the nested list in JSON format.

    Example:
    python cli.py struct flatten "[[1, 2], [3, 4], [5]]"
    """
    try:
        nested_list = json.loads(values)
        result = preprocessing.flatten_list(nested_list)
        click.echo(f"Result: {result}")
    except (json.JSONDecodeError, TypeError):
        raise click.BadParameter(
            "Please provide a valid JSON list of lists."
        )


@struct.command("unique")
@click.argument("values", nargs=-1, type=str)
def unique(values):
    """
    Remove duplicated values from a list.

    Example:
    python cli.py struct unique 10 20 10 30 20
    """
    result = preprocessing.remove_duplicates(list(values))
    click.echo(f"Result: {result}")


# =====================================================
# MAIN
# =====================================================

if __name__ == "__main__":
    cli()

