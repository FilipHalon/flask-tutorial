from user import User

# users = [
#     {"id": 1, "username": "admin", "password": "admin"},
#     {"id": 2, "username": "Mihu", "password": "password"},
# ]

users = [User(1, "admin", "admin"), User(2, "user", "password")]

# tworząc w ten sposób 2 słowniki pomocnicze nie będziemy musieli iterować po całej liscie użytkowników

# username_mapping = {
#     "admin": {"id": 1, "username": "admin", "password": "admin"},
#     "Mihu": {"id": 2, "username": "Mihu", "password": "password"},
# }

username_mapping = {user.username: user for user in users}

# userid_mapping = {
#     1: {"id": 1, "username": "admin", "password": "admin"},
#     2: {"id": 2, "username": "Mihu", "password": "password"},
# }

userid_mapping = {user.id: user for user in users}


# def authenticate(username, password):
#     user = username_mapping.get(username, None)
#     if user and user.password == password:
#         return user


def authenticate(username, password):
    user = User.find_by_username(username)
    if user and user.password == password:
        return user


# funkcja JWT, która pozwala nam dopasować odpowiedni token do odpowiedniego użytkownika
# def identity(payload):
#     user_id = payload["identity"]
#     return userid_mapping.get(user_id, None)


def identity(payload):
    user_id = payload["identity"]
    return User.find_by_username(user_id)
