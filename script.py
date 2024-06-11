import json


# Segment for emulation banned inbuilt function


def custom_lower(input_string):
    # Gets a string as input, returns the same string but with capital letters being replaced by lower ones
    result = ""
    for char in input_string:
        if 'A' <= char <= 'Z':
            lower_char = chr(ord(char) + 32)
            result += lower_char
        else:
            result += char
    return result


def custom_lower_list(uncertain_list):
    # Gets a list of strings as input, returns list with same strings, but capital letters replaced with lower ones
    lower_list = []
    for element in uncertain_list:
        lower_list.append(custom_lower(element))
    return lower_list


def custom_enumerate(main_list):
    # Gets a list of lines as input, returns list with added 'n. ' to each line, where n represents ordeal number
    aux_list = []
    counter = 1
    for _ in main_list:
        aux_list.append(str(counter) + '. ' + main_list[counter - 1])
        counter += 1
    return aux_list


def find_index(custom_list, element):
    # Returns index of a certain element in the certain list
    counter = 0
    for content in custom_list:
        if content == element:
            return counter
        counter += 1

# Segment for external file handling: getting data from file and saving data into the file


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

# Segment for some auxiliary functions


def get_login_list():
    # Returns list of all users registered in the system
    userData = open_userdata()
    login_list = [user['login'] for user in userData]
    return login_list


def get_active_login_list():
    # Returns list of all users in the system, whose accounts are not blocked
    userData = open_userdata()
    active_login_list = []
    for user in userData:
        if user['active']:
            active_login_list.append(user['login'])
    return active_login_list


def get_blocked_login_list():
    # Returns list of all users in the system, whose accounts are blocked
    userData = open_userdata()
    blocked_login_list = []
    for user in userData:
        if not user['active']:
            blocked_login_list.append(user['login'])
    return blocked_login_list


def get_service_list():
    # Returns list of all services in the system, including ones from blocked users
    service_list = []
    serviceData = open_service_data()
    for service in serviceData:
        service_list.append(service['serviceName'])
    return service_list


def get_active_service_list():
    # Return list of all services in the system, that are made by users that are currently active(not blocked)
    userData = open_userdata()
    active_service_list = []
    serviceData = open_service_data()
    for service in serviceData:
        Host = service['userHost']
        for user in userData:
            if user['login'] == Host and user['active']:
                active_service_list.append(service['serviceName'])
    return active_service_list


def get_user_service_list(currentUser):
    # Returns list of services, provided by a certain user
    service_list = []
    serviceData = open_service_data()
    for service in serviceData:
        if service['userHost'] == currentUser['login']:
            service_list.append(service['serviceName'])
    return service_list


def get_destination_list():
    # Returns list of all destinations in the system
    destination_list = []
    destinationData = open_destination_data()
    for destination in destinationData:
        destination_list.append(destination['destinationName'])
    return destination_list

# Segment with big functions, each of which represents a certain functionality


def assign_guest():
    # Default user, exploring the system
    currentUser = {
        "userType": "Guest",
        "login": "default",
        "password": "default",
        "active": True
    }
    return currentUser


def interact_with_options(currentUser):
    # This is a main cycle of the system, basically the main menu
    # Handles showing options based on User Type, reading input from the main menu and terminating the program
    # Full options here because I couldn't come up with more elegant solution to allow input not only as digits
    # But also as actual character input
    full_options = ['log in', 'sign up', 'block user', 'unblock user', 'delete account', 'log out', 'exit',
                    'manage services', 'explore services', 'explore destinations', 'provide trip recommendation',
                    'view recommended', 'update promotions', 'view promotions', 'manage booking', 'plan my trip']
    while True:
        # check = 0
        print(f"\n\nYou are currently logged as {currentUser['userType']}\n"
              f"With your current access rights, you have access to: ")
        options_to_show = show_options(currentUser)
        options_to_process = custom_lower_list(options_to_show)
        alternative = [str(index + 1) for index in range(len(options_to_show))]
        options_to_show_aux = custom_enumerate(options_to_show)
        print(f"{'\n'.join(option for option in options_to_show_aux)}\n0. Exit")
        choice = custom_lower(input("What would you like to do?\n"))
        if choice == 'exit' or choice == '0':
            break
        elif choice in options_to_process:
            index = find_index(full_options, choice)
            currentUser = function_call(index, currentUser)
        elif choice in alternative:
            index = find_index(full_options, options_to_process[int(choice) - 1])
            currentUser = function_call(index, currentUser)
        else:
            print("There are no such option")
        # if check == 1:
        #     break


def show_options(currentUser):
    # This is what options are presented to user based on their User type
    # Also couldn't come up with more alegant solution
    options = []
    if currentUser['userType'] == 'Admin':
        options = ['Log in', 'Log out', 'Sign up', 'Block User', 'Unblock User', 'Delete Account',
                   'Update promotions', 'Provide trip recommendation']
    elif currentUser['userType'] == 'Service':
        options = ['Log in', 'Log out', 'Sign up', 'Manage Services', 'Manage Booking', 'Delete Account']
    elif currentUser['userType'] == 'Traveller':
        options = ['Log in', 'Log out', 'Sign up', 'View promotions', 'Explore Services', 'View recommended',
                   'Explore Destinations', 'Plan my trip', 'Manage Booking', 'Delete Account']
    elif currentUser['userType'] == 'Guest':
        options = ['Log in', 'Sign up', 'View promotions', 'Explore Services', 'View recommended',
                   'Explore Destinations']
    # options.append("Exit")
    return options


def function_call(index, currentUser):
    # Auxiliary function that is made to be used in interact_with_options, as both input as digits and letters are possible
    # What I wanted to do is to make specific function for each option and lock it with specific index, so I can easily call
    # This specific function with this index. However, I can't put functions in a list, so I had to create
    # Something similar myself, but it is hardcoded, therefore expandability is not easily performed
    if index == 0:
        currentUser = log_in_account(currentUser)
        return currentUser
    elif index == 1:
        currentUser = create_account(currentUser)
        return currentUser
    elif index == 2:
        block_account(currentUser)
        return currentUser
    elif index == 3:
        unblock_account(currentUser)
        return currentUser
    elif index == 4:
        currentUser = delete_account(currentUser)
        return currentUser
    elif index == 5:
        currentUser = log_out(currentUser)
        return currentUser
    # elif index == 6:
    #     return 1, currentUser
    elif index == 7:
        manage_services(currentUser)
        return currentUser
    elif index == 8:
        currentUser = explore_services(currentUser)
        return currentUser
    elif index == 9:
        explore_destinations()
        return currentUser
    elif index == 10:
        manage_recommendation(currentUser)
        return currentUser
    elif index == 11:
        view_recommendation()
        return currentUser
    elif index == 12:
        manage_promotions(currentUser)
        return currentUser
    elif index == 13:
        view_promotions()
        return currentUser
    elif index == 14:
        currentUser = manage_booking(currentUser)
        return currentUser
    elif index == 15:
        plan_my_trip(currentUser)
        return currentUser
    else:
        print("There are no such option available")
        return currentUser


def create_account(currentUser):
    # Creating account based on user input, prompting to stay signed once account created
    # Admin accounts can be created only if you are already logged in as Admin
    userData = open_userdata()
    newUser = {'userType': 'default'}

    while newUser['userType'] == 'default':
        userType = custom_lower(input("Please, enter which account you want to create:\n1. Admin\n2. Service\n3. Traveller\n0. Exit\n"
                                      "Be aware that only Admins are allowed to create additional Admin accounts\n"))
        if userType == 'exit' or userType == '0':
            print("Returning to main menu")
            return currentUser
        elif (userType == 'admin' or userType == '1') and currentUser['userType'] == 'Admin':
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
        newUser['path'] = []
    userData.append(newUser)
    print("Account created successfully")

    confirmation = custom_lower(input("Would you like to stay signed in this account?\n1. Yes\n2. No\n"))
    if confirmation == "yes" or confirmation == "1":
        userData = open_userdata()
        currentUser = userData[-1]
    elif confirmation == 'no' or confirmation == '2':
        print("Returning to main menu")
    save_userdata(userData)
    return currentUser


def log_in_account(currentUser):
    # Log in account, what else to say - prompting login and password, returning user profile
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


def log_out(currentUser):
    # Log out function
    while True:
        confirmation = custom_lower(input("Are you sure you want to log out?\n1. Yes\n2. No\n"))
        if confirmation == "yes" or confirmation == "1":
            currentUser = assign_guest()
            return currentUser
        elif confirmation == 'no' or confirmation == '2':
            print("Log out cancelled")
            return currentUser
        else:
            print("There is no such option")


def block_account(currentUser):
    # Admin - exclusive, allows them to suspend an account, blocking the person from using the system
    # Removing all services provided by user, as well as other people's booking of these services
    while True:
        if currentUser['userType'] != 'Admin':
            print("How did you get this option???")
        active_users = get_active_login_list()
        blocked_users = get_blocked_login_list()
        print(f"Currently active users:\n{'\n'.join(user for user in active_users)}\n0. Exit\n")
        user_to_block = input("Which user do you want to block?\n")
        if user_to_block == "0" or user_to_block == '0':
            break
        elif user_to_block in active_users and user_to_block != currentUser['login']:
            confirmation = custom_lower(input(f"Are you sure you want to block user {user_to_block}?\n1. Yes\n2. No\n"))
            if confirmation == 'yes' or confirmation == '1':
                login_list = get_login_list()
                index = find_index(login_list, user_to_block)
                userData = open_userdata()
                userData[index]['active'] = False
                cancel_users_booking(userData[index])
                save_userdata(userData)
                print(f"User {user_to_block} successfully blocked")
            elif confirmation == 'no' or confirmation == '2':
                print("User blocking cancelled")
        elif user_to_block in active_users and user_to_block == currentUser['login']:
            print("You can not block yourself")
        elif user_to_block in blocked_users:
            print(f"User {user_to_block} is already blocked")
        else:
            print(f"User {user_to_block} not found")
        tmp = input("Do you wish to continue blocking?\n1. Yes\n2. No\n")
        if custom_lower(tmp) == 'no' or tmp == '2':
            break


def unblock_account(currentUser):
    # Admin - exclusive, allows them to unblock user, giving back their right to use the system.
    # In case of Merchants, their services are NOT restored and has to be registered again
    while True:
        if currentUser['userType'] != 'Admin':
            print("How did you get this option???")
        active_users = get_active_login_list()
        blocked_users = get_blocked_login_list()
        if blocked_users == []:
            print("There are no currently blocked users")
            break
        print(f"Currently blocked users:\n{'\n'.join(user for user in blocked_users)}\n0. Exit\n")
        user_to_unblock = input("Which user do you want to unblock?\n")
        if user_to_unblock == "0" or user_to_unblock == 'exit':
            break
        elif user_to_unblock in blocked_users:
            confirmation = custom_lower(input(f"Are you sure you want to unblock user {user_to_unblock}?\n1. Yes\n2. No\n"))
            if confirmation == 'yes' or confirmation == '1':
                login_list = get_login_list()
                index = find_index(login_list, user_to_unblock)
                userData = open_userdata()
                userData[index]['active'] = True
                save_userdata(userData)
                print(f"User {user_to_unblock} successfully unblocked")
            elif confirmation == 'no' or confirmation == '2':
                print("User unblocking cancelled")
        elif user_to_unblock in active_users:
            print(f"User {user_to_unblock} is not blocked")
        else:
            print(f"User {user_to_unblock} not found")
        tmp = input("Do you wish to continue unblocking?\n1. Yes\n2. No\n")
        if custom_lower(tmp) == 'no' or tmp == '2':
            break


def delete_account(currentUser):
    # Allows Admin to delete every user except for himself
    # Allows everyone else to delete theirs account
    userData = open_userdata()
    login_list = get_login_list()
    login_list_aux = custom_enumerate(login_list)
    for user in login_list:
        index_tmp = find_index(login_list, user)
        if not userData[index_tmp]['active']:
            login_list_aux[index_tmp] += ' (blocked)'
    if currentUser['userType'] == 'Admin':
        print(f"User list:\n{'\n'.join(user for user in login_list_aux)}\n0. Exit\n")
        user_to_delete = input("Write, which user you want to delete\n")
        alternative = [str(index+1) for index in range (len(login_list))]
        if user_to_delete == 'exit' or user_to_delete == '0':
            print("Returning to main menu")
            return currentUser
        elif user_to_delete in login_list:
            confirmation = custom_lower(input(f"Are you sure you want to delete user {user_to_delete}?\n1. Yes\n2. No\n"))
            if confirmation == 'yes' or confirmation == '1':
                index = find_index(login_list, user_to_delete)
                cancel_users_booking(userData[index])
                del userData[index]
                save_userdata(userData)
                print(f'User {user_to_delete} successfully deleted')
            elif confirmation == 'no' or confirmation == '2':
                print("Deletion cancelled")
            else:
                print("There is no such option")
        elif user_to_delete in alternative:
            confirmation = custom_lower(input(f"Are you sure you want to delete user {login_list[int(user_to_delete)-1]}?\n1. Yes\n2. No\n"))
            if confirmation == 'yes' or confirmation == '1':
                index = int(user_to_delete)-1
                cancel_users_booking(userData[index])
                del userData[index]
                save_userdata(userData)
                print(f'User {login_list[int(user_to_delete)-1]} successfully deleted')
            elif confirmation == 'no' or confirmation == '2':
                print("Deletion cancelled")
            else:
                print("There is no such option")
        else:
            print(f"User {user_to_delete} not found")
        return currentUser
    else:
        user_to_delete = currentUser["login"]
        confirmation = custom_lower(input(f"Are you sure you want to delete your account {user_to_delete}?\n1. Yes\n2. No\n"))
        if confirmation == 'yes' or confirmation == '1':
            index = find_index(login_list, user_to_delete)
            cancel_users_booking(userData[index])
            del userData[index]
            save_userdata(userData)
            print(f'Your account {user_to_delete} successfully deleted')
            currentUser = assign_guest()
            return currentUser
        elif confirmation == 'no' or confirmation == '2':
            print('Account deletion cancelled')
            return currentUser


def cancel_users_booking(user):
    # Auxiliary function that is used to delete booking information of a person from database
    serviceData = open_service_data()
    userData = open_userdata()
    user['booking'] = []
    for service in serviceData:
        if user['login'] in service['booking']:
            index = find_index(service['booking'], user['login'])
            del service['booking'][index]
    save_service_data(serviceData)
    save_userdata(userData)


def manage_services(currentUser):
    # Merchant - exclusive
    # Submenu, leading to three other options: Adding service, Deleting service and Managing service
    while True:
        if currentUser['userType'] != "Service":
            print("How did you get this option???")
        service_list = get_user_service_list(currentUser)
        if service_list == []:
            to_process = input("What would you like to do?\n1. Add Service\n0. Exit\n")
        else:
            service_list_aux = custom_enumerate(service_list)
            print(f"You are currently providing:\n{'\n'.join(service for service in service_list_aux)}\n")
            to_process = input(
                "What would you like to do?\n1. Add Service\n2. Update Services\n3. Delete Service\n0. Exit\n")
        if custom_lower(to_process) == "exit" or to_process == '0':
            break
        elif custom_lower(to_process) == "add service" or to_process == '1':
            add_service(currentUser)
        elif custom_lower(to_process) == "update service" or to_process == '2':
            update_service(currentUser)
        elif custom_lower(to_process) == "delete service" or to_process == '3':
            delete_service(currentUser)


def add_service(currentUser):
    # Creating new service from users input, prompts helping user all the way through
    # All services can be bound to existing destination for user's convenience in planning
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
    confirmation = custom_lower(input("Do you want to associate your service with a location?\n1. Yes\n2. No\n"))
    if confirmation == 'yes' or confirmation == '1':
        destination_list = get_destination_list()
        lower_destination_list = custom_lower_list(destination_list)
        # print(f"LIST = {lower_destination_list}")
        while True:
            location_to_associate = custom_lower(input(
                f"Currently available destinations:\n{'\n'.join(destination for destination in destination_list)}\n0. Exit\n"))
            if location_to_associate == 'exit' or location_to_associate == '0':
                new_service["placing"] = 'Not mentioned'
                break
            elif location_to_associate in lower_destination_list:
                inside_index = find_index(lower_destination_list, location_to_associate)
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


def update_service(currentUser):
    # Update information on already created service
    # This part was highly modified in the process, so it's a bit messy, should be redone if I have time
    while True:
        service_list = get_user_service_list(currentUser)
        glob_service_list = get_service_list()
        service_list_aux = custom_enumerate(service_list)
        print(f"You are currently providing:\n{'\n'.join(service for service in service_list_aux)}\n0. Exit")
        to_process = custom_lower(input("Which of your services you would like to update?\n"))
        alternative = [str(index + 1) for index in range(len(service_list))]
        if to_process == 'exit' or to_process == '0':
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
            # glob_index is index in global service list
            destinationData = open_destination_data()
            destination_list = get_destination_list()
            serviceData = open_service_data()
            if serviceData[glob_index]['placing'] != 'Not mentioned':
                destination_index_1 = find_index(destination_list, serviceData[glob_index]['placing'])
                # destination_index_1 allows to access service's placing before updating its settings
                existence_index = find_index(destinationData[destination_index_1]['amenities'][0], serviceData[glob_index]['serviceName'])
                # existence_index allows to access destination-bound service's index inside this destination's data
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
                        # destination_index_2 allows to access service's placing after updating its settings
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
    # Deletes service and all the booking associated with it
    while True:
        service_list = get_user_service_list(currentUser)
        glob_service_list = get_service_list()
        service_list_aux = custom_enumerate(service_list)
        print(f"You are currently providing:\n{'\n'.join(service for service in service_list_aux)}\n0. Exit\n")
        to_process = custom_lower(input("Which of your services you would like to delete?\n"))
        alternative = [str(index + 1) for index in range(len(service_list))]
        if to_process == 'exit' or to_process == '0':
            print("Service deletion cancelled")
            break
        elif to_process in custom_lower_list(service_list):
            index = find_index(custom_lower_list(service_list), to_process)
            glob_index = find_index(custom_lower_list(glob_service_list), to_process)
        elif to_process in alternative:
            index = int(to_process) - 1
            glob_index = find_index(glob_service_list, service_list[index])
        else:
            print("There is no such service")
            glob_index = -1
        if glob_index != -1:
            confirmation = custom_lower(input(f"Are you sure you want to delete service {service_list[index]}?\n1. Yes\n2. No\n"))
            if confirmation == "yes" or confirmation == '1':
                destinationData = open_destination_data()
                serviceData = open_service_data()
                destination_list = get_destination_list()
                userData = open_userdata()
                login_list = get_login_list()
                for user in serviceData[glob_index]['booking']:
                    booking_index_1 = find_index(login_list, user)
                    booking_index_2 = find_index(userData[booking_index_1]['booking'], serviceData[glob_index]['serviceName'])
                    del userData[booking_index_1]['booking'][booking_index_2]
                print(destination_list)
                print(serviceData[glob_index]['placing'])
                destination_index = find_index(destination_list, serviceData[glob_index]['placing'])
                existence_index = find_index(destinationData[destination_index]['amenities'][0], serviceData[glob_index]['serviceName'])
                del serviceData[glob_index]
                del destinationData[destination_index]['amenities'][0][existence_index]
                del destinationData[destination_index]['amenities'][1][existence_index]
                save_userdata(userData)
                save_service_data(serviceData)
                save_destination_data(destinationData)
                print(f"Service {glob_service_list[glob_index]} deleted successfully")
            else:
                print("Service deletion cancelling")


def explore_services(currentUser):
    # For Guests and Travellers - Allow them to see service list, then choose one of them to see additional info
    # Travellers can also make a booking from this menu as well as cancel already booked service
    serviceData = open_service_data()
    active_service_list = get_active_service_list()
    service_list = get_service_list()
    userData = open_userdata()
    login_list = get_login_list()
    user_data_index = find_index(login_list, currentUser['login'])
    while True:
        service_list_aux = custom_enumerate(active_service_list)
        print(f"Available services:\n{'\n'.join(service for service in service_list_aux)}\n0. Exit\n")
        alternative = [str(index + 1) for index in range(len(active_service_list))]
        to_explore = custom_lower(input("Which one do you want to explore?\n"))
        if to_explore == 'exit' or to_explore == '0':
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
                confirmation = custom_lower(input("1. Book\n0. Exit\n"))
                if confirmation == 'exit' or confirmation == '0':
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
                confirmation = custom_lower(input("1. Cancel Booking\n0. Exit\n"))
                if confirmation == 'exit' or confirmation == '0':
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
    # For Guests and Travellers - Allow them to see destinations list, then choose one of them to see additional info
    # Such as Points of interest nearby and associated services
    destinationData = open_destination_data()
    destination_list = get_destination_list()
    while True:
        destination_list_aux = custom_enumerate(destination_list)
        print(f"Available destinations:\n{'\n'.join(destination for destination in destination_list_aux)}\n0. Exit\n")
        alternative = [str(index + 1) for index in range(len(destination_list))]
        to_explore = custom_lower(input("Which one do you want to know more about?\n"))
        if to_explore == 'exit' or to_explore == '0':
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
            confirmation = custom_lower(input("0. Exit\n"))
            if custom_lower(confirmation) == 'exit' or confirmation == '0':
                break


def manage_recommendation(currentUser):
    # For Admins - allow them to construct a recommendation for one of the existing destinations
    # There is a choice between default recommendation structure(auto filled) and custom, made by user themselves
    destinationData = open_destination_data()
    destination_list = get_destination_list()
    while True:
        recommendation = open_recommendation()
        if currentUser['userType'] != "Admin":
            print("How did you get this option???")
        destination_list_aux = custom_enumerate(destination_list)
        print(f"You are currently recommending: {recommendation[0]}")
        print(f"Available destinations to recommend:\n{'\n'.join(destination for destination in destination_list_aux)}\n0. Exit\n")
        alternative = [str(index + 1) for index in range(len(destination_list))]
        to_explore = custom_lower(input("Which one do you want to recommend?\n"))
        if to_explore == 'exit' or to_explore == '0':
            break
        elif to_explore in custom_lower_list(destination_list):
            index = find_index(custom_lower_list(destination_list), to_explore)
        elif to_explore in alternative:
            index = int(to_explore) - 1
        else:
            index = -1
        while index != -1:
            confirmation = custom_lower(input("Do you wish to use default structure?\n1. Yes\n2. No\n0. Exit\n"))
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
                                                  f"Are you satisfied with the result?\n1. Yes\n2. No\n"))
                if confirmation == 'yes' or confirmation == '1':
                    recommendation[3] = first_part
                    recommendation[4] = second_part
                    save_recommendation(recommendation)
                    break
                elif confirmation == 'no' or confirmation == '2':
                    print("Recommendation update cancelled")
                else:
                    print("This is not a valid option")
            elif confirmation == 'exit' or confirmation == '0':
                break
            else:
                print("This is not a valid option")


def view_recommendation():
    # For Guests and Travellers - Allow them to see current recommendation
    while True:
        recommendation = open_recommendation()
        confirmation = custom_lower(input(f"{recommendation[3]} {recommendation[0]} {recommendation[4]}\n0. Exit\n"))
        if confirmation == 'exit' or confirmation == '0':
            break


def manage_promotions(currentUser):
    # For Admins - allow them to add and delete promotions of services
    # Free style, doesn't require to choose from existing service
    while True:
        promotion_list = open_promotions()
        if currentUser['userType'] != "Admin":
            print("How did you get this option???")
        if promotion_list == []:
            print("No promotions currently active\n")
        else:
            print(f"Current promotions:\n{'\n'.join(promotion for promotion in promotion_list)}\n")
        to_process = custom_lower(input("What do you want to do\n1. Add promotion\n2. Delete promotion\n0. Exit\n"))
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
                print(f"Current promotions:\n{'\n'.join(promotion for promotion in promotion_list_aux)}\n0. Exit\n")
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
        elif to_process == 'exit' or to_process == '0':
            print("Returning to options screen")
            break
        else:
            print("There are no such option")


def view_promotions():
    # For Guests and Travellers - allow them to see current promotions
    while True:
        promotion_list = open_promotions()
        if promotion_list == []:
            confirmation = input("Unfortunately, there are no available promotions at the moment\n0. Exit")
            if confirmation == 'exit' or confirmation == '0':
                print("Returning to options screen")
                break
        else:
            promotion_list_aux = custom_enumerate(promotion_list)
            confirmation = custom_lower(input(f"Current promotions:\n{'\n'.join(promotion for promotion in promotion_list_aux)}\n0. Exit\n"))
            if confirmation == 'exit' or confirmation == '0':
                print("Returning to options screen")
                break


def manage_booking(currentUser):
    # For Merchants and Travellers(Probably should have made 2 separate functions)
    # Travellers can see their booking from this menu and cancel any of them
    # Merchants can see their provided services and users, who booked them
    # Merchants also can cancel certain booking
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
                    confirmation = custom_lower(input("1. Cancel Booking\n0. Exit\n"))
                    if confirmation == 'exit' or confirmation == '0':
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


def plan_my_trip(currentUser):
    # For Travellers - Allow them to create and check their trip plan around KL, choosing from destinations in the system
    if currentUser['userType'] != 'Traveller':
        print("How did you get this option???")
    if currentUser['path'] == []:
        while True:
            confirmation = custom_lower(input("1. Create a plan for my trip\n0. Exit\n"))
            if confirmation == 'create a plan for my trip' or confirmation == '1':
                create_path(currentUser)
            elif confirmation == 'exit' or confirmation == '0':
                print("Returning to main menu")
                break
            else:
                print("There is no such option")
    else:
        while True:
            confirmation = custom_lower(input("1. Create a new plan for my trip\n2. Check existing plan\n0. Exit\n"))
            if confirmation == 'create a plan for my trip' or confirmation == '1':
                create_path(currentUser)
            elif confirmation == 'check existing plan' or confirmation == '2':
                plan_aux = custom_enumerate(currentUser['path'])
                while True:
                    confirmation = custom_lower(input(f"Your current lan for the trip:\n{'\n'.join(place for place in plan_aux)}\n0. Exit\n"))
                    if confirmation == 'exit' or confirmation == '0':
                        break
                    else:
                        print("There is no such option")
            elif confirmation == 'exit' or confirmation == '0':
                print("Returning to main menu")
                break
            else:
                print("There is no such option")


def create_path(currentUser):
    # Auxiliary function to create a new trip plan
    backup_path = currentUser['path'].copy()
    currentUser['path'] = []
    userData = open_userdata()
    destination_list = get_destination_list()
    left_destination_list = destination_list.copy()
    lower_destination_list = custom_lower_list(destination_list)
    left_lower_destination_list = custom_lower_list(destination_list)
    while True:
        destination_list_tmp = currentUser['path']
        destination_list_tmp_aux = custom_enumerate(destination_list_tmp)
        left_destination_list_aux = custom_enumerate(left_destination_list)
        print(f"Your current path:\n{'\n'.join(place for place in destination_list_tmp_aux)}")
        if currentUser['path'] == []:
            confirmation = custom_lower(input(f"{'-'*20}\n{'\n'.join(place for place in left_destination_list_aux)}\n0. Exit\nWhich place do you want to visit first?\n"))
        else:
            confirmation = custom_lower(input(f"{'-'*20}\n{'\n'.join(place for place in left_destination_list_aux)}\n-1. Exit\n0. Save and Exit\nWhich place do you want to visit next?\n"))
        alternative = [str(index+1) for index in range(len(left_destination_list_aux))]
        if confirmation in left_lower_destination_list:
            left_index = find_index(left_lower_destination_list, confirmation)
            index = find_index(lower_destination_list, confirmation)
            currentUser['path'].append(destination_list[index])
            del left_lower_destination_list[left_index]
            del left_destination_list[left_index]
        elif confirmation in alternative:
            left_index = int(confirmation) - 1
            index = find_index(lower_destination_list, left_lower_destination_list[left_index])
            currentUser['path'].append(destination_list[index])
            del left_lower_destination_list[left_index]
            del left_destination_list[left_index]
        elif confirmation == 'exit' or confirmation == '0':
            confirmation = custom_lower(input("Are you sure you want to discard changes and exit?\n1. Yes\n2. No\n"))
            if confirmation == 'yes' or confirmation == '1':
                print("Returning to planning screen")
                currentUser['path'] = backup_path
                break
            elif confirmation == 'no' or confirmation == '2':
                print("Discarding changes cancelled")
            else:
                print("There is no such option")
        elif confirmation == 'save and exit' or confirmation == '-1':
            confirmation = custom_lower(input("Are you sure you want to save changes and exit?\n1. Yes\n2. No\n"))
            if confirmation == 'yes' or confirmation == '1':
                print("New plan set successfully")
                break
            elif confirmation == 'no' or confirmation == '2':
                print("Saving cancelled")
            else:
                print("There is no such option")
        else:
            print("There is no such option")
    login_list = get_login_list()
    index = find_index(login_list, currentUser['login'])
    userData[index]['path'] = currentUser['path']
    save_userdata(userData)


def main():
    currentUser = assign_guest()
    interact_with_options(currentUser)


main()
