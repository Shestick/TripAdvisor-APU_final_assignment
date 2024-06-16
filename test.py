def custom_copy(list_1):
    list_2 = []
    for element in list_1:
        list_2.append(element)
    return list_2

string = "1\n2\n3\n4"

list_1 = ['yes', 'no']
list_2 = custom_copy(list_1)
list_2.append('Maybe')
print(list_1[-1])
