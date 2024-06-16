import json


# Segment for emulation banned inbuilt function


def custom_len(list_to_count):
    length = 0
    for item in list_to_count:
        length += 1
    return length


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
    # Returns list of services, provided by a current user
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
    # This is the main cycle of the system, essentially the main menu.
    # Handles showing options based on User Type, reading input from the main menu, and terminating the program.
    # 'full_options' contains all possible options to allow input as both digits and characters.
    full_options = ['log in', 'sign up', 'block user', 'unblock user', 'delete account', 'log out', '#exit#',
                    'manage services', 'explore services', 'explore destinations', 'provide trip recommendation',
                    'view recommended', 'update promotions', 'view promotions', 'manage booking', 'plan my trip']

    while True:
        # Display the current user type and their available options.
        print(f"\n\nYou are currently logged as {currentUser['userType']}\n"
              f"With your current access rights, you have access to: ")

        # Get and display the options available to the current user.
        options_to_show = show_options(currentUser)
        options_to_process = custom_lower_list(options_to_show)
        alternative = [str(index + 1) for index in range(custom_len(options_to_show))]
        options_to_show_aux = custom_enumerate(options_to_show)

        # Print options with enumerated list and an 'Exit' option.
        print(f"{'\n'.join(option for option in options_to_show_aux)}\n0. Exit")

        # Get the user's choice and process it.
        choice = custom_lower(input("What would you like to do?\n"))

        if choice == 'exit' or choice == '0':
            break  # Exit the loop if the choice is 'exit' or '0'.
        elif choice in options_to_process:
            # Find the index of the chosen option and call the corresponding function.
            index = find_index(full_options, choice)
            currentUser = function_call(index, currentUser)
        elif choice in alternative:
            # Find the index of the chosen numerical option and call the corresponding function.
            index = find_index(full_options, options_to_process[int(choice) - 1])
            currentUser = function_call(index, currentUser)
        else:
            print("There are no such option")  # Invalid option message


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
    # Function to create a new account based on user input
    # Only Admins can create other Admin accounts
    userData = open_userdata()
    newUser = {'userType': 'default'}

    # Loop to determine the type of account to create
    while newUser['userType'] == 'default':
        userType = custom_lower(
            input("Please, enter which account you want to create:\n1. Admin\n2. Service\n3. Traveller\n0. Exit\n"
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

    # Loop to set a unique login for the new account
    while True:
        login = input("Please, set your login: ")
        login_list = get_login_list()
        if login in login_list:
            print(f"User {login} already exists, choose another login")
        else:
            newUser['login'] = login
            break

    # Loop to set and confirm the password for the new account
    while True:
        password_set = input("Please, set your password: ")
        password_confirmation = input("Please, confirm your password: ")
        if password_set == password_confirmation:
            newUser['password'] = password_confirmation
            break
        else:
            print("Passwords do not match")

    # Set the account as active and initialize fields for Traveller accounts
    newUser['active'] = True
    if newUser['userType'] == 'Traveller':
        newUser['booking'] = []
        newUser['path'] = []

    userData.append(newUser)  # Add the new account to user data
    print("Account created successfully")

    # Prompt to stay signed in the new account
    confirmation = custom_lower(input("Would you like to stay signed in this account?\n1. Yes\n2. No\n"))
    if confirmation == "yes" or confirmation == "1":
        currentUser = userData[-1]
    elif confirmation == 'no' or confirmation == '2':
        print("Returning to main menu")

    save_userdata(userData)
    return currentUser


def log_in_account(currentUser):
    # Prompts user to log in by entering login and password, returning user profile if successful
    userData = open_userdata()
    login_list = get_login_list()

    while True:
        login_attempt = input("Enter your login:\n")
        if login_attempt == "0":  # Cancel login
            return currentUser

        if login_attempt in login_list:
            while True:
                password_attempt = input("Enter your password:\n")
                if password_attempt == "0":  # Cancel login
                    return currentUser

                # Check credentials
                for user in userData:
                    if user['login'] == login_attempt and user['password'] == password_attempt:
                        if user['active']:
                            print(f"Login successful. Welcome, {user['login']}!")
                            return user  # Return user profile if active
                        else:
                            print("Your account is inactive, please contact an Admin")
                            return currentUser  # Return current user if account is inactive

                print("Your password is wrong, try again or type 0 to cancel")
        else:
            print("There are no such user, try again or type 0 to cancel")


def log_out(currentUser):
    # Prompts user to confirm log out, reassigns guest profile if confirmed
    while True:
        confirmation = custom_lower(input("Are you sure you want to log out?\n1. Yes\n2. No\n"))

        if confirmation == "yes" or confirmation == "1":
            currentUser = assign_guest()  # Reassign guest profile
            return currentUser

        elif confirmation == 'no' or confirmation == '2':
            print("Log out cancelled")
            return currentUser

        else:
            print("There is no such option")


def block_account(currentUser):
    # Admin-exclusive function to block a user, removing their services and bookings
    while True:
        if currentUser['userType'] != 'Admin':
            print("How did you get this option???")

        active_users = get_active_login_list()
        blocked_users = get_blocked_login_list()

        print(f"Currently active users:\n{'\n'.join(user for user in active_users)}\n0. Exit\n")
        user_to_block = input("Which user do you want to block?\n")

        if user_to_block == "exit" or user_to_block == '0':  # Exit option
            break

        elif user_to_block in active_users and user_to_block != currentUser['login']:
            # Confirm and proceed to block the selected user
            confirmation = custom_lower(input(f"Are you sure you want to block user {user_to_block}?\n1. Yes\n2. No\n"))
            if confirmation == 'yes' or confirmation == '1':
                login_list = get_login_list()
                index = find_index(login_list, user_to_block)
                userData = open_userdata()
                userData[index]['active'] = False
                cancel_users_booking(userData[index])  # Cancel user's services and bookings
                save_userdata(userData)
                print(f"User {user_to_block} successfully blocked")
            elif confirmation == 'no' or confirmation == '2':
                print("User blocking cancelled")

        elif user_to_block in active_users and user_to_block == currentUser['login']:
            print("You cannot block yourself")

        elif user_to_block in blocked_users:
            print(f"User {user_to_block} is already blocked")

        else:
            print(f"User {user_to_block} not found")

        # Check if admin wants to continue blocking users
        tmp = input("Do you wish to continue blocking?\n1. Yes\n2. No\n")
        if custom_lower(tmp) == 'no' or tmp == '2':
            break


def unblock_account(currentUser):
    # Admin-exclusive function to unblock a user, allowing them to use the system again
    while True:
        if currentUser['userType'] != 'Admin':
            print("How did you get this option???")

        active_users = get_active_login_list()
        blocked_users = get_blocked_login_list()

        if not blocked_users:
            print("There are no currently blocked users")
            break

        print(f"Currently blocked users:\n{'\n'.join(user for user in blocked_users)}\n0. Exit\n")
        user_to_unblock = input("Which user do you want to unblock?\n")

        if user_to_unblock == "0" or user_to_unblock == 'exit':  # Exit option
            break

        elif user_to_unblock in blocked_users:
            # Confirm and proceed to unblock the selected user
            confirmation = custom_lower(
                input(f"Are you sure you want to unblock user {user_to_unblock}?\n1. Yes\n2. No\n"))
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

        # Check if admin wants to continue unblocking users
        tmp = input("Do you wish to continue unblocking?\n1. Yes\n2. No\n")
        if custom_lower(tmp) == 'no' or tmp == '2':
            break


def delete_account(currentUser):
    # Allows Admin to delete any user except himself; others can delete their own accounts
    userData = open_userdata()
    login_list = get_login_list()
    login_list_aux = custom_enumerate(login_list)

    # Mark blocked users in the displayed list
    for user in login_list:
        index_tmp = find_index(login_list, user)
        if not userData[index_tmp]['active']:
            login_list_aux[index_tmp] += ' (blocked)'

    if currentUser['userType'] == 'Admin':
        print(f"User list:\n{'\n'.join(user for user in login_list_aux)}\n0. Exit\n")
        user_to_delete = input("Write which user you want to delete\n")
        alternative = [str(index + 1) for index in range(custom_len(login_list))]

        if user_to_delete == 'exit' or user_to_delete == '0':
            print("Returning to main menu")
            return currentUser

        # Direct user selection by login
        elif user_to_delete in login_list:
            confirmation = custom_lower(
                input(f"Are you sure you want to delete user {user_to_delete}?\n1. Yes\n2. No\n"))
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

        # User selection by index
        elif user_to_delete in alternative:
            confirmation = custom_lower(
                input(f"Are you sure you want to delete user {login_list[int(user_to_delete) - 1]}?\n1. Yes\n2. No\n"))
            if confirmation == 'yes' or confirmation == '1':
                index = int(user_to_delete) - 1
                cancel_users_booking(userData[index])
                del userData[index]
                save_userdata(userData)
                print(f'User {login_list[int(user_to_delete) - 1]} successfully deleted')
            elif confirmation == 'no' or confirmation == '2':
                print("Deletion cancelled")
            else:
                print("There is no such option")

        else:
            print(f"User {user_to_delete} not found")
        return currentUser

    # Non-admin users deleting their own account
    else:
        user_to_delete = currentUser["login"]
        confirmation = custom_lower(
            input(f"Are you sure you want to delete your account {user_to_delete}?\n1. Yes\n2. No\n"))
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
    # Auxiliary function to delete a user's booking information from the database

    # Open service data and user data
    serviceData = open_service_data()
    userData = open_userdata()

    # Clear the user's booking list
    user['booking'] = []

    # Iterate through all services
    for service in serviceData:
        # Check if the user has any bookings in the current service
        if user['login'] in service['booking']:
            # Find and remove the user's booking
            index = find_index(service['booking'], user['login'])
            del service['booking'][index]

    # Save the updated service data and user data
    save_service_data(serviceData)
    save_userdata(userData)


def manage_services(currentUser):
    # Merchant-exclusive function for managing services.
    # Provides a submenu to add, update, or delete services.

    while True:
        if currentUser['userType'] != "Service":
            print("How did you get this option???")

        # Retrieve the list of services provided by the current user
        service_list = get_user_service_list(currentUser)

        # Display appropriate options based on whether the user has any services
        if service_list == []:
            to_process = input("What would you like to do?\n1. Add Service\n0. Exit\n")
        else:
            # Enumerate the user's services and display them
            service_list_aux = custom_enumerate(service_list)
            print(f"You are currently providing:\n{'\n'.join(service for service in service_list_aux)}\n")
            to_process = input(
                "What would you like to do?\n1. Add Service\n2. Update Services\n3. Delete Service\n0. Exit\n")

        # Process the user's choice
        if custom_lower(to_process) == "exit" or to_process == '0':
            break
        elif custom_lower(to_process) == "add service" or to_process == '1':
            add_service(currentUser)
        elif custom_lower(to_process) == "update service" or to_process == '2':
            update_service(currentUser)
        elif custom_lower(to_process) == "delete service" or to_process == '3':
            delete_service(currentUser)


def add_service(currentUser):
    # Creating a new service based on user input, guiding the user through the process.
    # Services can be linked to an existing destination for easier planning.

    new_service = {}

    while True:
        # Retrieve the list of existing services to check for name uniqueness
        service_list = get_service_list()
        service_name = input("Enter the service's name\n")

        # Ensure the service name is unique
        if service_name in service_list:
            print(f"Service {service_name} already exists, choose another name")
        else:
            new_service['serviceName'] = service_name
            break

    # Assign the current user's login as the host of the service
    new_service['userHost'] = currentUser['login']

    # Ask if the user wants to associate the service with a specific location
    confirmation = custom_lower(input("Do you want to associate your service with a location?\n1. Yes\n2. No\n"))

    if confirmation == 'yes' or confirmation == '1':
        # Retrieve and display the list of available destinations
        destination_list = get_destination_list()
        lower_destination_list = custom_lower_list(destination_list)

        while True:
            location_to_associate = custom_lower(input(
                f"Currently available destinations:\n{'\n'.join(destination for destination in destination_list)}\n0. Exit\n"))

            # Allow the user to exit without choosing a location
            if location_to_associate == 'exit' or location_to_associate == '0':
                new_service["placing"] = 'Not mentioned'
                break
            elif location_to_associate in lower_destination_list:
                inside_index = find_index(lower_destination_list, location_to_associate)
                new_service["placing"] = destination_list[inside_index]
                break
            else:
                print("There is no such location")
    else:
        new_service["placing"] = 'Not mentioned'

    # Prompt the user to enter additional details about the service
    new_service['quantity'] = input("Enter the provided quantity of your service\n")
    new_service['price'] = input("Enter the price of your service\n")

    # Ask for the service start date or if it is continuous
    start_date = input("Enter your service start date as 'Day Month' or 'Continuous' if your service is not expiring\n")

    if custom_lower(start_date) != 'continuous':
        end_date = input("Enter your service end date as 'Day Month'\n")
        schedule = f"From {start_date} to {end_date}"
    else:
        schedule = 'Continuous'

    new_service['schedule'] = schedule
    new_service['booking'] = []

    # Display the new service details for confirmation
    print(f"Service name: {new_service['serviceName']}\n"
          f"Hosted by: {new_service['userHost']}\n"
          f"Location: {new_service['placing']}\n"
          f"Provided quantity: {new_service['quantity']}\n"
          f"Price: {new_service['price']}\n"
          f"Schedule: {new_service['schedule']}\n")

    # Ask the user if they wish to save the new service
    confirmation = input("Do you wish to save the current service? Yes/No\n")

    if custom_lower(confirmation) == 'yes' or confirmation == '1':
        # Save the new service to the service data
        serviceData = open_service_data()
        serviceData.append(new_service)
        save_service_data(serviceData)

        # If the service is linked to a location, update the destination data
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

    while True:
        # Fetch user's service list and global service list
        service_list = get_user_service_list(currentUser)
        glob_service_list = get_service_list()
        service_list_aux = custom_enumerate(service_list)

        # Display user's services for update selection
        print(f"You are currently providing:\n{'\n'.join(service for service in service_list_aux)}\n0. Exit")
        to_process = custom_lower(input("Which of your services you would like to update?\n"))
        alternative = [str(index + 1) for index in range(custom_len(service_list))]

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
            # Fetch destination and service data
            destinationData = open_destination_data()
            destination_list = get_destination_list()
            serviceData = open_service_data()

            # Check if service's placing is mentioned and get destination-bound service index
            if serviceData[glob_index]['placing'] != 'Not mentioned':
                destination_index_1 = find_index(destination_list, serviceData[glob_index]['placing'])
                existence_index = find_index(destinationData[destination_index_1]['amenities'][0], serviceData[glob_index]['serviceName'])
            else:
                destination_index_1 = -1

            # Display service details for update selection
            print(f"1. Service name: {serviceData[glob_index]['serviceName']}\n"
                  f"2. Hosted by: {serviceData[glob_index]['userHost']}\n"
                  f"3. Location: {serviceData[glob_index]['placing']}\n"
                  f"4. Provided quantity: {serviceData[glob_index]['quantity']}\n"
                  f"5. Price: {serviceData[glob_index]['price']}\n"
                  f"6. Schedule: {serviceData[glob_index]['schedule']}\n"
                  f"0. Exit")
            to_update = custom_lower(input("Which part you would like to update?\n"))

            if to_update == 'service name' or to_update == 'name' or to_update == '1':
                # Update service name
                while True:
                    service_list = get_service_list()
                    new_name = input(f"Current Service name: {serviceData[glob_index]['serviceName']}\n"
                                     f"New Service name: ")
                    if new_name in service_list:
                        print(f"Service {new_name} already exists, choose another name")
                    else:
                        serviceData[glob_index]['serviceName'] = new_name
                        break
                save_service_data(serviceData)
                if destination_index_1 != -1:
                    destinationData[destination_index_1]['amenities'][0][existence_index] = new_name
                save_destination_data(destinationData)
                print("Service update successful")

            # Other update options for service details
            elif to_update == 'hosted by' or to_update == '2':
                print("You cannot update this")
            elif to_update == 'location' or to_update == '3':
                # Update service location
                destination_list = get_destination_list()
                destination_list.append('Not mentioned')
                new_location = input(f"Current Location: {serviceData[glob_index]['placing']}\n"
                                     f"Available locations:\n{'\n'.join(destination for destination in destination_list)}\n"
                                     f"New Location: ")
                if custom_lower(new_location) == 'not mentioned':
                    new_location = 'Not mentioned'

                # Check if the new location is valid and update accordingly
                if custom_lower(new_location) in custom_lower_list(destination_list):
                    # Update location in service data
                    serviceData[glob_index]['placing'] = new_location
                    save_service_data(serviceData)

                    # Handle data consistency with destination data
                    if custom_lower(new_location) != 'not mentioned':
                        destination_index_2 = find_index(destination_list, serviceData[glob_index]['placing'])
                    else:
                        destination_index_2 = -1
                    if destination_index_1 != destination_index_2 and destination_index_2 != -1:
                        # Update destination-bound service in new location
                        destinationData[destination_index_2]['amenities'][0].append(
                            serviceData[glob_index]['serviceName'])
                        destinationData[destination_index_2]['amenities'][1].append(serviceData[glob_index]['schedule'])
                        if destination_index_1 != -1:
                            # Remove service from old location if it existed there
                            del destinationData[destination_index_1]['amenities'][0][existence_index]
                            del destinationData[destination_index_1]['amenities'][1][existence_index]
                    else:
                        # Remove service from old location if it moved to 'Not mentioned'
                        del destinationData[destination_index_2]['amenities'][0][existence_index]
                        del destinationData[destination_index_2]['amenities'][1][existence_index]
                    save_destination_data(destinationData)
                    print("Service update successful")
                else:
                    print("There is no such location available")

            # Similar update logic for other service details
            elif to_update == 'provided quantity' or to_update == 'quantity' or to_update == '4':
                new_quantity = input(f"Current Quantity: {serviceData[glob_index]['quantity']}\n"
                                     f"New Quantity: ")
                serviceData[glob_index]['quantity'] = new_quantity
                save_service_data(serviceData)
                print("Service update successful")
            elif to_update == 'price' or to_update == '5':
                new_price = input(f"Current Price: {serviceData[glob_index]['price']}\n"
                                  f"New Price: ")
                serviceData[glob_index]['price'] = new_price
                save_service_data(serviceData)
                print("Service update successful")
            elif to_update == 'schedule' or to_update == '6':
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

            elif to_update == 'exit' or to_update == '0':
                print("Returning to service page...")
                break
            else:
                print("This is not a valid option")


def delete_service(currentUser):
    # Deletes service and all the booking associated with it
    while True:
        # Fetch user's service list and global service list
        service_list = get_user_service_list(currentUser)
        glob_service_list = get_service_list()
        service_list_aux = custom_enumerate(service_list)

        # Display user's services for deletion selection
        print(f"You are currently providing:\n{'\n'.join(service for service in service_list_aux)}\n0. Exit\n")
        to_process = custom_lower(input("Which of your services you would like to delete?\n"))
        alternative = [str(index + 1) for index in range(custom_len(service_list))]

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
            # Confirm service deletion
            confirmation = custom_lower(input(f"Are you sure you want to delete service {service_list[index]}?\n1. Yes\n2. No\n"))

            if confirmation == "yes" or confirmation == '1':
                destinationData = open_destination_data()
                serviceData = open_service_data()
                destination_list = get_destination_list()
                userData = open_userdata()
                login_list = get_login_list()

                # Delete associated bookings
                for user in serviceData[glob_index]['booking']:
                    booking_index_1 = find_index(login_list, user)
                    booking_index_2 = find_index(userData[booking_index_1]['booking'], serviceData[glob_index]['serviceName'])
                    del userData[booking_index_1]['booking'][booking_index_2]

                # Delete service from destination data
                destination_index = find_index(destination_list, serviceData[glob_index]['placing'])
                existence_index = find_index(destinationData[destination_index]['amenities'][0], serviceData[glob_index]['serviceName'])
                del serviceData[glob_index]
                del destinationData[destination_index]['amenities'][0][existence_index]
                del destinationData[destination_index]['amenities'][1][existence_index]

                # Save updated data
                save_userdata(userData)
                save_service_data(serviceData)
                save_destination_data(destinationData)
                print(f"Service {glob_service_list[glob_index]} deleted successfully")
            else:
                print("Service deletion cancelling")


def explore_services(currentUser):
    # For Guests and Travellers - Allow them to see service list, then choose one of them to see additional info
    # Travellers can also make a booking from this menu as well as cancel already booked service

    # Open necessary data files
    serviceData = open_service_data()
    active_service_list = get_active_service_list()
    service_list = get_service_list()
    userData = open_userdata()
    login_list = get_login_list()
    user_data_index = find_index(login_list, currentUser['login'])

    while True:
        # Display available services for exploration
        service_list_aux = custom_enumerate(active_service_list)
        print(f"\nAvailable services:\n{'\n'.join(service for service in service_list_aux)}\n0. Exit\n")
        alternative = [str(index + 1) for index in range(custom_len(active_service_list))]
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
            # Display details of the selected service
            print(f"\nService name: {serviceData[index]['serviceName']}\n"
                  f"Hosted by: {serviceData[index]['userHost']}\n"
                  f"Location: {serviceData[index]['placing']}\n"
                  f"Provided quantity: {int(serviceData[index]['quantity']) - custom_len(serviceData[index]['booking'])}\n"
                  f"Price: {serviceData[index]['price']}\n"
                  f"Schedule: {serviceData[index]['schedule']}\n")

            # Handle booking options for Travellers
            if currentUser['userType'] == 'Traveller' and currentUser['login'] not in serviceData[index]['booking']:
                confirmation = custom_lower(input("1. Book\n0. Exit\n"))

                if confirmation == 'exit' or confirmation == '0':
                    break
                elif confirmation == 'book' or confirmation == '1':
                    availability = int(serviceData[index]['quantity']) - custom_len(serviceData[index]['booking'])

                    if availability == 0:
                        print("Sorry, there are no free spots left for booking")
                    else:
                        confirmation = custom_lower(input("Do you wish to book this service?\n1. Yes\n2. No\n"))

                        if confirmation == 'no' or confirmation == '2':
                            print("Booking process cancelled")
                        elif confirmation == 'yes' or confirmation == '1':
                            # Update booking data
                            serviceData[index]['booking'].append(currentUser['login'])
                            userData[user_data_index]["booking"].append(serviceData[index]['serviceName'])
                            save_service_data(serviceData)
                            save_userdata(userData)
                            print(f"{serviceData[index]['serviceName']} booked successfully")
                            break
                        else:
                            print("Invalid option")

            # Handle booking cancellation for Travellers
            elif currentUser['userType'] == 'Traveller' and currentUser['login'] in serviceData[index]['booking']:
                confirmation = custom_lower(input("1. Cancel Booking\n0. Exit\n"))

                if confirmation == 'exit' or confirmation == '0':
                    break
                elif confirmation == 'cancel booking' or confirmation == '1':
                    confirmation = custom_lower(input("Do you wish to cancel your booking?\n1. Yes\n2. No\n"))

                    if confirmation == 'no' or confirmation == '2':
                        print("Booking cancellation interrupted")
                    elif confirmation == 'yes' or confirmation == '1':
                        # Update booking data
                        booking_index = find_index(serviceData[index]['booking'], currentUser['login'])
                        del serviceData[index]['booking'][booking_index]
                        user_index = find_index(userData[user_data_index]['booking'], serviceData[index]['serviceName'])
                        del userData[user_data_index]["booking"][user_index]
                        save_service_data(serviceData)
                        save_userdata(userData)
                        print(f"Booking of {serviceData[index]['serviceName']} cancelled successfully")
                        break
                    else:
                        print("Invalid option")

            else:
                confirmation = custom_lower(input("0. Exit\n"))

                if confirmation == 'exit' or confirmation == '0':
                    break
                else:
                    print("Invalid option")

    currentUser = userData[user_data_index]
    return currentUser


def explore_destinations():
    # For Guests and Travellers - Allow them to see destinations list, then choose one of them to see additional info
    # Such as Points of interest nearby and associated services

    # Open necessary data files
    destinationData = open_destination_data()
    destination_list = get_destination_list()

    while True:
        # Display available destinations for exploration
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
            # Display details of the selected destination
            print(f"Title: {destinationData[index]['destinationName']}\n"
                  f"Points of interest: {', '.join(POI for POI in destinationData[index]['points of interest'])}")

            # Display amenities information
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
            else:
                print("Invalid option")


def manage_recommendation(currentUser):
    # For Admins - allow them to construct a recommendation for one of the existing destinations
    # There is a choice between default recommendation structure (auto filled) and custom, made by the user themselves

    # Open necessary data files
    destinationData = open_destination_data()
    destination_list = get_destination_list()

    while True:
        # Open current recommendation data
        recommendation = open_recommendation()

        # Check if user is Admin
        if currentUser['userType'] != "Admin":
            print("How did you get this option???")

        # Display available destinations for recommendation
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
            # Ask for default or custom recommendation structure
            confirmation = custom_lower(input("Do you wish to use the default structure?\n1. Yes\n2. No\n0. Exit\n"))

            if confirmation == 'yes' or confirmation == '1':
                # Update recommendation with default structure
                recommendation[0] = destinationData[index]['destinationName']
                recommendation[3] = recommendation[1]
                recommendation[4] = recommendation[2]
                save_recommendation(recommendation)
                break
            elif confirmation == 'no' or confirmation == '2':
                # Ask for custom recommendation parts
                recommendation[0] = destinationData[index]['destinationName']
                first_part = input(f"Custom structure: 'First part', '{destinationData[index]['destinationName']}', 'Second part'\n"
                                   f"Enter the first part:\n")
                second_part = input(f"{first_part} {destinationData[index]['destinationName']} 'Second part'\n"
                                    f"Enter the second part:\n")
                confirmation = custom_lower(input(f"{first_part} {destinationData[index]['destinationName']} {second_part}\n"
                                                  f"Are you satisfied with the result?\n1. Yes\n2. No\n"))

                if confirmation == 'yes' or confirmation == '1':
                    # Update recommendation with custom structure
                    recommendation[3] = first_part
                    recommendation[4] = second_part
                    save_recommendation(recommendation)
                    break
                elif confirmation == 'no' or confirmation == '2':
                    print("Recommendation update cancelled")
                else:
                    print("Invalid option")
            elif confirmation == 'exit' or confirmation == '0':
                break
            else:
                print("Invalid option")


def view_recommendation():
    # For Guests and Travellers - Allow them to see current recommendation

    while True:
        # Open current recommendation data
        recommendation = open_recommendation()

        # Display current recommendation
        confirmation = custom_lower(input(f"{recommendation[3]} {recommendation[0]} {recommendation[4]}\n0. Exit\n"))

        if confirmation == 'exit' or confirmation == '0':
            break
        else:
            print("Invalid option")


def manage_promotions(currentUser):
    # For Admins - allow them to add and delete promotions of services

    while True:
        # Open current promotions list
        promotion_list = open_promotions()

        if currentUser['userType'] != "Admin":
            print("How did you get this option???")

        # Display current promotions or inform about their absence
        if promotion_list == []:
            print("No promotions currently active\n")
        else:
            print(f"Current promotions:\n{'\n'.join(promotion for promotion in promotion_list)}\n")

        # Ask user what they want to do
        to_process = custom_lower(input("What do you want to do\n1. Add promotion\n2. Delete promotion\n0. Exit\n"))

        if to_process == 'yes' or to_process == '1':
            # Adding a new promotion
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
                    print("Invalid option\n")

        elif to_process == 'no' or to_process == '2':
            # Deleting a promotion
            while True:
                if promotion_list == []:
                    print("There are no promotions to delete")
                    break

                # Display current promotions for deletion
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
                        print("Invalid option")
                else:
                    print("Invalid option")

        elif to_process == 'exit' or to_process == '0':
            print("Returning to options screen")
            break
        else:
            print("Invalid option")


def view_promotions():
    # For Guests and Travellers - allow them to see current promotions

    while True:
        # Open current promotions list
        promotion_list = open_promotions()

        if promotion_list == []:
            # Inform about no available promotions
            confirmation = input("Unfortunately, there are no available promotions at the moment\n0. Exit")
            if confirmation == 'exit' or confirmation == '0':
                print("Returning to options screen")
                break
        else:
            # Display current promotions for viewing
            promotion_list_aux = custom_enumerate(promotion_list)
            confirmation = custom_lower(input(f"Current promotions:\n{'\n'.join(promotion for promotion in promotion_list_aux)}\n0. Exit\n"))
            if confirmation == 'exit' or confirmation == '0':
                print("Returning to options screen")
                break
            else:
                print("Invalid option")


def manage_booking(currentUser):
    # For Merchants and Travellers (Probably should have made 2 separate functions)
    # Travellers can see their booking from this menu and cancel any of them
    # Merchants can see their provided services and users who booked them
    # Merchants also can cancel certain bookings

    userData = open_userdata()
    serviceData = open_service_data()
    service_list = get_service_list()
    lower_service_list = custom_lower_list(service_list)
    login_list = get_login_list()
    user_data_index = find_index(login_list, currentUser['login'])

    if currentUser['userType'] == 'Traveller':
        # For Travellers

        while True:
            if currentUser['booking'] == []:
                confirmation = custom_lower(input("You don't have anything booked at this moment\n0. Exit\n"))
                if confirmation == 'exit' or confirmation == '0':
                    print("Returning to options screen")
                    break
            else:
                # Display the bookings of the traveller
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
                else:
                    print("There is no such option")
                    index = -1

                while index != -1:
                    # Show details of the selected booking
                    print(f"Service name: {serviceData[index]['serviceName']}\n"
                          f"Hosted by: {serviceData[index]['userHost']}\n"
                          f"Location: {serviceData[index]['placing']}\n"
                          f"Provided quantity: {int(serviceData[index]['quantity']) - len(serviceData[index]['booking'])}\n"
                          f"Price: {serviceData[index]['price']}\n"
                          f"Schedule: {serviceData[index]['schedule']}\n")

                    # Ask for confirmation to cancel the booking
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
        # For Merchants
        while True:
            # Check if the merchant provides any services
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
                # Display the services provided by the merchant
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
                    # Show the bookings for the selected service
                    booked_users_list = serviceData[index]['booking']
                    if booked_users_list == []:
                        print("This service has not got any bookings at this moment")
                        break
                    else:
                        booked_users_list_aux = custom_enumerate(booked_users_list)
                        lower_booked_users_list = custom_lower_list(booked_users_list)
                        print(f"Service name: {serviceData[index]['serviceName']}\n"
                              f"Booked by:\n{'\n'.join(user for user in booked_users_list_aux)}\n0. Exit\n")

                        # Ask the merchant which booking they want to cancel
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
                            # Confirm cancellation of the selected booking
                            confirmation = custom_lower(input(f"Are you sure you want to cancel following booking:\n"
                                                              f"Service: {serviceData[index]['serviceName']}\n"
                                                              f"User: {userData[booked_index]['login']}\n1. Yes\n2. No\n"))
                            if confirmation == 'no' or confirmation == '2':
                                print("Returning to booking screen")
                                break
                            elif confirmation == 'yes' or confirmation == '1':
                                # Cancel the booking
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

    # Check if the user has any existing trip plans
    if currentUser['path'] == []:
        while True:
            # User has no existing plan, offer to create a new plan or exit
            confirmation = custom_lower(input("1. Create a plan for my trip\n0. Exit\n"))
            if confirmation == 'create a plan for my trip' or confirmation == '1':
                create_path(currentUser)  # Call the function to create a trip plan
            elif confirmation == 'exit' or confirmation == '0':
                print("Returning to main menu")
                break
            else:
                print("There is no such option")
    else:
        while True:
            # User has an existing plan, offer options to create a new plan, check the existing plan, or exit
            confirmation = custom_lower(input("1. Create a new plan for my trip\n2. Check existing plan\n0. Exit\n"))
            if confirmation == 'create a plan for my trip' or confirmation == '1':
                create_path(currentUser)  # Call the function to create a new trip plan
            elif confirmation == 'check existing plan' or confirmation == '2':
                # Display the current trip plan and offer to exit
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
    # Backup the user's current path before modifications
    backup_path = currentUser['path'].copy()
    # Reset the current path for creating a new plan
    currentUser['path'] = []
    userData = open_userdata()
    destination_list = get_destination_list()
    left_destination_list = destination_list.copy()
    lower_destination_list = custom_lower_list(destination_list)
    left_lower_destination_list = custom_lower_list(destination_list)

    # Main loop for creating the trip plan
    while True:
        destination_list_tmp = currentUser['path']
        destination_list_tmp_aux = custom_enumerate(destination_list_tmp)
        left_destination_list_aux = custom_enumerate(left_destination_list)
        print(f"Your current path:\n{'\n'.join(place for place in destination_list_tmp_aux)}")

        # Prompt the user to choose a destination
        if currentUser['path'] == []:
            confirmation = custom_lower(input(f"{'-'*20}\n{'\n'.join(place for place in left_destination_list_aux)}\n0. Exit\nWhich place do you want to visit first?\n"))
        else:
            confirmation = custom_lower(input(f"{'-'*20}\n{'\n'.join(place for place in left_destination_list_aux)}\n0. Exit\n-1. Save and Exit\nWhich place do you want to visit next?\n"))

        alternative = [str(index+1) for index in range(len(left_destination_list_aux))]

        # Process user input for destination selection
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
                # Restore the original path
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
