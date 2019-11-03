import re


def check_mac_address(mac_address):

    """ Checks if a string matches the pattern of a MAC address.
    
        :param mac_address: a string that represents a MAC address
    """

    mac_pattern = r'^[a-fA-F0-9]{2}[:][a-fA-F0-9]{2}[:][a-fA-F0-9]{2}[:][a-fA-F0-9]{2}[:][a-fA-F0-9]{2}[:][a-fA-F0-9]{2}$'

    if re.match(mac_pattern, str(mac_address)):
        return True
    else:
        return False


def infer_type(item):
    
    """This function attempts to match the input item with predefined patterns to determine its data type.
       Four patterns are tested: double, integer, boolean, datetime and string

       :param item: The item to be matched with the predefined patterns
       :returns: The infered type or None
       :rtype: String or None
    """

    if(item == None):
        return None

    # Spaces at the beginning and end of the string are removed
    trimmed_item = str(item).strip()

    ## Parse double
    #match = re.search(r'^[-+]?(?:(?:\d*\.\d+)|(?:\d+\.?))(?:[Ee][+-]?\d+)?$', trimmed_item)
    # This matching pattern forces the use of a decimal point to differentiate integers from decimals
    match = re.search(r'^[-+]?(?:(?:\d*\.\d+)|(?:\d+\.))(?:[Ee][+-]?\d+)?$', trimmed_item)

    if match:
        return 'double'

    ## Parse integer
    match = re.search(r'^[-+]?[0-9]+$', trimmed_item)

    if match:
        return 'int'

    ## Parse boolean
    match = re.search(r'^(true|false)$', trimmed_item.lower())

    if match:
        return 'boolean'

    ## Parse datetime
    match = re.search(r'^((\d{2}(?:\d{2}))[-/]\d{1,2}[-/]\d{1,2})[T\s](\d{1,2}:\d{1,2}:\d{1,2})([.]\d+)$', trimmed_item.upper())

    if match:
        return 'datetime'

    ## Parse string / paragraph
    match = re.search(r'^([\w\W]\s*)+$', trimmed_item)

    if match:
        return 'string'
    
    return None     ## If None of the previous patterns were matched!

