# -*- coding: utf-8 -*-
'''
@File    :   auxiliary_functions.py
@Author  :   Joel Figueiras
@Version :   1.0
@Desc    :   Provides auxiliary functions for text processing and word cloud generation.
'''

import os


def font_size(count, max_count):
    '''
    Determines the font size category based on the word count and maximum count.

    Parameters:
        ------------
        count(int): Number of occurrences of the word.
        max_count(int): Maximum number of occurrences across all words.

    Returns:
        ------------
        str: The font size category ("Huge", "Big", "Normal", "Small").
    '''
    # Determine font size based on frequency ratio.
    # If count equals max_count, the word is the most frequent.
    # pylint: disable=superfluous-parens
    try:
        # Check if the word has the maximum count.
        if(count == max_count):
            return "Huge"
        # Calculate the ratio of the word's count to the maximum count.
        ratio = count / max_count
        if(ratio > 0.6):
            return "Big"
        if(ratio > 0.3):
            return "Normal"
        return "Small"
    except Exception as e:
        raise RuntimeError("Error calculating font size.") from e

def list_files(folder, ext=".txt"):
    '''
    Lists file paths in a folder that match the given extension.

    Parameters:
        ------------
        folder(str): Folder path to search.
        ext(str): File extension filter (default ".txt").

    Returns:
        ------------
        list: A list of file paths matching the extension.
    '''
    # Make sure the extension begins with a dot.
    if(not ext.startswith(".")):
        ext = f".{ext}"
    try:
        # List and filter files in the specified folder by extension.
        return [
            os.path.join(folder, name)
            for name in os.listdir(folder)
            if(name.lower().endswith(ext.lower()))
        ]
    except Exception as e:
        raise RuntimeError(f"Error listing files in {folder}: {e}") from e

def read_text(path, encoding="utf-8"):
    '''
    Reads and returns the full text content of a file.

    Parameters:
        ------------
        path(str): Path to the input file.
        encoding(str): File encoding (default "utf-8").

    Returns:
        ------------
        str: The file content as text.
    '''
    try:
        # Read the file content with the specified encoding.
        with open(path, "r", encoding=encoding) as file:
            return file.read()
    except Exception as e:
        raise RuntimeError(f"Error reading text from {path}: {e}") from e

def extract_words(text, pattern):
    '''
    Extracts words from text using the provided regex pattern.

    Parameters:
        ------------
        text(str): Input text to tokenize.
        pattern(re.Pattern): Compiled regular expression for word matching.

    Returns:
        ------------
        list: A list of matched words.
    '''
    try:
        # Use the regex pattern to find all words in the text.
        return pattern.findall(text)
    except Exception as e:
        raise RuntimeError("Error extracting words from text.") from e

def count_words(words):
    '''
    Counts word occurrences in a list.

    Parameters:
        ------------
        words(list): List of words to count.

    Returns:
        ------------
        dict: Dictionary of word counts.
    '''
    try:
        # Count occurrences of each word in the list.
        counts = {}
        for word in words:
            # Increment the word count in the dictionary.
            counts[word] = counts.get(word, 0) + 1
        return counts
    except Exception as e:
        raise RuntimeError("Error counting words.") from e

def merge_counts(list_of_dicts):
    '''
    Merges multiple word-count dictionaries by summing counts.

    Parameters:
        ------------
        list_of_dicts(list): List of dictionaries to merge.

    Returns:
        ------------
        dict: Merged dictionary with summed counts.
    '''
    try:
        # Merge dictionaries by summing counts for each word.
        merged = {}
        for counts in list_of_dicts:
            # Iterate through each word-count pair in the current dictionary.
            for word, count in counts.items():
                # Sum the counts for each word in the merged dictionary.
                merged[word] = merged.get(word, 0) + count
        return merged
    except Exception as e:
        raise RuntimeError("Error merging word counts.") from e

def filter_counts(counts, min_count=2):
    '''
    Filters out words that appear fewer than min_count times.

    Parameters:
        ------------
        counts(dict): Dictionary of word counts.
        min_count(int): Minimum count to keep (default 2).

    Returns:
        ------------
        dict: Filtered dictionary with counts >= min_count.
    '''
    try:
        # Filter the counts dictionary to include only words with counts >= min_count.
        return {word: count for word, count in counts.items() if(count >= min_count)}
    except Exception as e:
        raise RuntimeError("Error filtering word counts.") from e

def sorted_counts(counts):
    '''
    Returns a list of (word, freq) pairs sorted by frequency desc and word asc.

    Parameters:
        ------------
        counts(dict): Dictionary of word counts.

    Returns:
        ------------
        list: Sorted list of (word, freq) tuples.
    '''
    try:
        # Sort the counts dictionary by frequency (descending) and word (ascending).
        return sorted(counts.items(), key=lambda item: (-item[1], item[0]))
    except Exception as e:
        raise RuntimeError("Error sorting word counts.") from e

def write_report(items, output_path):
    '''
    Writes the word cloud report to a file.

    Parameters:
        ------------
        items(list): List of (word, freq, size) tuples in output order.
        output_path(str): Path to the output file.
    '''
    try:
        # Write the report to the specified output file.
        with open(output_path, "w", encoding="utf-8") as file:
            # Write each word, frequency, and size to the file.
            for word, freq, size in items:
                # Write a line with word, frequency, and size separated by tabs.
                file.write(f"{word}\t{freq}\t{size}\n")
    except Exception as e:
        raise RuntimeError(f"Error writing report to {output_path}: {e}") from e

def write_error(error_message, error_path):
    '''
    Writes an error message to a specified error file.

    Parameters:
        ------------
        error_message(str): The error message to write.
        error_path(str): Path to the error file.
    '''
    try:
        # Write the error message to the specified error file.
        with open(error_path, "w", encoding="utf-8") as file:
            file.write(error_message)
    except Exception as e:
        raise RuntimeError(f"Error writing error message to {error_path}: {e}") from e

def process_file(path, pattern):
    '''
    Reads text from a file, extracts words, lowercases them, and counts occurrences.

    Parameters:
        ------------
        path(str): Path to the input file.
        pattern(re.Pattern): Compiled regex pattern for word matching.

    Returns:
        ------------
        dict: Dictionary of word counts from this file.
    '''
    try:
        text = read_text(path)
        words = [word.lower() for word in extract_words(text, pattern)]
        return count_words(words)
    except Exception as e:
        raise RuntimeError(f"Error processing file {path}: {e}") from e

def return_full_directory(dir_name):
    '''
    Returns the full path to a directory given its name.

    Parameters:
        ------------
        dir_name(str): Name of the directory.

    Returns:
        ------------
        str: Path to the directory.
    '''
    try:
        if(dir_name is None or dir_name.strip() == ""):
            raise ValueError("Directory name must be a non empty string.")
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        return os.path.join(base_dir, dir_name)
    except Exception as e:
        raise RuntimeError(f"Error determining directory path: {dir_name} ") from e


def return_output_path(file_name, output_dir_name):
    '''
    Returns the full path to the output file.

    Parameters:
        ------------
        file_name(str): Name of the output file.
        output_dir_name(str): Name of the output directory.

    Returns:
        ------------
        str: Path to the output file.
    '''
    try:
        if(file_name is None or file_name.strip() == ""):
            raise ValueError("File name must be a non empty string.")
        if(output_dir_name is None or output_dir_name.strip() == ""):
            raise ValueError("Output directory name must be a non empty string.")
        output_dir = return_full_directory(output_dir_name)
        return os.path.join(output_dir, file_name)
    except Exception as e:
        raise RuntimeError("Error determining output file path.") from e
