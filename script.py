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
        options = ['Log in', 'Log out', 'Block User', 'Unblock User', 'Delete Account', 'Update promotion(in development)', 'Provide trip recommendation(in development)']
    elif currentUser['userType'] == 'Service':
        options = ['Log in', 'Log out', 'Manage Services', 'Manage Booking(in development)', 'Delete Account']
    elif currentUser['userType'] == 'Traveller':
        options = ['Log in', 'Log out', 'Explore Services(in development)', 'Explore Destinations(in development)', 'View recommended(in development)', 'Check availability(in development)', 'Delete Account']
    elif currentUser['userType'] == 'Guest':
        options = ['Log in', 'Sign up', 'Explore Services(in development)', 'Explore Destinations(in development)', 'View recommended(in development)', 'Check availability(in development)', 'Delete Account']
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
        pass
    elif index == 10:
        pass
    elif index == 11:
        pass
    else:
        print("There are no such option available")
        return 0, currentUser


def interact_with_options(currentUser):
    full_options = ['log in', 'sign up', 'search', 'block user', 'unblock user', 'delete account', 'log out', 'exit',
                    'manage services', 'add service', 'update service', 'delete service']
    while True:
        check = 0
        print(f"\n\nYou are currently logged as {currentUser['userType']}\n"
              f"With your current access rights, you have access to: ")
        options_to_show = show_options(currentUser)
        options_to_process = custom_lower_list(options_to_show)
        # options_to_process = []
        # for i in range(len(options_to_show)):
        #     options_to_process.append(custom_lower(options_to_show[i]))
        alternative = [(index+1) for index in range(len(options_to_show))]
        print('\n'.join(f"{num+1}. {option}" for num, option in enumerate(options_to_show)))
        # print(options_to_process)
        choice = custom_lower(input("What would you like to do?\n"))
        if choice in options_to_process:
            index = find_index(full_options, choice)
            check, currentUser = function_call(index, currentUser)
        elif int(choice) in alternative:
            index = find_index(full_options, options_to_process[int(choice)-1])
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
        elif userType == 'traveler' or userType == '3':
            newUser['userType'] = 'Traveller'
        else:
            print("There is no such account type, enter valid option")
    newUser['login'] = input("Please, set your login: ")
    while True:
        password_set = input("Please, set your password: ")
        password_confirmation = input("Please, confirm your password: ")
        if password_set == password_confirmation:
            newUser['password'] = password_confirmation
            break
        else:
            print("Passwords do not match")
    newUser['active'] = True
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


def get_destination_list():
    destination_list = []
    destinationData = open_destination_data()
    for destination in destinationData:
        destination_list.append(destination['destinationName'])
    return destination_list


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
            to_process = input("What would you like to do?\n1. Add Service\n2. Update Services\n3. Delete Service\n4. Exit\n")
        if custom_lower(to_process) == "exit" or to_process == '4':
            break
        elif custom_lower(to_process) == "add service" or to_process == '1':
            add_service(currentUser)
        elif custom_lower(to_process) == "update service" or to_process == '2':
            update_service(service_list)
        elif custom_lower(to_process) == "delete service" or to_process == '3':
            pass


def add_service(currentUser):
    new_service = {}
    new_service['serviceName'] = input("Enter the service's name\n")
    new_service['userHost'] = currentUser['login']
    confirmation = input("Do you want to associate your service with a location? Yes/No\n")
    if custom_lower(confirmation) == 'yes' or confirmation == '1':
        destination_list = get_destination_list()
        lower_destination_list = custom_lower_list(destination_list)
        # print(f"LIST = {lower_destination_list}")
        while True:
            location_to_associate = input(f"Currently available destinations:\n{'\n'.join(destination for destination in destination_list)}\nExit\n")
            if custom_lower(location_to_associate) == 'exit':
                new_service["placing"] = 'Not mentioned'
                break
            elif custom_lower(location_to_associate) in lower_destination_list:
                new_service["placing"] = location_to_associate
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
    else:
        print("Service creation cancelled")


# def update_service_aux()


def update_service(service_list):
    while True:
        if service_list[-1] != 'Exit':
            service_list.append('Exit')
        print(f"You are currently providing:\n{'\n'.join(f"{num+1}. {service}" for num, service in enumerate(service_list))}\n")
        to_process = input("Which of your services you would like to update?\n")
        alternative = [str(index + 1) for index in range(len(service_list))]
        if custom_lower(to_process) == 'exit' or int(to_process) == len(service_list):
            print("Service update cancelled")
            break
        elif custom_lower(to_process) in custom_lower_list(service_list):
            index = find_index(custom_lower_list(service_list), custom_lower(to_process))
        elif to_process in alternative:
            index = int(to_process) - 1
        else:
            print("There is no such service")
            index = -1
        while index != -1:
            serviceData = open_service_data()
            print(f"1. Service name: {serviceData[index]['serviceName']}\n"
                  f"2. Hosted by: {serviceData[index]['userHost']}\n"
                  f"3. Location: {serviceData[index]['placing']}\n"
                  f"4. Provided quantity: {serviceData[index]['quantity']}\n"
                  f"5. Price: {serviceData[index]['price']}\n"
                  f"6. Schedule: {serviceData[index]['schedule']}\n"
                  f"7. Exit")
            to_update = input("Which part you would like to update?\n")
            if custom_lower(to_update) == 'service name' or custom_lower(to_update) == 'name' or to_update == '1':
                new_name = input(f"Current Service name: {serviceData[index]['serviceName']}\n"
                                 f"New Service name: ")
                serviceData[index]['serviceName'] = new_name
                save_service_data(serviceData)
                print("Service update successful")
            elif custom_lower(to_update) == 'hosted by' or to_update == '2':
                print("You can not update this")
            elif custom_lower(to_update) == 'location' or to_update == '3':
                destination_list = get_destination_list()
                destination_list.append('Not mentioned')
                new_location = input(f"Current Location: {serviceData[index]['placing']}\n"
                                     f"Available locations:\n{'\n'.join(destination for destination in destination_list)}\n"
                                     f"New Location: ")
                if custom_lower(new_location) in custom_lower_list(destination_list):
                    serviceData[index]['placing'] = new_location
                    save_service_data(serviceData)
                    print("Service update successful")
                else:
                    print("There is no such location available")
            elif custom_lower(to_update) == 'provided quantity' or custom_lower(to_update) == 'quantity' or to_update == '4':
                new_quantity = input(f"Current Quantity: {serviceData[index]['quantity']}\n"
                                     f"New Quantity: ")
                serviceData[index]['quantity'] = new_quantity
                save_service_data(serviceData)
                print("Service update successful")
            elif custom_lower(to_update) == 'price' or to_update == '5':
                new_price = input(f"Current Price: {serviceData[index]['price']}\n"
                                  f"New Price: ")
                serviceData[index]['price'] = new_price
                save_service_data(serviceData)
                print("Service update successful")
            elif custom_lower(to_update) == 'schedule' or to_update == '6':
                new_start_date = input(f"Current schedule: {serviceData[index]['price']}\n"
                                       f"Type new start date 'Day Month' or 'Continuous': ")
                if custom_lower(new_start_date) != 'continuous':
                    new_end_date = input("Type new end date 'Day Month' or 'Continuous': ")
                    schedule = f"From {new_start_date} to {new_end_date}"
                else:
                    schedule = 'continuous'
                serviceData[index]['schedule'] = schedule
                save_service_data(serviceData)
                print("Service update successful")
            elif custom_lower(to_update) == 'exit' or to_update == '7':
                print("Returning to service page...")
                break
            else:
                print("This is not a valid option")

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
