import random
import sqlite3

conn = sqlite3.connect('password.db')
cur = conn.cursor()
cur.execute(
    "CREATE TABLE IF NOT EXISTS password_holder(pass_key TEXT PRIMARY KEY NOT NULL, service_name TEXT NOT NULL)")
conn.commit()


# Randomly generate a password of a given length.
# Generated password contains a combination of characters from 'characters' of the given length.
def generate_password():
    characters = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*"
    length_of_pass = input("Password length? ")
    length_of_pass = int(length_of_pass)

    # Initialize an empty string named 'password'. Generated password will be stored in this string.
    password = ""
    for item in range(length_of_pass):
        password += random.choice(characters)

    return password


def add_password(password, service):
    cur.execute("INSERT INTO password_holder VALUES(?, ?)", (password, service))
    conn.commit()


def show_password(service):
    cur.execute("SELECT * FROM password_holder WHERE service_name=?", (service,))
    get_pass = cur.fetchall()
    return get_pass


def show_database():
    cur.execute("SELECT * FROM password_holder")
    get_all = cur.fetchall()
    return get_all


def delete_password(service):
    cur.execute("DELETE FROM password_holder WHERE service_name=?", (service,))
    conn.commit()


def main():
    # It is the master password to log in to the database and access other passwords.
    # It is just a sample password. Should change it for actual use.
    ADMIN_PASSWORD = "123"

    connect = input("Enter password to generate password! ")
    while connect != ADMIN_PASSWORD:
        connect = input("Wrong one, try again...")
        if connect == 'q':
            break

    if (connect == ADMIN_PASSWORD):
        while True:
            print("\n")
            print("PASSWORD MANAGER")
            print("******************************************")
            print(">> Type q to quit.")
            print(">> Type m to generate a new password.")
            print(">> Type d to delete an old password.")
            print(">> Type s to show password.")
            print(">> Type all to show the entire database.")
            print("******************************************")
            print("\n")

            inpt = input("Enter command: ")

            if inpt == 'q':
                break

            elif inpt == 'm':
                service = input("What is the name of your service?\n")
                print("Manually enter the password or randomly generate password?\n")
                print("---> Type 1 for manual input\n")
                print("---> Type 2 to randomly generate\n")

                choice = input("What is your choice? ")
                if (choice == '1'):
                    password = input("Input password: ")
                    add_password(password, service)
                elif (choice == '2'):
                    password = generate_password()
                    add_password(password, service)

            elif inpt == 'd':
                service = input("What is the name of your service?\n")
                delete_password(service)
                print("Password deleted for " + service)

            elif inpt == 's':
                try:
                    service = input("What is the name of your service?\n")
                    print("Password for " + service + " is:  " + show_password(service)[0][0])
                except:
                    print("Most probably you've deleted the password for this service!")

            elif inpt == 'all':
                # print(show_database())
                data_list = show_database()
                if len(data_list) == 0:
                    print("Database is empty.")
                else:
                    for i in range(len(data_list)):
                        print("Service Name: " + data_list[i][1] + " --- " + "Password: " + data_list[i][0])

            else:
                print("What did you mean?")
                pass

    conn.close()


if __name__ == "__main__":
    main()