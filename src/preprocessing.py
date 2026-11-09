
import math
import re
import random
import statistics


# 1. Removal of missing values
def remove_missing_values(values):
    """
    Remove missing values: None, empty strings, 'nan', 'nano' and NaN.
    """
    return [
        value for value in values
        if value is not None
        and not (isinstance(value, str) and value.strip().lower() in ("", "nan", "nano"))
        and not (isinstance(value, float) and math.isnan(value))
    ]


# 2. Filling missing values
def fill_missing_values(values, fill_value=0):
    """
    Replace missing values with the specified fill value.
    """
    result = []

    for value in values:
        if (value is None
            or (isinstance(value, str) and value.strip().lower() in ("", "nan", "nano"))
            or (isinstance(value, float) and math.isnan(value))):
            result.append(fill_value)
        else:
            result.append(value)

    return result


# 3. Removal of duplicated values
def remove_duplicates(values):
    """
    Return a list containing only unique values.
    Preserve the original order.
    """
    return list(dict.fromkeys(values))


# 4. Min-max normalization
def normalize(values, new_min=0.0, new_max=1.0):
    """
    Normalize numerical values using the min-max method.
    """
    if not values:
        return []

    if new_min > new_max:
        raise ValueError("new_min cannot be greater than new_max")

    old_min = min(values)
    old_max = max(values)

    if old_min == old_max:
        return [new_min for _ in values]

    return [
        ((value - old_min) / (old_max - old_min))
        * (new_max - new_min) + new_min
        for value in values
    ]


# 5. Z-score standardization
def standardize(values):
    """
    Standardize numerical values using the z-score method.
    """
    if not values:
        return []

    mean = statistics.mean(values)
    std_dev = statistics.pstdev(values)

    if std_dev == 0:
        return [0.0 for _ in values]

    return [(value - mean) / std_dev for value in values]


# 6. Clipping numerical values
def clip_values(values, min_value, max_value):
    """
    Restrict numerical values to a specified range.
    """
    if min_value > max_value:
        raise ValueError("min_value cannot be greater than max_value")

    return [
        max(min_value, min(value, max_value))
        for value in values
    ]


# 7. Conversion of values to integers
def convert_to_integers(values):
    """
    Convert numerical strings to integers.
    Exclude non-numerical values.
    """
    result = []

    for value in values:
        try:
            result.append(int(value))
        except (ValueError, TypeError):
            continue

    return result


# 8. Logarithmic scale transformation
def logarithmic_transform(values):
    """
    Convert positive numerical values to their natural logarithm.
    Ignore zero and negative values.
    """
    return [
        math.log(value)
        for value in values
        if value > 0
    ]


# 9. Tokenization of text
def tokenize_text(text):
    """
    Split text into lowercase words.
    Keep only alphanumeric characters.
    """
    return re.findall(r"[^\W_]+", text.lower())


# 10. Selection of alphanumeric characters and spaces
def select_alphanumeric(text):
    """
    Keep only alphanumeric characters and spaces.
    """
    return "".join(
        char for char in text
        if char.isalnum() or char == " "
    )


# 11. Removal of stop words
def remove_stop_words(text, stop_words):
    """
    Remove stop words from lowercase text.
    """
    words = text.lower().split()
    stop_words = {word.lower() for word in stop_words}

    filtered_words = [
        word for word in words
        if word not in stop_words
    ]

    return " ".join(filtered_words)


# 12. Flatten a list of lists
def flatten_list(nested_list):
    """
    Convert a list of lists into a single list.
    """
    return [
        item
        for sublist in nested_list
        for item in sublist
    ]


# 13. Random shuffling of a list
def shuffle_values(values, seed):
    """
    Shuffle values randomly using a seed for reproducibility.
    The original list remains unchanged.
    """
    shuffled = values.copy()
    random.Random(seed).shuffle(shuffled)

    return shuffled

