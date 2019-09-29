"""
Title: Search files and folders for username, password combinations.
    Output results to a file in format username:password:file_found
Author: Primus27
Version: 1.1
"""

# Import packages
import os
import argparse
from pathlib import Path
from title_generator import TitleGen

# Current program version
current_version = 1.1


def extract_kw(line):
    """
    Takes string and extracts the keyword.
    E.g. 'Password: 123' returns '123'
    :param line: Line to extract.
    :return: Keyword found after the colon punctuation mark.
    """
    return (line.split(":")[-1]).replace("\n", "").replace(" ", "")


def list_lower(mixed_list):
    """
    Converts list element in a list to lowercase.
    :param mixed_list: The list to be altered.
    :return: The list in all lowercase.
    """
    return [str(element).lower() for element in mixed_list]


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
                        username = "%no_user%"

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
            if output_path_flag:
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
            with open(file_output_name, "a") as f:
                # Write to file if list has >0 values
                if credentials_list:
                    # Add a new line at end of each value in list
                    f.writelines("%s\n" % line for line in credentials_list)
            print("\n[*] File saved under '{f}'".format(f=file_output_name))
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
    # Define argument parser
    parser = argparse.ArgumentParser()
    # Remove existing action groups
    parser._action_groups.pop()

    # Create a required and optional group
    required = parser.add_argument_group("required arguments")
    optional = parser.add_argument_group("optional arguments")

    # Define arguments
    required.add_argument("-s", "--scanpath", action="store", default="scan",
                          dest="scan_path",
                          help="Scan path (absolute or relative)",
                          required=True)
    optional.add_argument("-rm", "--userpass", action="store_false",
                          dest="user_pass_flag",
                          help="Disable username & password search")
    optional.add_argument("-x", "--inclpath", action="store_true",
                          dest="output_path_flag",
                          help="Enable path where credential was found")
    optional.add_argument("-f", "--fileout", action="store_true",
                          dest="file_output_flag", help="Enable file output")
    optional.add_argument("-n", "--filename", action="store",
                          default="credentials.txt", dest="file_output_name",
                          help="Declare a custom filename for file output")
    optional.add_argument("-u", "--username", nargs="*", action="store",
                          default=[], dest="user_syn",
                          help="Add additional username aliases")
    optional.add_argument("-p", "--password", nargs="*", action="store",
                          default=[], dest="pass_syn",
                          help="Add additional password aliases")
    optional.add_argument("-l", "--advanced", nargs="*", action="store",
                          default=[], dest="search_list",
                          help="Add additional search terms")
    optional.add_argument("--version", action="version",
                          version="%(prog)s {v}".format(v=current_version),
                          help="Display program version")
    args = parser.parse_args()

    # Synonyms of username
    user_syn = ["user", "username", "login", "email", "id"]
    user_syn.extend(args.user_syn)
    user_syn = list_lower(user_syn)

    # Synonyms of password
    pass_syn = ["pass", "password", "key", "secret", "pin", "passcode",
                "token"]
    pass_syn.extend(args.pass_syn)
    pass_syn = list_lower(pass_syn)

    # Folder path to scan (Relative (current) or Absolute)
    scan_path = Path(args.scan_path)

    # Search file for username and password
    user_pass_flag = args.user_pass_flag

    # Location is output alongside credentials
    output_path_flag = args.output_path_flag

    # Output results to file
    file_output_flag = args.file_output_flag

    # Declare custom filename for output file
    file_output_name = args.file_output_name

    # Additional search terms
    search_list = []
    search_list.extend(args.search_list)
    search_list = list_lower(search_list)

    # Run main method
    main()
