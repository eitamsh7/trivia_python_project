CMD_FIELD_LENGTH = 16  # Exact length of cmd field (in bytes)
LENGTH_FIELD_LENGTH = 4  # Exact length of length field (in bytes)
MAX_DATA_LENGTH = 10 ** LENGTH_FIELD_LENGTH - 1  # Max size of data field according to protocol
MSG_HEADER_LENGTH = CMD_FIELD_LENGTH + 1 + LENGTH_FIELD_LENGTH + 1  # Exact size of header (CMD+LENGTH fields)
MAX_MSG_LENGTH = MSG_HEADER_LENGTH + MAX_DATA_LENGTH  # Max size of total message
DELIMITER = '|'  # Delimiter character in protocol
DATA_DELIMITER = '#'  # Delimiter in the data part of the message

PROTOCOL_CLIENT = {
    "login_msg": "LOGIN",
    "logout_msg": "LOGOUT"
}

PROTOCOL_SERVER = {
    "login_ok_msg": "LOGIN_OK",
    "login_failed_msg": "ERROR"
}
ERROR_RETURN = None  # What is returned in case of an error


def split_data(msg: str, expected_fields: int):
    """
    Helper method. gets a string and number of expected fields in it. Splits the string
    using protocol's data field delimiter (|#) and validates that there are correct number of fields.
    Returns: list of fields if all ok. If some error occured, returns None
    """
    split_msg = msg.split(DATA_DELIMITER, expected_fields)
    if len(split_msg) == expected_fields + 1:
        return split_msg
    else:
        return [ERROR_RETURN]


def join_data(msg_fields: str):
    """
    Helper method. Gets a list, joins all of it's fields to one string divided by the data delimiter.
    Returns: string that looks like cell1#cell2#cell3
    """
    return DATA_DELIMITER.join(msg_fields)  # return one str with DATA_DELIMITER '#'


def build_message(cmd: str, data: str):
    """
    Gets command name (str) and data field (str) and creates a valid protocol message
    Returns: str, or None if error occured
    """
    if cmd not in PROTOCOL_CLIENT.values():
        return ERROR_RETURN
    if len(data) > MAX_DATA_LENGTH:
        return ERROR_RETURN
    cmd_fields = cmd.ljust(16)
    data_length = str(len(data)).zfill(4)
    msg_format = cmd_fields + DELIMITER + data_length + DELIMITER + data
    return msg_format


def parse_message(data: str):
    """
    Parses protocol message and returns command name and data field
    Returns: cmd (str), data (str). If some error occured, returns None, None
    """
    split_data_format = data.split(DELIMITER, 2)
    if len(split_data_format) != 3:
        return None, None
    data_length = split_data_format[1].replace(' ', '0')
    if not data_length.isnumeric():  # check if the data is only numbers
        return None, None
    cmd = split_data_format[0].strip()  # remove all the spaces int the string
    data = split_data_format[-1]
    return cmd, data
