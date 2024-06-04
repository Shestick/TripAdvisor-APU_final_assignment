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
    if currentUser['userType'] == 'Admin':
        options = 'Option1A\nOption2A\nOption3A'
    elif currentUser['userType'] == 'Service':
        options = 'Option1S\nOption2S\nOption3S'
    elif currentUser['userType'] == 'Traveller':
        options = 'Option1T\nOption2T\nOption3T'
    elif currentUser['userType'] == 'Guest':
        options = 'Log in\nSign up\nSearch'
    options += "\nExit"
    print(options)


def interact_with_options(currentUser):
    while True:
        print(f"You are currently logged as {currentUser['userType']}\n"
              f"With your current access rights, you have access to: ")
        show_options(currentUser)
        choice = custom_lower(input("What would you like to do?\n"))
        if choice == "log in" or choice == "1":
            currentUser = log_in_account(currentUser)
        elif choice == "sign up" or choice == "2":
            create_account(currentUser)
            confirmation = custom_lower(input("Would you like to stay signed in this account? Yes/No\n"))
            if confirmation == "yes" or confirmation == "1":
                userData = open_userdata()
                currentUser = userData[-1]
            else:
                pass
        elif choice == "delete Account" or choice == "3":
            delete_account(currentUser)
            userData = open_userdata()
            login_list = get_login_list()
            if currentUser['login'] not in login_list:
                currentUser = assign_guest()
        elif choice == "exit" or choice == "4":
            break


def create_account(currentUser):
    userData = open_userdata()
    newUser = {'userType': 'default'}

    while newUser['userType'] == 'default':
        userType = custom_lower(input("Please, enter which account you want to create: Admin, Service or Traveller\n"
                                      "Be aware that only Admins are allowed to create additional Admin accounts\n"))
        if userType == 'admin' and currentUser['userType'] == 'Admin':
            newUser['userType'] = userType
        elif userType == 'admin' and currentUser['userType'] != 'Admin':
            print("You have insufficient access rights")
        elif userType == 'service' or userType == 'Traveller':
            newUser['userType'] = userType
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
        user_to_delete = input("Write, which user you want to delete")
        if user_to_delete in login_list:
            confirmation = custom_lower(input(f"Are you sure you want to delete user {user_to_delete}? Yes/No\n"))
            if custom_lower(confirmation) == 'yes':
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
        if custom_lower(confirmation) == 'yes':
            index = find_index(login_list, user_to_delete)
            del userData[index]
            save_userdata(userData)
            print(f'User {user_to_delete} successfully deleted')


def block_account(currentUser):
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
