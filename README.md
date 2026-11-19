# Lab0 - Fundamentals of Continuous Integration

This repository contains the code for **Lab 0** of the MLOps course. The goal of the lab is to understand the basic elements of Continuous Integration (CI): linting, code formatting and testing.

The project is a small **data preprocessing application** with a Command Line Interface (CLI) built with [Click](https://click.palletsprojects.com/). It includes functions to clean data, process numerical values, work with text and change the structure of lists.

## Project structure

```
Lab0/
├── src/
│   ├── __init__.py
│   ├── preprocessing.py   # main logic (preprocessing functions)
│   └── cli.py             # command line interface (Click)
├── tests/
│   ├── test_logic.py      # unit tests of preprocessing.py
│   └── test_cli.py        # integration tests of the CLI
├── pyproject.toml
├── uv.lock
└── README.md
```

## Installation

The project uses [uv](https://docs.astral.sh/uv/) to manage the virtual environment and the dependencies.

1. Clone the repository:

```bash
git clone https://github.com/<your-user>/Lab0.git
cd Lab0
```

2. Create the environment and install the dependencies:

```bash
uv sync
```

The dependencies of the project are:

- **click**: to build the CLI
- **black**: to format the code
- **pylint**: to lint the code
- **pytest**: to run the unit and integration tests
- **pytest-cov**: to measure the test coverage

If you start the project from zero, you can create it with `uv init` and add each library with `uv add <library-name>`.

## Functionalities

The functions are implemented in `src/preprocessing.py` and are organized in the CLI in four groups inside the main `cli` group:

| Group | Functions |
|-------|-----------|
| `clean` | Remove missing values (`None`, `''`, `nan`), fill missing values (default 0) |
| `numeric` | Min-max normalization, z-score standardization, clipping, conversion to integers, logarithmic transformation |
| `text` | Tokenization, selection of alphanumeric characters and spaces, removal of stop-words |
| `struct` | Shuffle (with seed), flatten a list of lists, unique values |

## Usage

To see all the groups and commands available:

```bash
uv run python -m src.cli --help
```

To see the commands of one group and their options:

```bash
uv run python -m src.cli numeric --help
```

Some examples:

```bash
# Remove missing values
uv run python -m src.cli clean remove-missing 1 "" 3 None 5

# Fill missing values with 99
uv run python -m src.cli clean fill-missing 1 "" 3 --fill-value 99

# Normalize between -1 and 1
uv run python -m src.cli numeric normalize 1 5 10 --new-min -1 --new-max 1

# Clip values between 0 and 5
uv run python -m src.cli numeric clip 1 7 -2 4 --min-value 0 --max-value 5

# Tokenize a text
uv run python -m src.cli text tokenize "Hello, World! This is MLOps"

# Remove stop-words
uv run python -m src.cli text remove-stopwords "This is a test" --stop-words is --stop-words a

# Shuffle with a seed
uv run python -m src.cli struct shuffle 1 2 3 4 5 --seed 42

# Flatten a list of lists (JSON format)
uv run python -m src.cli struct flatten "[[1, 2], [3, 4], [5]]"
```

## Continuous Integration steps

### Linting (Pylint)

```bash
uv run python -m pylint src/*.py
```

### Formatting (Black)

```bash
uv run black src/*.py
```

### Testing (Pytest)

```bash
uv run python -m pytest -v
```

The tests are divided in two files:

- `tests/test_logic.py`: **unit tests** of all the functions in `preprocessing.py`. They use fixtures to reuse test data and `pytest.mark.parametrize` to run the same test with different inputs (normal cases, edge cases like empty lists, and special values like `None`, `nan` or negative numbers).
- `tests/test_cli.py`: **integration tests** between the CLI and the logic. They use a fixture with Click's `CliRunner` to invoke the commands of the four groups and check their output.

### Test coverage (pytest-cov)

```bash
uv run python -m pytest -v --cov=src
```

## Results

| Step | Result |
|------|--------|
| Pylint | 9.17/10 |
| Black | 3 files left unchanged |
| Pytest | 67 tests passed |
| Coverage | 98% |
