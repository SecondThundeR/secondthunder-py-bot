"""Files Handler Library.

This is a basic self-written module to handle operations with files

**Noteworthy:** As the script and needs grow, this module can be expanded and improved

This file can also be imported as a module and contains the following functions:
    * import_data - imports data from file to variable
    * is_exist - returns a bool when checking for presence of local file or folder
    * folder_status - return a bool when checking if folder empty or not
    * create_folder - returns a bool when creating a local folder
    * delete_file - returns a bool when deleting a local file
    * delete_folder - returns a bool when deleting a local folder
"""


import os
import shutil


def import_data(path):
    """Import data from local file and returning as variable.

    Parameters:
        path (str): Path to local file

    Returns:
        str: Read data from local file
    """
    with open(path, 'r', encoding='utf-8') as file:
        file_data = file.read().splitlines()
    file.close()
    return file_data


def is_exist(path):
    """Check for the presence of a file or folder at the specified path.

    Parameters:
        path (str): Path to local file or folder

    Returns:
        bool: True if file or folder exists, False otherwise
    """
    return bool(os.path.exists(path))


def folder_status(path):
    """Check if folder is empty or not.

    Parameters:
        path (str): Path to local folder

    Returns:
        bool: True if not empty, False otherwise
    """
    try:
        return bool(os.listdir(path))
    except OSError as err:
        print('There is an error while checking folder.\n'
              f'Here are error details: {err}')


def create_folder(path):
    """Create folder at the specified path.

    Parameters:
        path (str): Path to local folder
    """
    try:
        if not is_exist(path):
            os.mkdir(path)
    except OSError as err:
        print('There is an error while creating folder.\n'
              f'Here are error details: {err}')


def delete_file(path):
    """Delete file at the specified path.

    If file exists, removes it. Otherwise do nothing

    Parameters:
        path (str): Path to local file
    """
    if is_exist(path):
        os.remove(path)


def delete_folder(path):
    """Delete folder at the specified path.

    Parameters:
        path (str): Path to local folder
    """
    try:
        if is_exist(path):
            shutil.rmtree(path)
    except shutil.Error as err:
        print('There is an error while deleting folder.\n'
              f'Here are error details: {err}')
