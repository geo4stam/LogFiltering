# Run in terminal like this 
# python3 filter-log.py <filename>

# Summarized description
# Each log entry is spotted by following process - 
# Starts with the date_pattern and ends when a new line AND new date_pattern is found
# then the file is filtered by following process and a new file is created filtered - 
# the dictionary string_patterns contains strings that determine the log entry as unwanted so its removed (skipped) 
# when creating the filtered file. 
# use True or False to determine if the particular string filtering is active or not

# possible mods may include:
# use regex patterns instead of strings for the filtering log entries

import re
import sys

def filter_log(filename):
    with open(filename, 'r') as f:
        log = f.readlines()

# Here we can use "re.match(regex_pattern, line)" to find if a regex pattern is present in a string/line
# or "required_string in line" to find if a string is present inside a string/line

    # Set the pattern to match date entries
        # The second regex seems more complete
    #date_pattern = "^\d{4}-\d{2}-\d{2}"
    # if you are only using script to read osmo logs (never read logs from console output during debugging)
    # you don't need date_pattern_console
    date_pattern_console = r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}.\d+'
    date_pattern_logs = r'\d{2}-\d{2} \d{2}:\d{2}:\d{2}.\d+'

#ADD STRINGS to below dictionary to filter out log entries (see description at top for general info)
    # Set the string to match unwanted lines
    string_patterns = {
        "[LayoutConstraints]": True,
        "[EventSocket] didReceiveMessage - json: Content: {": True,
        "[AppConnect:Debug]": True,
    }

    # Initialize variables
    skip_line = False
    has_date = False

    # Filter the log based on the pattern
    filtered_log = []
    for line in log:
        if re.match(date_pattern_console + '|' + date_pattern_logs, line):
            has_date = True
            skip_line = False
        else:
            has_date = False

        if has_date:
                #if any(unwanted_pattern in line for unwanted_pattern in unwanted_patterns):
            if any(s in line for s, enabled in string_patterns.items() if enabled):
                skip_line = True
            
        if not skip_line:
            filtered_log.append(line)

            #skips lines that start with "+++"
        # if line.startswith("+++"):
        #     skip_line = True

    # Write the filtered log to a new file
    with open(f'{filename}_filtered.log', 'w') as f:
        f.writelines(filtered_log)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Please specify the name of the log file to filter.')
        sys.exit(1)
    filter_log(sys.argv[1])
