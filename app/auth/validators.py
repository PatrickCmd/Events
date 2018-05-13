# method to check for special characters and validate a name
def is_valid(name_string):
    special_character = "~!@#$%^&*()_={}|\[]<>?/,;:."
    return any(char in special_character for char in name_string)


# check if field contains number
def has_numbers(inputString):
    return any(char.isdigit() for char in inputString)


# check if names contain numbers
def name_has_numbers(data):
    keys = ('first_name', 'last_name')
    for key in keys:
        if has_numbers(data[key]):
            return True


# string string to remove white spaces
def strip_clean(string):
    return string.strip()
