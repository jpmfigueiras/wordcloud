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

from auxiliary_functions import (
    filter_counts,
    font_size,
    list_files,
    merge_counts,
    process_file,
    return_full_directory,
    return_output_path,
    sorted_counts,
    write_error,
    write_report
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
        # Get the input files directory path.
        input_dir = return_full_directory(dir_name="InputFiles")
        # Define output directory and file path relative to the base directory.
        output_dir = return_full_directory(dir_name="OutputFile")
        # Define the output file path within the output directory.
        output_path = return_output_path(file_name="word_cloud.txt", output_dir_name="OutputFile")
        # Collect all .txt files from the input directory.
        files = list_files(input_dir, ext=".txt")
        # Regular expression to match words including accented characters.
        word_regex = re.compile(r"[A-Za-zÀ-ÖØ-öø-ÿ]+")
        # Ensure there are at least 5 input files.
        if(len(files) < 5):
            raise RuntimeError("Need at least 5 input text files.")
        # Process each text file in parallel, using one worker per file.
        # Each task extracts and counts words independently.
        with ThreadPoolExecutor(max_workers=len(files)) as executor:
            futures = [executor.submit(process_file, path, word_regex) for path in files]
            results = [future.result() for future in as_completed(futures)]
        # Merge individual word counts from all files into a total count.
        total = merge_counts(results)
        # Filter out words with frequency less than 2.
        total = filter_counts(total, min_count=2)
        # Determine the maximum word count for size categorization.
        max_count = max(total.values())
        # Sort words by frequency and prepare items for the report.
        ordered = sorted_counts(total)
        # Create a list of tuples with word, frequency, and size label.
        items = [(word, freq, font_size(freq, max_count)) for word, freq in ordered]
        # Ensure the output directory exists, if not, create it.
        os.makedirs(output_dir, exist_ok=True)
        # Write the word cloud report to the output file.
        write_report(items, output_path)
        print(f"Word cloud written to: {output_path}")
    except RuntimeError as exc:
        # Ensure the output directory exists, if not, create it.
        os.makedirs(output_dir, exist_ok=True)
        error_path = return_output_path(file_name="errors.txt", output_dir_name="OutputFile")
        # On error, write the error message to errors.txt in the output directory.
        write_error(error_message=str(exc), error_path=error_path)
        print(f"Error written to: {error_path}")

if __name__ == "__main__":
    main()
