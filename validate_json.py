import json
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def validate_json_data(json_file_path):
    """Validates the Linux command JSON data.

    Args:
        json_file_path (str): The path to the JSON file.

    Returns:
        bool: True if the JSON data is valid, False otherwise.
    """

    try:
        with open(json_file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        logging.error(f"JSON file not found: {json_file_path}")
        return False
    except json.JSONDecodeError:
        logging.error(f"Invalid JSON format in: {json_file_path}")
        return False

    valid = True

    for i, command_entry in enumerate(data):
        command = command_entry.get("command")
        summary = command_entry.get("summary")
        description = command_entry.get("description")
        options = command_entry.get("options")
        exit_status = command_entry.get("exit_status")
        examples = command_entry.get("examples")

        if not command:
            logging.error(f"Entry {i+1}: 'command' is missing.")
            valid = False
        if not summary:
            logging.error(f"Entry {i+1}: 'summary' is missing.")
            valid = False
        if not description:
            logging.error(f"Entry {i+1}: 'description' is missing.")
            valid = False

        if options is not None:  # Options can be an empty list
            if not isinstance(options, list):
                logging.error(f"Entry {i+1}: 'options' must be a list.")
                valid = False
            else:
                for j, option in enumerate(options):
                    short = option.get("short")
                    long = option.get("long")
                    desc = option.get("description")
                    if not desc:
                        logging.error(f"Entry {i+1}, Option {j+1}: 'description' is missing.")
                        valid = False
                    if short and not isinstance(short, str):
                        logging.error(f"Entry {i+1}, Option {j+1}: 'short' must be a string.")
                        valid = False
                    if long and not isinstance(long, str):
                        logging.error(f"Entry {i+1}, Option {j+1}: 'long' must be a string.")
                        valid = False
                    if short is None and long is None:
                        logging.error(f"Entry {i+1}, Option {j+1}: At least 'short' or 'long' must be present")
                        valid = False

        if exit_status is not None:
            if not isinstance(exit_status, dict):
                logging.error(f"Entry {i+1}: 'exit_status' must be a dictionary.")
                valid = False
            else:
                for code, desc in exit_status.items():
                    if not isinstance(code, str) and not isinstance(code, int): # Exit codes can be numbers or strings.
                        logging.error(f"Entry {i+1}: Exit status code '{code}' must be a string or an integer.")
                        valid = False
                    if not isinstance(desc, str):
                        logging.error(f"Entry {i+1}: Exit status description for '{code}' must be a string.")
                        valid = False

        if examples is not None:
            if not isinstance(examples, list):
                logging.error(f"Entry {i+1}: 'examples' must be a list.")
                valid = False
            else:
                for k, example in enumerate(examples):
                    if not isinstance(example, dict):
                        logging.error(f"Entry {i+1}, Example {k+1}: Example must be a dictionary.")
                        valid = False
                    else:
                        ex_command = example.get("command")
                        ex_description = example.get("description")
                        if not ex_command:
                            logging.error(f"Entry {i+1}, Example {k+1}: 'command' is missing.")
                            valid = False
                        if not ex_description:
                            logging.error(f"Entry {i+1}, Example {k+1}: 'description' is missing.")
                            valid = False
                        if not isinstance(ex_command, str):
                            logging.error(f"Entry {i+1}, Example {k+1}: Example command must be a a string")
                            valid = False
                        if not isinstance(ex_description, str):
                            logging.error(f"Entry {i+1}, Example {k+1}: Example description must be a string")
                            valid = False

    return valid


if __name__ == "__main__":
    json_file = "commands.json"  # Replace with your JSON file path
    if validate_json_data(json_file):
        logging.info("JSON data is valid.")
    else:
        logging.error("JSON data is invalid. Please correct the errors before proceeding.")