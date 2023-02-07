
def camel_case_to_title(string):

    result = string[0].upper()
    for letter in string[1:]:
        if letter.isupper():
            result += ' '
        result += letter
    return result

