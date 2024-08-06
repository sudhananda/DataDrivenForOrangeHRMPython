import csv
import json
from pathlib import Path
from framework.exceptions import TestCaseNotFoundInDataFileException


def get_environment_data(environment_name):
    with open(str(Path(__file__).parent.parent.absolute()) +
              '/data/appData.json', 'r') as f:
        data = json.load(f)

    if environment_name in data['environments']:
        return data['environments'][environment_name]
    else:
        return None


def get_test_case_data(file_path, tc_id):
    """
    Searches for a given test case ID in a CSV file and returns the test case data along with headers.

    :param file_path: Path to the CSV file
    :param tc_id: The test case ID to search for
    :return: A dictionary with headers as keys and test case data as values
    :raises TestCaseNotFoundInDataFileException: If the test case ID is not found in the CSV file
    """
    try:
        with open(file_path, mode='r', newline='') as file:
            reader = csv.DictReader(file)
            headers = reader.fieldnames  # Get headers from the CSV file
            for row in reader:
                if row['tc_id'] == tc_id:
                    # Construct the dictionary with headers as keys and test case row as values
                    return {header: row[header] for header in headers}
            # If the loop completes without finding the test case, raise an exception
            raise TestCaseNotFoundInDataFileException(f"Test case with ID '{tc_id}' not found in the data file.")
    except FileNotFoundError:
        raise FileNotFoundError(f"The file at path '{file_path}' was not found.")
    except Exception as e:
        raise Exception(f"An error occurred: {e}")
