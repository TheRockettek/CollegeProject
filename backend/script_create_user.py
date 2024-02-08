""" Script to create a new user in the database. """

from getpass import getpass

from queries import create_user


def main():
    username = input("Enter username: ")
    password = getpass("Enter password: ")
    name = input("Enter name: ")
    role = input("Enter role (editor/viewer/restricted): ")

    # Validate inputs
    if not username or not password or not name or not role:
        print("Error: All fields are required.")
        return

    # Validate role
    valid_roles = ["editor", "viewer", "restricted"]
    if role.lower() not in valid_roles:
        print("Error: Invalid role. Please enter 'editor', 'viewer', or 'restricted'.")
        return

    # Call create_user from the queries module
    create_user(username=username, plain_password=password, name=name, role=role)

    print(f"User {username} created successfully.")


if __name__ == "__main__":
    main()
