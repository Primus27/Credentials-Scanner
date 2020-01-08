![](readme_files/Banner.png)

# Credentials Scanner

## Features
 - Scan files and folders for username & password combinations
 - Add aliases for username or password i.e. "login"
 - Search for additional terms i.e. website.com
    - Remove username & password search to limit search to terms (optional)
 - Output results to a file (optional)
    - Enable or Disable where the combination was found (optional)
    - Custom filename (optional)

![](readme_files/demo.gif)
> Application demo (fake credentials used)

## Requirements and Installation
 - [Python 3.x](https://www.python.org/)
 - Windows (tested), Linux (tested), Mac (untested)
 - Install all dependencies from the requirements.txt file. `pip3 install -r requirements.txt`

## Arguments
#### Required arguments:
  - `-s SCAN_PATH` || `--scanpath SCAN_PATH`
    - Scan path (absolute or relative)

#### Optional arguments:
  - `-rm` || `--userpass`
    - Disable username & password search (limit to search terms)
    - Default: Enabled (username & password search)
  
  
  - `-x` || `--inclpath`
    - Show credential path in terminal / file output
    - Default: Disabled
    - This will show in the format: **\_:\_:(path)**
  
  
  - `-f` || `--fileout`
    - Enable file output
    - Each credential is written to a new line
    - It is recommended to output to a txt file
    - Default: Disabled
    
    
  - `-n FILENAME.txt` || `--filename FILENAME.txt`
    - Custom filename for output
    - It is recommended to output to a txt file
    - Default: credentials.txt
  
  
  - `-u USER_SYN1 USER_SYN2 ...` || `--username USER_SYN1 USER_SYN2 ...`
    - Add additional username aliases
    - Default:
        - user
        - username
        - login
        - email
        - id
        
        
  - `-p PASS_SYN1 PASS_SYN2 ...` || `--password PASS_SYN1 PASS_SYN2 ...`
    - Add additional password aliases
    - Default:
        - pass
        - password
        - key
        - secret
        - pin
        - passcode
        - token
  
  
  - `-l TERM1 TERM2 ...` || `--advanced TERM1 TERM2 ...`
    - Add additional search terms
    - Default: (None)
  
  
  - `--version`
    - Display program version

## Usage
 - Run 'scanner.py' in terminal (i.e. command prompt/terminal) with arguments (see above)
 - Results are output to a file in format:
    - _username_:_password_:(_file_location_)
    - _keyword_:_value_:(_file_location_)
    
    or
    
    - _username_:_password_
    - _keyword_:_value_

### Starter commands
 - Run detailed scan
    - `python3 scanner.py -s SCAN_PATH -x`
 - Run detailed scan with file output
    - `python3 scanner.py -s SCAN_PATH -x -f -n FILENAME.txt`

## Changelog
#### Version 1.0 - Initial release
 - File and folder scanner for credentials
    - Can be relative path or absolute path
    - Does not have to contain 'username' or 'password' via aliases
    - Search for words following specific keywords
 - Output results to file
    - _username_::_password_::(_file_location_)
    
#### Version 1.1 - CLI 
 - Added CLI menu
 - Custom filename for output
 
#### Version 1.2 - Small Update
 - Changed formatting for results to _user_::_pass_::_file_
 
#### Version 1.3 - Unix compatibility
  - Updated requirements.txt for Unix support
  - Error testing in Unix

## Planned features:
 - Word list (file) input for username, password and search terms