#!/usr/bin/python3
# unique-ans.py   
# This solution walks through all directories in root_dir, extracts
# accession numbers using regular expressions, and saves each unique 
# accession item to a separate file in output_dir using the 
# accession number for the filename.
# Thu 06 Apr 2023 08:18:52 AM CDT
#====================================================================

import os
import re

# Set the root directory
root_directory = '/home/juren/Projects/HST-Zyimage-Project/ZyFiles'

# Create a dictionary to store the unique accession items
unique_accessions = {}

# Loop through all the files in the directory tree
for root, dirs, files in os.walk(root_directory):
    for file_name in files:
        # Only process ASCII text files
        if file_name.endswith('.txt'):
            file_path = os.path.join(root, file_name)
            with open(file_path, 'r', encoding='ascii', errors='ignore') as f:
                file_contents = f.read()
                # Use a regular expression to extract the accession number
                accession_match = re.search(r'<accession_number>\s*(\S+)\s*</accession_number>', file_contents)
                if accession_match:
                    accession_number = accession_match.group(1)
                    # If the accession number is not in the dictionary, add the accession item
                    if accession_number not in unique_accessions:
                        unique_accessions[accession_number] = file_contents
                        # Save the accession item as a separate file
                        with open(accession_number + '.txt', 'w', encoding='ascii') as output_file:
                            output_file.write(file_contents)

