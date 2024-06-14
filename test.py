def custom_len(list):
    length = 0
    for item in list:
        length += 1
    return length


login_list = ['0', '1', '2', '3', '4', '5', '6']

alternative = [str(index + 1) for index in range(custom_len(login_list))]
print(alternative)
