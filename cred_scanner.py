"""
Title: Search files and folders for username, password combinations.
    Output results to a file in format username:password:file_found
Author: Primus27
Version: 1.0
"""

# Import packages
import os
from title_generator import TitleGen

# USER DEFAULTS
# Synonyms of username
user_syn = ["user", "username", "login", "email", "id"]
# Synonyms of password
pass_syn = ["pass", "password", "key", "secret", "pin", "passcode", "token"]
# Folder path to scan (Relative (current) or Absolute)
scan_path = r"creds"
# Search file for username and password
user_pass_flag = True
# Location is output alongside credentials
cred_location_flag = True
# Output results to file
file_output_flag = False
# Additional search terms
search_list = []


def extract_kw(line):
    """
    Takes string and extracts & returns the keyword.
    E.g. 'Password: 123' returns '123'
    :param line: Line to extract.
    :return: Keyword found after the colon punctuation mark.
    """
    return (line.split(":")[-1]).replace("\n", "").replace(" ", "")


def scan_file(file, credentials_dict):
    """
    Opens file and scans for keywords (username, password, etc).
    :param file: The path of the file to be scanned.
    :param credentials_dict: A dictionary with username, password credentials.
    :return: An updated dictionary inc. the contents from the scanned file.
    """
    try:
        # Open file in 'read' mode
        with open(file, "r") as f:
            # Set default username in case a password is the first entry
            username = "%no_user%"
            for line in f:
                if user_pass_flag:
                    # Line contains any username synonym
                    if any(i in line.lower() for i in user_syn):
                        # Extract the keyword from the line
                        username = extract_kw(line)

                    # Line contains any password synonym
                    if any(i in line.lower() for i in pass_syn):
                        # Extract the keyword from the line
                        password = extract_kw(line)

                        # Username already exists in credentials dictionary
                        if username in credentials_dict.keys():
                            # Add the password to the existing username key
                            credentials_dict[username].append((password, file))
                        else:
                            # Add the username, password combo to dictionary
                            credentials_dict[username] = [(password, file)]

                # User had added search terms
                if search_list:
                    # Cycle through keywords
                    for keyword in search_list:
                        # Keyword found in line. Extract
                        if keyword in line.lower():
                            word = extract_kw(line)

                            # Create or add word to dictionary
                            if keyword in credentials_dict.keys():
                                credentials_dict[keyword].append((word, file))
                            else:
                                credentials_dict[keyword] = [(word, file)]
            return credentials_dict
    # Inadequate permission to access location
    except PermissionError:
        print("[*] Inadequate permissions to access file location")
    # Could not find path (should never occur since they were enumerated)
    except OSError:
        print("[*] Unable to find path: {}".format(file))


def enum_files(folder_path):
    """
    Enumerates files in a path.
    :param folder_path: Root folder path for enumeration.
    :return: List containing all files in a folder.
    """
    # List of all files in path
    f_list = []
    # Enumerate files
    for root, dirs, files in os.walk(folder_path, topdown=True):
        for file in files:
            # Generate the absolute/relative path for each file
            file_path = os.path.join(root, file)
            # File exists (it should) and has a size greater than 0KB
            if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
                f_list.append(file_path)
    return f_list


def format_credentials(credentials_dict):
    """
    Create a list of credentials from the dictionary
    :param credentials_dict: Final dictionary containing username, passwords...
    :return Credentials formatted (list)
    """
    # List containing all credentials
    formatted_creds = []

    # Cycle through dictionary
    for key, value in credentials_dict.items():
        # Value (list) contains multiple passwords. Each password (tuple)
        # contains an actual password and the path it was found
        for password in value:
            # Format the credential
            if cred_location_flag:
                cred_combination = "{u}:{p}:({f})".format(u=key, p=password[0],
                                                          f=password[1])
            else:
                cred_combination = "{u}:{p}".format(u=key, p=password[0])

            # Add the formatted credential to the dictionary
            formatted_creds.append(cred_combination)
    return formatted_creds


def file_output(credentials_list):
    """
    Outputs list results to a file
    :param credentials_list: List containing username, passwords...
    """
    if file_output_flag:
        try:
            # Open creds file and append
            with open("creds.txt", "a") as f:
                # Write to file if list has >0 values
                if credentials_list:
                    # Add a new line at end of each value in list
                    f.writelines("%s\n" % line for line in credentials_list)
        # Inadequate permission to access location / save to location
        except PermissionError:
            print("[*] Error saving log - Permission denied")
        # Could not find path
        except OSError:
            print("[*] Error saving log - Path issues")


def main():
    """
    Main method. Runs credential scanner
    """
    # Output title card
    title = TitleGen(text="Credential Scanner", author="Primus27").title
    print(title)

    # Enumerate files in path
    file_list = enum_files(scan_path)

    # Scan each file and add update the credentials dictionary
    credentials = {}
    for filename in file_list:
        credentials = scan_file(filename, credentials)

    # Convert the dictionary into a list ready for output
    creds_list = format_credentials(credentials)

    # Print results title
    print("{n} results found in '{p}':\n".format(n=len(creds_list),
                                                 p=scan_path))

    # Output results to terminal
    for item in creds_list:
        print(item)

    # Output results to file
    if file_output_flag:
        file_output(creds_list)


if __name__ == '__main__':
    main()
