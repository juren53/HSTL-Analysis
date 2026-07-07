import os
import re

# Directory containing the files to search
directory = '/home/juren/Projects/HST-ZyImage-Project/'

# Search query
search_query = '"Senator Tom Connally meets"'

# Function to search for the query in each file
def search_files(directory, search_query):
    results = []
    for filename in os.listdir(directory):
        if filename.endswith('.txt'):  # Change the file extension if necessary
            with open(os.path.join(directory, filename), 'r') as file:
                file_contents = file.read()
                if re.search(search_query, file_contents):
                    results.append(filename)
    return results

# Search for the query in the files
matching_files = search_files(directory, search_query)

# Print the matching files
if len(matching_files) > 0:
    print('Matching files:')
    for filename in matching_files:
        print(filename)
else:
    print('No matching files found.')

