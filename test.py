def custom_enumerate(main_list):
    aux_list = []
    counter = 1
    for _ in main_list:
        aux_list.append(str(counter) + '. ' + main_list[counter - 1])
        counter += 1
    return aux_list

service_list = ["sum", "del", "exterminate", "exit"]
# aux_list = []
# custom_enumerate(aux_list, service_list)
# print(aux_list)
# print(service_list)
aux_list = custom_enumerate(service_list)
print(f"Available services:\n{'\n'.join(service for service in aux_list)}\n")
