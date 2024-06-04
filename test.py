def custom_lower(input_string):
    result = ""
    for char in input_string:
        if 'A' <= char <= 'Z':
            lower_char = chr(ord(char) + 32)
            result += lower_char
        else:
            result += char
    return result


options = ['Log in', 'Sign up', 'Explore Services', 'Explore Destinations', 'View recommended', 'Check availability']

for i in range(len(options)):
    options[i] = custom_lower(options[i])

print(options)
