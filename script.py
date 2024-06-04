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


def assign_guest():
    currentUser = {
        "userType": "Guest",
        "login": None,
        "password": None,
        "active": True
    }
    return currentUser


def show_options(currentUser):
    options = []
    if currentUser['userType'] == 'Admin':
        options = ['Log in', 'Log out(in development)', 'Block Account(in development)', 'Unblock Account(in development)', 'Delete Account', 'Update promotion(in development)', 'Provide trip recommendation(in development)']
    elif currentUser['userType'] == 'Service':
        options = ['Log in', 'Log out(in development)', 'Manage Services(in development)', 'Manage Booking(in development)']
    elif currentUser['userType'] == 'Traveller':
        options = ['Log in', 'Log out(in development)', 'Explore Services(in development)', 'Explore Destinations(in development)', 'View recommended(in development)', 'Check availability(in development)']
    elif currentUser['userType'] == 'Guest':
        options = ['Log in', 'Sign up', 'Explore Services(in development)', 'Explore Destinations(in development)', 'View recommended(in development)', 'Check availability(in development)']
    options.append("Exit")
    # options = custom_lower(options)
    return options


def function_call(index, currentUser):
    if index == 0:
        currentUser = log_in_account(currentUser)
        return 1, currentUser
    elif index == 1:
        create_account(currentUser)
        confirmation = custom_lower(input("Would you like to stay signed in this account? Yes/No\n"))
        if confirmation == "yes" or confirmation == "1":
            userData = open_userdata()
            currentUser = userData[-1]
        return 1, currentUser
    elif index == 2:
        pass
    elif index == 3:
        pass
    elif index == 4:
        pass
    elif index == 5:
        delete_account(currentUser)
        login_list = get_login_list()
        if currentUser['login'] not in login_list:
            currentUser = assign_guest()
        return "1", currentUser
    elif index == 6:
        return "0", currentUser
    else:
        print("There are no such option available")
        return 1, currentUser


def interact_with_options(currentUser):
    full_options = ['log in', 'sign up', 'search', 'block user', 'unblock user', 'delete account', 'exit']
    while True:
        print(f"You are currently logged as {currentUser['userType']}\n"
              f"With your current access rights, you have access to: ")
        options = show_options(currentUser)
        alternative = [(index+1) for index in range(len(options))]
        print('\n'.join(option for option in options))
        choice = custom_lower(input("What would you like to do?\n"))
        for i in range(len(options)):
            options[i] = custom_lower(options[i])
        if choice in options:
            index = find_index(full_options, choice)
            check, currentUser = function_call(index, currentUser)
        elif int(choice) in alternative:
            index = find_index(full_options, options[int(choice)-1])
            check, currentUser = function_call(index, currentUser)
        else:
            print("There are no such option")
        if check == "0":
            break


def create_account(currentUser):
    userData = open_userdata()
    newUser = {'userType': 'default'}

    while newUser['userType'] == 'default':
        userType = custom_lower(input("Please, enter which account you want to create: Admin, Service or Traveller\n"
                                      "Be aware that only Admins are allowed to create additional Admin accounts\n"))
        if (userType == 'admin' or userType == '1') and currentUser['userType'] == 'Admin':
            newUser['userType'] = userType
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
    login_list = [userData[i]['login'] for i in range(len(userData))]
    return login_list


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


def block_user(currentUser):
    pass


def unblock_user(currentUser):
    pass


def main():
    currentUser = assign_guest()
    # tmp = get_login_list()
    # print(tmp)
    interact_with_options(currentUser)


main()

# data = open_userdata()
# print(*data, sep='\n')
