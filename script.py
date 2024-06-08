import json


def custom_lower(input_string):
    result = ""
    for char in input_string:
        if 'A' <= char <= 'Z':
            lower_char = chr(ord(char) + 32)
            result += lower_char
        else:
            result += char
    return result


def custom_lower_list(uncertain_list):
    lower_list = []
    for element in uncertain_list:
        lower_list.append(custom_lower(element))
    return lower_list


def custom_enumerate(main_list):
    aux_list = []
    counter = 1
    for _ in main_list:
        aux_list.append(str(counter) + '. ' + main_list[counter - 1])
        counter += 1
    return aux_list


def find_index(custom_list, element):
    counter = 0
    for content in custom_list:
        if content == element:
            return counter
        counter += 1


def open_userdata():
    with open('UserData.json', 'r') as file:
        userData = json.load(file)
        return userData


def save_userdata(userData):
    with open('UserData.json', 'w') as file:
        json.dump(userData, file, indent=3)


def open_service_data():
    with open('ServiceData.json', 'r') as file:
        serviceData = json.load(file)
        return serviceData


def save_service_data(serviceData):
    with open('ServiceData.json', 'w') as file:
        json.dump(serviceData, file, indent=3)


def open_destination_data():
    with open('DestinationData.json', 'r') as file:
        destinationData = json.load(file)
        return destinationData


def save_destination_data(destinationData):
    with open('DestinationData.json', 'w') as file:
        json.dump(destinationData, file, indent=3)


def open_recommendation():
    with open('Recommendation.json', 'r') as file:
        recommendation = json.load(file)
        return recommendation


def save_recommendation(recommendation):
    with open('Recommendation.json', 'w') as file:
        json.dump(recommendation, file, indent=3)


def open_promotions():
    with open('Promotions.json', 'r') as file:
        promotions = json.load(file)
        return promotions


def save_promotions(promotions):
    with open('Promotions.json', 'w') as file:
        json.dump(promotions, file, indent=3)


def assign_guest():
    currentUser = {
        "userType": "Guest",
        "login": "default",
        "password": "default",
        "active": True
    }
    return currentUser


def show_options(currentUser):
    options = []
    if currentUser['userType'] == 'Admin':
        options = ['Log in', 'Log out', 'Sign up', 'Block User', 'Unblock User', 'Delete Account',
                   'Update promotions', 'Provide trip recommendation']
    elif currentUser['userType'] == 'Service':
        options = ['Log in', 'Log out', 'Sign up', 'Manage Services', 'Manage Booking', 'Delete Account']
    elif currentUser['userType'] == 'Traveller':
        options = ['Log in', 'Log out', 'Sign up', 'View promotions', 'Explore Services', 'View recommended',
                   'Explore Destinations', 'Manage Booking', 'Delete Account']
    elif currentUser['userType'] == 'Guest':
        options = ['Log in', 'Sign up', 'View promotions', 'Explore Services', 'View recommended',
                   'Explore Destinations']
    options.append("Exit")
    # options = custom_lower(options)
    return options


def function_call(index, currentUser):
    if index == 0:
        currentUser = log_in_account(currentUser)
        return 0, currentUser
    elif index == 1:
        create_account(currentUser)
        confirmation = custom_lower(input("Would you like to stay signed in this account? Yes/No\n"))
        if confirmation == "yes" or confirmation == "1":
            userData = open_userdata()
            currentUser = userData[-1]
        return 0, currentUser
    elif index == 2:
        pass
    elif index == 3:
        block_account(currentUser)
        return 0, currentUser
    elif index == 4:
        unblock_account(currentUser)
        return 0, currentUser
    elif index == 5:
        delete_account(currentUser)
        login_list = get_login_list()
        if currentUser['login'] not in login_list:
            currentUser = assign_guest()
        return 0, currentUser
    elif index == 6:
        confirmation = custom_lower(input("Are you sure you want to log out? Yes/No\n"))
        if confirmation == "yes" or confirmation == "1":
            currentUser = assign_guest()
        return 0, currentUser
    elif index == 7:
        return 1, currentUser
    elif index == 8:
        manage_services(currentUser)
        return 0, currentUser
    elif index == 9:
        currentUser = explore_services(currentUser)
        return 0, currentUser
    elif index == 10:
        explore_destinations()
        return 0, currentUser
    elif index == 11:
        manage_recommendation(currentUser)
        return 0, currentUser
    elif index == 12:
        view_recommendation()
        return 0, currentUser
    elif index == 13:
        manage_promotions(currentUser)
        return 0, currentUser
    elif index == 14:
        view_promotions()
        return 0, currentUser
    elif index == 15:
        currentUser = manage_booking(currentUser)
        return 0, currentUser
    else:
        print("There are no such option available")
        return 0, currentUser


def interact_with_options(currentUser):
    full_options = ['log in', 'sign up', 'search', 'block user', 'unblock user', 'delete account', 'log out', 'exit',
                    'manage services', 'explore services', 'explore destinations', 'provide trip recommendation',
                    'view recommended', 'update promotions', 'view promotions', 'manage booking']
    while True:
        check = 0
        print(f"\n\nYou are currently logged as {currentUser['userType']}\n"
              f"With your current access rights, you have access to: ")
        options_to_show = show_options(currentUser)
        options_to_process = custom_lower_list(options_to_show)
        # options_to_process = []
        # for i in range(len(options_to_show)):
        #     options_to_process.append(custom_lower(options_to_show[i]))
        alternative = [str(index + 1) for index in range(len(options_to_show))]
        options_to_show_aux = custom_enumerate(options_to_show)
        print('\n'.join(option for option in options_to_show_aux))
        # print(options_to_process)
        choice = custom_lower(input("What would you like to do?\n"))
        if choice in options_to_process:
            index = find_index(full_options, choice)
            check, currentUser = function_call(index, currentUser)
        elif choice in alternative:
            index = find_index(full_options, options_to_process[int(choice) - 1])
            # print(index)
            check, currentUser = function_call(index, currentUser)
        else:
            print("There are no such option")
        if check == 1:
            break


def create_account(currentUser):
    userData = open_userdata()
    newUser = {'userType': 'default'}

    while newUser['userType'] == 'default':
        userType = custom_lower(input("Please, enter which account you want to create: Admin, Service or Traveller\n"
                                      "Be aware that only Admins are allowed to create additional Admin accounts\n"))
        if (userType == 'admin' or userType == '1') and currentUser['userType'] == 'Admin':
            newUser['userType'] = 'Admin'
        elif (userType == 'admin' or userType == '1') and currentUser['userType'] != 'Admin':
            print("You have insufficient access rights")
        elif userType == 'service' or userType == '2':
            newUser['userType'] = 'Service'
        elif userType == 'traveller' or userType == '3':
            newUser['userType'] = 'Traveller'
        else:
            print("There is no such account type, enter valid option")
    while True:
        login = input("Please, set your login: ")
        login_list = get_login_list()
        if login in login_list:
            print(f"User {login} already exist, choose another login")
        else:
            newUser['login'] = login
            break
    while True:
        password_set = input("Please, set your password: ")
        password_confirmation = input("Please, confirm your password: ")
        if password_set == password_confirmation:
            newUser['password'] = password_confirmation
            break
        else:
            print("Passwords do not match")
    newUser['active'] = True
    if newUser['userType'] == 'Traveller':
        newUser['booking'] = []
    userData.append(newUser)
    save_userdata(userData)


def get_login_list():
    userData = open_userdata()
    login_list = [user['login'] for user in userData]
    return login_list


def get_active_login_list():
    userData = open_userdata()
    active_login_list = []
    for user in userData:
        if user['active']:
            active_login_list.append(user['login'])
    return active_login_list


def get_blocked_login_list():
    userData = open_userdata()
    blocked_login_list = []
    for user in userData:
        if not user['active']:
            blocked_login_list.append(user['login'])
    return blocked_login_list


def get_user_service_list(currentUser):
    service_list = []
    serviceData = open_service_data()
    for service in serviceData:
        if service['userHost'] == currentUser['login']:
            service_list.append(service['serviceName'])
    return service_list


def get_service_list():
    service_list = []
    serviceData = open_service_data()
    for service in serviceData:
        service_list.append(service['serviceName'])
    return service_list


def get_active_service_list():
    userData = open_userdata()
    active_service_list = []
    serviceData = open_service_data()
    for service in serviceData:
        Host = service['userHost']
        for user in userData:
            if user['login'] == Host and user['active']:
                active_service_list.append(service['serviceName'])
    return active_service_list


def get_destination_list():
    destination_list = []
    destinationData = open_destination_data()
    for destination in destinationData:
        destination_list.append(destination['destinationName'])
    return destination_list


def cancel_users_booking(user):
    serviceData = open_service_data()
    userData = open_userdata()
    user['booking'] = []
    for service in serviceData:
        if user['login'] in service['booking']:
            index = find_index(service['booking'], user['login'])
            del service['booking'][index]
    save_service_data(serviceData)
    save_userdata(userData)


def log_in_account(currentUser):
    userData = open_userdata()
    login_list = get_login_list()
    while True:
        login_attempt = input("Enter your login:\n")
        if login_attempt == "0":
            return currentUser
        if login_attempt in login_list:
            while True:
                password_attempt = input("Enter your password:\n")
                if password_attempt == "0":
                    return currentUser
                for user in userData:
                    if user['login'] == login_attempt and user['password'] == password_attempt:
                        if user['active']:
                            print(f"Login successful. Welcome, {user['login']}!")
                            return user
                        else:
                            print("Your account is inactive, please contact an Admin")
                            return currentUser
                print("Your password is wrong, try again or type 0 to cancel")
        else:
            print("There are no such user, try again or type 0 to cancel")


# def log_out():
#     currentUser = assign_guest()
#     return currentUser

def block_account(currentUser):
    while True:
        if currentUser['userType'] != 'Admin':
            print("How did you get this option???")
        active_users = get_active_login_list()
        blocked_users = get_blocked_login_list()
        print(f"Currently active users:\n{'\n'.join(user for user in active_users)}")
        user_to_block = input("Which user do you want to block?\nType 0 to cancel\n")
        if user_to_block == "0":
            break
        elif user_to_block in active_users and user_to_block != currentUser['login']:
            confirmation = input(f"Are you sure you want to block user {user_to_block}? Yes/No\n")
            if custom_lower(confirmation) == 'yes' or confirmation == '1':
                login_list = get_login_list()
                index = find_index(login_list, user_to_block)
                userData = open_userdata()
                userData[index]['active'] = False
                cancel_users_booking(userData[index])
                save_userdata(userData)
                print(f"User {user_to_block} successfully blocked")
        elif user_to_block in active_users and user_to_block == currentUser['login']:
            print("You can not block yourself")
        elif user_to_block in blocked_users:
            print(f"User {user_to_block} is already blocked")
        else:
            print(f"User {user_to_block} not found")
        tmp = input("Do you wish to continue blocking? Yes/No\n")
        if custom_lower(tmp) == 'no' or tmp == '2':
            break


def unblock_account(currentUser):
    while True:
        if currentUser['userType'] != 'Admin':
            print("How did you get this option???")
        active_users = get_active_login_list()
        blocked_users = get_blocked_login_list()
        if blocked_users == []:
            print("There are no currently blocked users")
            break
        print(f"Currently blocked users:\n{'\n'.join(user for user in blocked_users)}")
        user_to_unblock = input("Which user do you want to unblock?\nType 0 to cancel\n")
        if user_to_unblock == "0":
            break
        elif user_to_unblock in blocked_users:
            confirmation = input(f"Are you sure you want to block user {user_to_unblock}? Yes/No\n")
            if custom_lower(confirmation) == 'yes' or confirmation == '1':
                login_list = get_login_list()
                index = find_index(login_list, user_to_unblock)
                userData = open_userdata()
                userData[index]['active'] = True
                save_userdata(userData)
                print(f"User {user_to_unblock} successfully unblocked")
        elif user_to_unblock in active_users:
            print(f"User {user_to_unblock} is not blocked")
        else:
            print(f"User {user_to_unblock} not found")
        tmp = input("Do you wish to continue unblocking? Yes/No\n")
        if custom_lower(tmp) == 'no' or tmp == '2':
            break


def delete_account(currentUser):
    userData = open_userdata()
    login_list = get_login_list()
    if currentUser['userType'] == 'Admin':
        user_to_delete = input("Write, which user you want to delete\n")
        if user_to_delete in login_list:
            confirmation = custom_lower(input(f"Are you sure you want to delete user {user_to_delete}? Yes/No\n"))
            if custom_lower(confirmation) == 'yes' or custom_lower(confirmation) == '1':
                index = find_index(login_list, user_to_delete)
                cancel_users_booking(userData[index])
                del userData[index]
                save_userdata(userData)
                print(f'User {user_to_delete} successfully deleted')
            else:
                print("Deletion cancelled")
        else:
            print(f"User {user_to_delete} not found")
    else:
        user_to_delete = currentUser["login"]
        confirmation = custom_lower(input(f"Are you sure you want to delete user {user_to_delete}? Yes/No\n"))
        if custom_lower(confirmation) == 'yes' or custom_lower(confirmation) == '1':
            index = find_index(login_list, user_to_delete)
            del userData[index]
            save_userdata(userData)
            print(f'User {user_to_delete} successfully deleted')


def manage_services(currentUser):
    while True:
        if currentUser['userType'] != "Service":
            print("How did you get this option???")
        service_list = get_user_service_list(currentUser)
        if service_list == []:
            to_process = input("What would you like to do?\nAdd Service\nExit\n")
        else:
            print(f"You are currently providing:\n{'\n'.join(service for service in service_list)}\n")
            to_process = input(
                "What would you like to do?\n1. Add Service\n2. Update Services\n3. Delete Service\n4. Exit\n")
        if custom_lower(to_process) == "exit" or to_process == '4':
            break
        elif custom_lower(to_process) == "add service" or to_process == '1':
            add_service(currentUser)
        elif custom_lower(to_process) == "update service" or to_process == '2':
            update_service(currentUser)
        elif custom_lower(to_process) == "delete service" or to_process == '3':
            delete_service(currentUser)


def add_service(currentUser):
    new_service = {}
    while True:
        service_list = get_service_list()
        service_name = input("Enter the service's name\n")
        if service_name in service_list:
            print(f"Service {service_name} already exist, choose another name")
        else:
            new_service['serviceName'] = service_name
            break
    new_service['userHost'] = currentUser['login']
    confirmation = input("Do you want to associate your service with a location? Yes/No\n")
    if custom_lower(confirmation) == 'yes' or confirmation == '1':
        destination_list = get_destination_list()
        lower_destination_list = custom_lower_list(destination_list)
        # print(f"LIST = {lower_destination_list}")
        while True:
            location_to_associate = input(
                f"Currently available destinations:\n{'\n'.join(destination for destination in destination_list)}\nExit\n")
            if custom_lower(location_to_associate) == 'exit':
                new_service["placing"] = 'Not mentioned'
                break
            elif custom_lower(location_to_associate) in lower_destination_list:
                inside_index = find_index(lower_destination_list, custom_lower(location_to_associate))
                new_service["placing"] = destination_list[inside_index]
                break
            else:
                print("There are no such location")
    else:
        new_service["placing"] = 'Not mentioned'
    new_service['quantity'] = input("Enter the provided quantity of your service\n")
    new_service['price'] = input("Enter the price of your service\n")
    start_date = input("Enter your service start date as 'Day Month' or 'Continuous' if your service is not expiring\n")
    if custom_lower(start_date) != 'continuous':
        end_date = input("Enter your service end date as 'Day Month'\n")
        schedule = f"From {start_date} to {end_date}"
    else:
        schedule = 'Continuous'
    new_service['schedule'] = schedule
    new_service['booking'] = []
    print(f"Service name: {new_service['serviceName']}\n"
          f"Hosted by: {new_service['userHost']}\n"
          f"Location: {new_service['placing']}\n"
          f"Provided quantity: {new_service['quantity']}\n"
          f"Price: {new_service['price']}\n"
          f"Schedule: {new_service['schedule']}\n")
    confirmation = input("Do you wish to save current service? Yes/No\n")
    if custom_lower(confirmation) == 'yes' or confirmation == '1':
        serviceData = open_service_data()
        serviceData.append(new_service)
        save_service_data(serviceData)
        destinationData = open_destination_data()
        destination_list = get_destination_list()
        if new_service['placing'] != 'Not mentioned':
            index = find_index(destination_list, new_service['placing'])
            destinationData[index]['amenities'][0].append(new_service['serviceName'])
            destinationData[index]['amenities'][1].append(new_service['schedule'])
            save_destination_data(destinationData)
        print(f"Service {new_service['serviceName']} successfully added")
    else:
        print("Service creation cancelled")


# def update_service_aux()


def update_service(currentUser):
    while True:
        service_list = get_user_service_list(currentUser)
        glob_service_list = get_service_list()
        # I didn't want to redo the whole function from scratch, so I had to do this spaghetti
        if service_list[-1] != 'Exit':
            service_list.append('Exit')
        service_list_aux = custom_enumerate(service_list)
        print(f"You are currently providing:\n{'\n'.join(service for service in service_list_aux)}\n")
        to_process = input("Which of your services you would like to update?\n")
        alternative = [str(index + 1) for index in range(len(service_list))]
        if custom_lower(to_process) == 'exit' or int(to_process) == len(service_list):
            print("Service update cancelled")
            break
        elif custom_lower(to_process) in custom_lower_list(service_list):
            index = find_index(custom_lower_list(service_list), custom_lower(to_process))
            glob_index = find_index(custom_lower_list(glob_service_list), custom_lower(to_process))
        elif to_process in alternative:
            index = int(to_process) - 1
            glob_index = find_index(custom_lower_list(glob_service_list), custom_lower(service_list[index]))
        else:
            print("There is no such service")
            glob_index = -1
        while glob_index != -1:
            destinationData = open_destination_data()
            destination_list = get_destination_list()
            serviceData = open_service_data()
            if serviceData[glob_index]['placing'] != 'Not mentioned':
                destination_index_1 = find_index(destination_list, serviceData[glob_index]['placing'])
                existence_index = find_index(destinationData[destination_index_1]['amenities'][0], serviceData[glob_index]['serviceName'])
            else:
                destination_index_1 = -1
            print(f"1. Service name: {serviceData[glob_index]['serviceName']}\n"
                  f"2. Hosted by: {serviceData[glob_index]['userHost']}\n"
                  f"3. Location: {serviceData[glob_index]['placing']}\n"
                  f"4. Provided quantity: {serviceData[glob_index]['quantity']}\n"
                  f"5. Price: {serviceData[glob_index]['price']}\n"
                  f"6. Schedule: {serviceData[glob_index]['schedule']}\n"
                  f"7. Exit")
            to_update = input("Which part you would like to update?\n")
            if custom_lower(to_update) == 'service name' or custom_lower(to_update) == 'name' or to_update == '1':
                while True:
                    service_list = get_service_list()
                    new_name = input(f"Current Service name: {serviceData[glob_index]['serviceName']}\n"
                                     f"New Service name: ")
                    if new_name in service_list:
                        print(f"Service {new_name} already exist, choose another name")
                    else:
                        serviceData[glob_index]['serviceName'] = new_name
                        break
                # serviceData[glob_index]['serviceName'] = new_name
                save_service_data(serviceData)
                if destination_index_1 != -1:
                    destinationData[destination_index_1]['amenities'][0][existence_index] = new_name
                save_destination_data(destinationData)
                print("Service update successful")
            elif custom_lower(to_update) == 'hosted by' or to_update == '2':
                print("You can not update this")
            elif custom_lower(to_update) == 'location' or to_update == '3':
                destination_list = get_destination_list()
                destination_list.append('Not mentioned')
                new_location = input(f"Current Location: {serviceData[glob_index]['placing']}\n"
                                     f"Available locations:\n{'\n'.join(destination for destination in destination_list)}\n"
                                     f"New Location: ")
                if custom_lower(new_location) == 'not mentioned':
                    new_location = 'Not mentioned'
                if custom_lower(new_location) in custom_lower_list(destination_list):
                    serviceData[glob_index]['placing'] = new_location
                    save_service_data(serviceData)
                    if custom_lower(new_location) != 'not mentioned':
                        destination_index_2 = find_index(destination_list, serviceData[glob_index]['placing'])
                    else:
                        destination_index_2 = -1
                    if destination_index_1 != destination_index_2 and destination_index_2 != -1:
                        destinationData[destination_index_2]['amenities'][0].append(serviceData[glob_index]['serviceName'])
                        destinationData[destination_index_2]['amenities'][1].append(serviceData[glob_index]['schedule'])
                        if destination_index_1 != -1:
                            del destinationData[destination_index_1]['amenities'][0][existence_index]
                            del destinationData[destination_index_1]['amenities'][1][existence_index]
                    else:
                        del destinationData[destination_index_2]['amenities'][0][existence_index]
                        del destinationData[destination_index_2]['amenities'][1][existence_index]
                    save_destination_data(destinationData)
                    print("Service update successful")
                else:
                    print("There is no such location available")
            elif custom_lower(to_update) == 'provided quantity' or custom_lower(
                    to_update) == 'quantity' or to_update == '4':
                new_quantity = input(f"Current Quantity: {serviceData[glob_index]['quantity']}\n"
                                     f"New Quantity: ")
                serviceData[glob_index]['quantity'] = new_quantity
                save_service_data(serviceData)
                print("Service update successful")
            elif custom_lower(to_update) == 'price' or to_update == '5':
                new_price = input(f"Current Price: {serviceData[glob_index]['price']}\n"
                                  f"New Price: ")
                serviceData[glob_index]['price'] = new_price
                save_service_data(serviceData)
                print("Service update successful")
            elif custom_lower(to_update) == 'schedule' or to_update == '6':
                new_start_date = input(f"Current schedule: {serviceData[glob_index]['price']}\n"
                                       f"Type new start date 'Day Month' or 'Continuous': ")
                if custom_lower(new_start_date) != 'continuous':
                    new_end_date = input("Type new end date 'Day Month' or 'Continuous': ")
                    schedule = f"From {new_start_date} to {new_end_date}"
                else:
                    schedule = 'continuous'
                serviceData[glob_index]['schedule'] = schedule
                save_service_data(serviceData)
                if destination_index_1 != -1:
                    destinationData[destination_index_1]['amenities'][1][existence_index] = schedule
                save_destination_data(destinationData)
                print("Service update successful")
            elif custom_lower(to_update) == 'exit' or to_update == '7':
                print("Returning to service page...")
                break
            else:
                print("This is not a valid option")


def delete_service(currentUser):
    while True:
        service_list = get_user_service_list(currentUser)
        glob_service_list = get_service_list()
        if service_list[-1] != 'Exit':
            service_list.append('Exit')
        service_list_aux = custom_enumerate(service_list)
        print(f"You are currently providing:\n{'\n'.join(service for service in service_list_aux)}\n")
        to_process = input("Which of your services you would like to delete?\n")
        alternative = [str(index + 1) for index in range(len(service_list))]
        if custom_lower(to_process) == 'exit' or int(to_process) == len(service_list):
            print("Service update cancelled")
            break
        elif custom_lower(to_process) in custom_lower_list(service_list):
            index = find_index(custom_lower_list(service_list), custom_lower(to_process))
            glob_index = find_index(custom_lower_list(glob_service_list), custom_lower(to_process))
        elif to_process in alternative:
            index = int(to_process) - 1
            glob_index = find_index(custom_lower_list(glob_service_list), custom_lower(service_list[index]))
        else:
            print("There is no such service")
            glob_index = -1
        if glob_index != -1:
            confirmation = input(f"Are you sure you want to delete service {service_list[glob_index]}? Yes/No\n")
            if custom_lower(confirmation) == "yes" or confirmation == '1':
                destinationData = open_destination_data()
                serviceData = open_service_data()
                destination_list = get_destination_list()
                destination_index = find_index(destination_list, serviceData[glob_index]['placing'])
                existence_index = find_index(destinationData[destination_index]['amenities'][0], serviceData[glob_index]['serviceName'])
                del serviceData[glob_index]
                del destinationData[destination_index]['amenities'][0][existence_index]
                del destinationData[destination_index]['amenities'][1][existence_index]
                save_service_data(serviceData)
                save_destination_data(destinationData)
                print(f"Service {service_list[glob_index]} deleted successfully")
            else:
                print("Service deletion cancelling")


def explore_services(currentUser):
    serviceData = open_service_data()
    active_service_list = get_active_service_list()
    service_list = get_service_list()
    active_service_list.append('Exit')
    userData = open_userdata()
    login_list = get_login_list()
    user_data_index = find_index(login_list, currentUser['login'])
    while True:
        service_list_aux = custom_enumerate(active_service_list)
        print(f"Available services:\n{'\n'.join(service for service in service_list_aux)}\n")
        # f"You are currently providing:\n{'\n'.join(f"{num + 1}. {service}" for num, service in enumerate(service_list))}\n"
        alternative = [str(index + 1) for index in range(len(active_service_list))]
        to_explore = custom_lower(input("Which one do you want to explore?\n"))
        if to_explore == 'exit' or to_explore == alternative[-1]:
            break
        elif to_explore in custom_lower_list(active_service_list):
            index = find_index(custom_lower_list(service_list), to_explore)
        elif to_explore in alternative:
            index = find_index(service_list, active_service_list[int(to_explore) - 1])
        else:
            index = -1
            print("There is no such service")
        while index != -1:
            print(f"Service name: {serviceData[index]['serviceName']}\n"
                  f"Hosted by: {serviceData[index]['userHost']}\n"
                  f"Location: {serviceData[index]['placing']}\n"
                  f"Provided quantity: {int(serviceData[index]['quantity'])-len(serviceData[index]['booking'])}\n"
                  f"Price: {serviceData[index]['price']}\n"
                  f"Schedule: {serviceData[index]['schedule']}\n")
            if currentUser['userType'] == 'Traveller' and currentUser['login'] not in serviceData[index]['booking']:
                confirmation = custom_lower(input("1. Book\n2. Exit\n"))
                if confirmation == 'exit' or confirmation == '2':
                    break
                elif (confirmation == 'book' or confirmation == '1') and int(serviceData[index]['quantity'])-len(serviceData[index]['booking']) > 0:
                    confirmation = custom_lower(input("Do you wish to book that service?\n1. Yes\n2. No\n"))
                    if confirmation == 'no' or confirmation == '2':
                        print("Booking process cancelled")
                    elif confirmation == 'yes' or confirmation == '1':
                        serviceData[index]['booking'].append(currentUser['login'])
                        userData[user_data_index]["booking"].append(serviceData[index]['serviceName'])
                        save_service_data(serviceData)
                        save_userdata(userData)
                        print(f"{serviceData[index]['serviceName']} booked successfully")
                        break
            elif currentUser['userType'] == 'Traveller' and currentUser['login'] in serviceData[index]['booking']:
                confirmation = custom_lower(input("1. Cancel Booking\n2. Exit\n"))
                if confirmation == 'exit' or confirmation == '2':
                    break
                elif confirmation == 'cancel booking' or confirmation == '1':
                    confirmation = custom_lower(input("Do you wish to cancel your booking?\n1. Yes\n2. No\n"))
                    if confirmation == 'no' or confirmation == '2':
                        print("Booking cancellation interrupted")
                    elif confirmation == 'yes' or confirmation == '1':
                        booking_index = find_index(serviceData[index]['booking'], currentUser['login'])
                        del serviceData[index]['booking'][booking_index]
                        user_index = find_index(userData[user_data_index]['booking'], serviceData[index]['serviceName'])
                        del userData[user_data_index]["booking"][user_index]
                        save_service_data(serviceData)
                        save_userdata(userData)
                        print(f"Booking of {serviceData[index]['serviceName']} cancelled successfully")
                        break
            else:
                confirmation = custom_lower(input("0. Exit\n"))
                if custom_lower(confirmation) == 'exit' or confirmation == '0':
                    break
    currentUser = userData[user_data_index]
    return currentUser


def explore_destinations():
    destinationData = open_destination_data()
    destination_list = get_destination_list()
    destination_list.append('Exit')
    while True:
        destination_list_aux = custom_enumerate(destination_list)
        print(f"Available destinations:\n{'\n'.join(destination for destination in destination_list_aux)}\n")
        alternative = [str(index + 1) for index in range(len(destination_list))]
        to_explore = custom_lower(input("Which one do you want to know more about?\n"))
        if to_explore == 'exit' or to_explore == alternative[-1]:
            break
        elif to_explore in custom_lower_list(destination_list):
            index = find_index(custom_lower_list(destination_list), to_explore)
        elif to_explore in alternative:
            index = int(to_explore) - 1
        else:
            index = -1
        while index != -1:
            print(f"Title: {destinationData[index]['destinationName']}\n"
                  f"Points of interest: {', '.join(POI for POI in destinationData[index]['points of interest'])}")
            if destinationData[index]['amenities'] == [[], []]:
                print("Amenities: Unfortunately, no amenities available at this point")
            else:
                tmp_list = []
                for tmp in range(len(destinationData[index]['amenities'][0])):
                    tmp_list.append(destinationData[index]['amenities'][0][tmp] + ': ' + destinationData[index]['amenities'][1][tmp])
                    tmp_list_aux = custom_enumerate(tmp_list)
                print(f"Amenities:\n{'\n'.join(amenity for amenity in tmp_list_aux)}")
            confirmation = custom_lower(input("Exit\n"))
            if custom_lower(confirmation) == 'exit' or confirmation == '0':
                break


def manage_recommendation(currentUser):
    destinationData = open_destination_data()
    destination_list = get_destination_list()
    destination_list.append('Exit')
    while True:
        recommendation = open_recommendation()
        if currentUser['userType'] != "Admin":
            print("How did you get this option???")
        destination_list_aux = custom_enumerate(destination_list)
        print(f"You are currently recommending: {recommendation[0]}")
        print(f"Available destinations to recommend:\n{'\n'.join(destination for destination in destination_list_aux)}\n")
        alternative = [str(index + 1) for index in range(len(destination_list))]
        to_explore = custom_lower(input("Which one do you want to recommend?\n"))
        if to_explore == 'exit' or to_explore == alternative[-1]:
            break
        elif to_explore in custom_lower_list(destination_list):
            index = find_index(custom_lower_list(destination_list), to_explore)
        elif to_explore in alternative:
            index = int(to_explore) - 1
        else:
            index = -1
        while index != -1:
            confirmation = custom_lower(input("Do you wish to use default structure?\n1. Yes\n2. No\n3. Exit\n"))
            if confirmation == 'yes' or confirmation == '1':
                recommendation[0] = destinationData[index]['destinationName']
                recommendation[3] = recommendation[1]
                recommendation[4] = recommendation[2]
                save_recommendation(recommendation)
                break
            elif confirmation == 'no' or confirmation == '2':
                recommendation[0] = destinationData[index]['destinationName']
                first_part = input(f"Custom structure:'First part', '{destinationData[index]['destinationName']}', 'Second part'\n"
                                   f"Enter the first part:\n")
                second_part = input(f"{first_part} {destinationData[index]['destinationName']} 'Second part'\n"
                                    f"Enter the second part:\n")
                confirmation = custom_lower(input(f"{first_part} {destinationData[index]['destinationName']}{second_part}\n"
                                                  f"Are you satisfied with the result?\n1. Yes\n2. No\n3. Exit\n"))
                if confirmation == 'yes' or confirmation == '1':
                    recommendation[3] = first_part
                    recommendation[4] = second_part
                    save_recommendation(recommendation)
                    break
                elif confirmation == 'no' or confirmation == '2':
                    print("Recommendation update cancelled")
                else:
                    print("This is not a valid option")
            elif confirmation == 'exit' or confirmation == '3':
                break
            else:
                print("This is not a valid option")


def view_recommendation():
    while True:
        recommendation = open_recommendation()
        confirmation = custom_lower(input(f"{recommendation[3]} {recommendation[0]} {recommendation[4]}\nExit\n"))
        if confirmation == 'exit' or confirmation == '0':
            break


def manage_promotions(currentUser):
    while True:
        promotion_list = open_promotions()
        if currentUser['userType'] != "Admin":
            print("How did you get this option???")
        if promotion_list == []:
            print("No promotions currently active\n")
        else:
            print(f"Current promotions:\n{'\n'.join(promotion for promotion in promotion_list)}\n")
        to_process = custom_lower(input("What do you want to do\n1. Add promotion\n2. Delete promotion\n3. Exit\n"))
        if to_process == 'yes' or to_process == '1':
            while True:
                new_promotion = input("Type your promotion:\n")
                confirmation = custom_lower(input("Are you satisfied with the result?\n1. Yes\n2. No\n"))
                if custom_lower(new_promotion) == 'exit':
                    print("Returning to promotions screen")
                    break
                if confirmation == 'yes' or confirmation == '1':
                    promotion_list.append(new_promotion)
                    save_promotions(promotion_list)
                    print("Promotion added successfully\n")
                    break
                elif confirmation == 'no' or confirmation == '2':
                    print("Promotion creation cancelled\n")
                else:
                    print("There is no such option\n")
        elif to_process == 'no' or to_process == '2':
            while True:
                if promotion_list == []:
                    print("There are no promotions to delete")
                    break
                promotion_list_aux = custom_enumerate(promotion_list)
                print(f"Current promotions:\n{'\n'.join(promotion for promotion in promotion_list_aux)}\nExit\n")
                aux_list = [str(index+1) for index in range(len(promotion_list))]
                to_delete = input("Which one do you want to delete?\n")
                if custom_lower(to_delete) == 'exit' or to_delete == '0':
                    print("Returning to promotions screen")
                    break
                if to_delete in aux_list:
                    confirmation = custom_lower(input(f"Are you sure you want to delete next promotion:\n{promotion_list[int(to_delete)-1]}\n1. Yes\n2. No\n"))
                    if confirmation == 'yes' or confirmation == '1':
                        del promotion_list[int(to_delete)-1]
                        save_promotions(promotion_list)
                        print("Promotion successfully deleted")
                        break
                    elif confirmation == 'no' or confirmation == '2':
                        print("Promotion deletion cancelled")
                    else:
                        print("There is no such option")
                else:
                    print("There is no such option")
        elif to_process == 'exit' or to_process == '3':
            print("Returning to options screen")
            break
        else:
            print("There are no such option")


def view_promotions():
    while True:
        promotion_list = open_promotions()
        if promotion_list == []:
            confirmation = input("Unfortunately, there are no available promotions at the moment\nExit")
            if confirmation == 'exit' or confirmation == '0':
                print("Returning to options screen")
                break
        else:
            promotion_list_aux = custom_enumerate(promotion_list)
            confirmation = custom_lower(input(f"Current promotions:\n{'\n'.join(promotion for promotion in promotion_list_aux)}\nExit\n"))
            if confirmation == 'exit' or confirmation == '0':
                print("Returning to options screen")
                break


def manage_booking(currentUser):
    userData = open_userdata()
    serviceData = open_service_data()
    service_list = get_service_list()
    lower_service_list = custom_lower_list(service_list)
    login_list = get_login_list()
    user_data_index = find_index(login_list, currentUser['login'])
    if currentUser['userType'] == 'Traveller':
        while True:
            if currentUser['booking'] == []:
                confirmation = custom_lower(input("You don't have anything booked at this moment\n0. Exit"))
                if confirmation == 'exit' or confirmation == '0':
                    print("Returning to options screen")
                    break
            else:
                booking_list_aux = custom_enumerate(currentUser['booking'])
                alternative = [str(index+1) for index in range(len(currentUser['booking']))]
                confirmation = custom_lower(input(f"{'\n'.join(booking for booking in booking_list_aux)}\n0. Exit\n"))
                if confirmation == 'exit' or confirmation == '0':
                    print("Returning to options screen")
                    break
                elif confirmation in lower_service_list:
                    index = find_index(lower_service_list, confirmation)
                elif confirmation in alternative:
                    index = find_index(service_list, currentUser['booking'][int(confirmation) - 1])
                    # print(f"index: {index}"
                    #       f"service list: {service_list}"
                    #       f"booking selected: {currentUser['booking'][int(confirmation) - 1]}")
                else:
                    print("There is no such option")
                    index = -1
                while index != -1:
                    print(f"Service name: {serviceData[index]['serviceName']}\n"
                          f"Hosted by: {serviceData[index]['userHost']}\n"
                          f"Location: {serviceData[index]['placing']}\n"
                          f"Provided quantity: {int(serviceData[index]['quantity']) - len(serviceData[index]['booking'])}\n"
                          f"Price: {serviceData[index]['price']}\n"
                          f"Schedule: {serviceData[index]['schedule']}\n")
                    confirmation = custom_lower(input("1. Cancel Booking\n2. Exit\n"))
                    if confirmation == 'exit' or confirmation == '2':
                        break
                    elif confirmation == 'cancel booking' or confirmation == '1':
                        confirmation = custom_lower(input("Do you wish to cancel your booking?\n1. Yes\n2. No\n"))
                        if confirmation == 'no' or confirmation == '2':
                            print("Booking cancellation interrupted")
                        elif confirmation == 'yes' or confirmation == '1':
                            booking_index = find_index(serviceData[index]['booking'], currentUser['login'])
                            del serviceData[index]['booking'][booking_index]
                            user_index = find_index(userData[user_data_index]['booking'],
                                                    serviceData[index]['serviceName'])
                            del userData[user_data_index]["booking"][user_index]
                            save_service_data(serviceData)
                            save_userdata(userData)
                            currentUser = userData[user_data_index]
                            print(f"Booking of {serviceData[index]['serviceName']} cancelled successfully")
                            break
    elif currentUser['userType'] == 'Service':
        while True:
            users_list = get_login_list()
            lower_users_list = custom_lower_list(users_list)
            user_service_list = get_user_service_list(currentUser)
            if user_service_list == []:
                confirmation = input("You do not currently provide any services to book\n0. Exit\n")
                if confirmation == 'exit' or confirmation == '0':
                    print("Returning to options screen")
                    break
                else:
                    print("This is not a valid option")
            else:
                lower_user_service_list = custom_lower_list(user_service_list)
                user_service_list_aux = custom_enumerate(user_service_list)
                confirmation = custom_lower(input(f"{'\n'.join(service for service in user_service_list_aux)}\n0. Exit\n"))
                alternative = [str(index + 1) for index in range(len(user_service_list))]
                if confirmation == 'exit' or confirmation == '0':
                    print("Returning to options screen")
                    break
                elif confirmation in lower_user_service_list:
                    index = find_index(lower_service_list, confirmation)
                elif confirmation in alternative:
                    index = find_index(service_list, user_service_list[int(confirmation) - 1])
                else:
                    print("There is no such option")
                    index = -1
                while index != -1:
                    booked_users_list = serviceData[index]['booking']
                    if booked_users_list == []:
                        print("This service has not got any bookings at this moment")
                    else:
                        booked_users_list_aux = custom_enumerate(booked_users_list)
                        lower_booked_users_list = custom_lower_list(booked_users_list)
                        print(f"Service name: {serviceData[index]['serviceName']}\n"
                              f"Booked by:\n{'\n'.join(user for user in booked_users_list_aux)}\n0. Exit\n")
                        confirmation = custom_lower(input("Which booking you would like to cancel?\n"))
                        alternative = [str(index + 1) for index in range(len(booked_users_list))]
                        if confirmation == 'exit' or confirmation == '0':
                            print("Returning to service screen")
                            break
                        elif confirmation in lower_booked_users_list:
                            booked_index = find_index(lower_users_list, confirmation)
                        elif confirmation in alternative:
                            booked_index = find_index(users_list, booked_users_list[int(confirmation)-1])
                        else:
                            booked_index = -1
                        while booked_index != -1:
                            confirmation = custom_lower(input(f"Are you sure you want to cancel following booking:\n"
                                                              f"Service: {serviceData[index]['serviceName']}\n"
                                                              f"User: {userData[booked_index]['login']}\n1. Yes\n2. No\n"))
                            if confirmation == 'no' or confirmation == '2':
                                print("Returning to booking screen")
                                break
                            elif confirmation == 'yes' or confirmation == '1':
                                index_tmp = find_index(serviceData[index]['booking'], userData[booked_index]['login'])
                                del serviceData[index]['booking'][index_tmp]
                                index_tmp = find_index(userData[booked_index]['booking'], serviceData[index]['serviceName'])
                                del userData[booked_index]['booking'][index_tmp]
                                save_service_data(serviceData)
                                save_userdata(userData)
                                print("Booking cancelled successfully")
                                break
                            else:
                                print("There is no such option")
    else:
        print("How did you get this option???")
    return currentUser


def main():
    currentUser = assign_guest()
    # tmp = get_login_list()
    # print(tmp)
    # login_list = get_login_list()
    # print(login_list)
    interact_with_options(currentUser)


main()

# data = open_userdata()
# print(*data, sep='\n')
