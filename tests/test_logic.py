
import pytest
import math

from src.preprocessing import (
    remove_missing_values,
    fill_missing_values,
    remove_duplicates,
    normalize,
    standardize,
    clip_values,
    convert_to_integers,
    logarithmic_transform,
    tokenize_text,
    select_alphanumeric,
    remove_stop_words,
    flatten_list,
    shuffle_values,
)


# FIXTURE
@pytest.fixture
def numbers():
    return [1, 2, 3, 4, 5]


# 1. REMOVE MISSING VALUES
@pytest.mark.parametrize(
    "values, expected",
    [
        ([1, None, 2, ""], [1, 2]),
        ([1, float("nan"), 2], [1, 2]),
        (["hello", "nan", "world"], ["hello", "world"]),
        ([None, "", "nano"], []),
    ],
)
def test_remove_missing_values(values, expected):
    assert remove_missing_values(values) == expected


# 2. FILL MISSING VALUES
@pytest.mark.parametrize(
    "values, fill_value, expected",
    [
        ([1, None, 2], 0, [1, 0, 2]),
        ([1, "", 2], 99, [1, 99, 2]),
        ([None, "nan", 3], -1, [-1, -1, 3]),
    ],
)
def test_fill_missing_values(values, fill_value, expected):
    assert fill_missing_values(values, fill_value) == expected


def test_fill_missing_values_default():
    assert fill_missing_values([1, None, 2]) == [1, 0, 2]


# 3. REMOVE DUPLICATES
@pytest.mark.parametrize(
    "values, expected",
    [
        ([1, 2, 2, 3], [1, 2, 3]),
        (["a", "b", "a"], ["a", "b"]),
        ([], []),
    ],
)
def test_remove_duplicates(values, expected):
    assert remove_duplicates(values) == expected


# 4. NORMALIZE
def test_normalize(numbers):
    assert normalize(numbers) == [0, 0.25, 0.5, 0.75, 1]


@pytest.mark.parametrize(
    "values, new_min, new_max, expected",
    [
        ([0, 5, 10], 0, 1, [0, 0.5, 1]),
        ([0, 5, 10], -1, 1, [-1, 0, 1]),
        ([2, 2, 2], 0, 1, [0, 0, 0]),
        ([], 0, 1, []),
    ],
)
def test_normalize_parametrized(values, new_min, new_max, expected):
    assert normalize(values, new_min, new_max) == expected


def test_normalize_invalid_range():
    with pytest.raises(ValueError):
        normalize([1, 2, 3], 10, 0)


# 5. STANDARDIZE
def test_standardize(numbers):
    result = standardize(numbers)
    assert len(result) == 5
    assert sum(result) == pytest.approx(0)


def test_standardize_constant_values():
    assert standardize([5, 5, 5]) == [0, 0, 0]


def test_standardize_empty_list():
    assert standardize([]) == []


# 6. CLIP VALUES
@pytest.mark.parametrize(
    "values, min_value, max_value, expected",
    [
        ([-5, 0, 5, 10, 15], 0, 10, [0, 0, 5, 10, 10]),
        ([1, 2, 3], 0, 5, [1, 2, 3]),
        ([1, 2, 3], 2, 2, [2, 2, 2]),
        ([], 0, 10, []),
    ],
)
def test_clip_values(values, min_value, max_value, expected):
    assert clip_values(values, min_value, max_value) == expected


def test_clip_invalid_range():
    with pytest.raises(ValueError):
        clip_values([1, 2, 3], 10, 0)


# 7. CONVERT TO INTEGERS
@pytest.mark.parametrize(
    "values, expected",
    [
        (["1", "2", "3"], [1, 2, 3]),
        (["10", "hello", "20"], [10, 20]),
        (["1", "2.5", "3"], [1, 3]),
        ([], []),
    ],
)
def test_convert_to_integers(values, expected):
    assert convert_to_integers(values) == expected


def test_convert_to_integers_with_none():
    assert convert_to_integers(["1", None, "2"]) == [1, 2]


# 8. LOGARITHMIC TRANSFORM
@pytest.mark.parametrize(
    "values, expected",
    [
        ([1, math.e, 0], [0, 1]),
        ([1, 10, -5], [0, math.log(10)]),
        ([], []),
        ([-1, -2, 0], []),
    ],
)
def test_logarithmic_transform(values, expected):
    assert logarithmic_transform(values) == pytest.approx(expected)


# 9. TOKENIZE TEXT
@pytest.mark.parametrize(
    "text, expected",
    [
        ("Hello World!", ["hello", "world"]),
        ("Python is GREAT.", ["python", "is", "great"]),
        ("Hello, 123 World!", ["hello", "123", "world"]),
        ("", []),
    ],
)
def test_tokenize_text(text, expected):
    assert tokenize_text(text) == expected


# 10. SELECT ALPHANUMERIC
@pytest.mark.parametrize(
    "text, expected",
    [
        ("Hello, World! 123", "Hello World 123"),
        ("Python@2025!", "Python2025"),
        ("Hello World", "Hello World"),
        ("", ""),
    ],
)
def test_select_alphanumeric(text, expected):
    assert select_alphanumeric(text) == expected


# 11. REMOVE STOP WORDS
@pytest.mark.parametrize(
    "text, stop_words, expected",
    [
        ("This is a test", ["is", "a"], "this test"),
        ("I love Python", ["i", "python"], "love"),
        ("HELLO WORLD", ["hello"], "world"),
        ("This is a test", [], "this is a test"),
        ("", ["the", "a"], ""),
    ],
)
def test_remove_stop_words(text, stop_words, expected):
    assert remove_stop_words(text, stop_words) == expected


# 12. FLATTEN LIST
@pytest.mark.parametrize(
    "nested_list, expected",
    [
        ([[1, 2], [3, 4]], [1, 2, 3, 4]),
        ([["a"], ["b", "c"]], ["a", "b", "c"]),
        ([[], [1, 2], []], [1, 2]),
        ([], []),
    ],
)
def test_flatten_list(nested_list, expected):
    assert flatten_list(nested_list) == expected


# 13. SHUFFLE VALUES
def test_shuffle_values(numbers):
    result = shuffle_values(numbers, 42)
    assert sorted(result) == sorted(numbers)
    assert numbers == [1, 2, 3, 4, 5]


def test_shuffle_reproducibility(numbers):
    result1 = shuffle_values(numbers, 42)
    result2 = shuffle_values(numbers, 42)
    assert result1 == result2

