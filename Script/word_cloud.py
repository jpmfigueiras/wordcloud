# -*- coding: utf-8 -*-
'''
@File    :   word_cloud.py
@Author  :   Joel Figueiras
@Version :   1.0
@Desc    :   Generates a word cloud report from multiple text files.
'''
import os
import re
from concurrent.futures import ThreadPoolExecutor, as_completed

from generic_functions import (
    filter_counts,
    list_files,
    merge_counts,
    process_file,
    size_label,
    sorted_counts,
    write_report,
)

def main():
    '''
    Main function to generate the word cloud report.
    
    Parameters:
        ------------
        param_name: None.
    
    Returns:
        ------------
        return_type: None.
    '''
    try:
        # Setup input and output directories
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        # Define input directory path relative to the base directory.
        input_dir = os.path.join(base_dir, "InputFiles")
        # Define output directory and file path relative to the base directory.
        output_dir = os.path.join(base_dir, "OutputFile")
        # Define the output file path within the output directory.
        output_path = os.path.join(output_dir, "word_cloud.txt")
        # Collect all .txt files from the input directory.
        files = list_files(input_dir, ext=".txt")
        # Regular expression to match words including accented characters.
        WORD_REGEX = re.compile(r"[A-Za-zÀ-ÖØ-öø-ÿ]+")
        # Ensure there are at least 5 input files.
        if(len(files) < 5):
            raise RuntimeError("Need at least 5 input text files.")
        # Process each text file in parallel, using one worker per file.
        # Each task extracts and counts words independently.
        with ThreadPoolExecutor(max_workers=len(files)) as executor:
            futures = [executor.submit(process_file, path, WORD_REGEX) for path in files]
            results = [future.result() for future in as_completed(futures)]
        # Merge individual word counts from all files into a total count.
        total = merge_counts(results)
        # Filter out words with frequency less than 2.
        total = filter_counts(total, min_count=2)
        if(not total):
            raise RuntimeError("No words with frequency greater than 1.")
        # Determine the maximum word count for size categorization.
        max_count = max(total.values())
        # Sort words by frequency and prepare items for the report.
        ordered = sorted_counts(total)
        # Create a list of tuples with word, frequency, and size label.
        items = [(word, freq, size_label(freq, max_count)) for word, freq in ordered]
        # Ensure the output directory exists, if not, create it.
        os.makedirs(output_dir, exist_ok=True)
        # Write the word cloud report to the output file.
        write_report(items, output_path)
        print(f"Word cloud written to: {output_path}")
    except RuntimeError as exc:
        # On error, write the error message to errors.txt in the output directory.
        os.makedirs(output_dir, exist_ok=True)
        error_path = os.path.join(output_dir, "errors.txt")
        with open(error_path, "w", encoding="utf-8") as file:
            file.write(str(exc))
        print(f"Error written to: {error_path}")

if __name__ == "__main__":
    main()
