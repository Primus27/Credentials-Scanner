![](readme_files/banner.png)

# Credentials Scanner

## Features
 - Scan files and folders for username & password combinations
 - Add aliases for username or password i.e. "login"
 - Search for additional terms i.e. website.com
    - Remove username & password search to limit search to terms (optional)
 - Output results to a file (optional)
    - Enable or Disable where the combination was found (optional)

## Requirements and Installation
 - [Python 3.x](https://www.python.org/)
 - Install all dependencies from the requirements.txt file. `pip install -r requirements.txt`

## Usage
 - Open `cred_scanner.py` and change lines 11-25 depending on params
 - Run `cred_scanner.py`
 - Results are output to `creds.txt` in format:
    - _username_:_password_:(_file_location_)
    - _keyword_:_value_:(_file_location_)
    
    or
    
    - _username_:_password_
    - _keyword_:_value_

## Changelog
#### Version 1.0 - Initial release
 - File and folder scanner for credentials
    - Can be relative path or absolute path
    - Does not have to contain 'username' or 'password' via aliases
    - Search for words following specific keywords
 - Output results to file
    - _username_:_password_:(_file_location_)