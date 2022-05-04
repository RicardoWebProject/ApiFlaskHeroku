from models.user import UserModel

# users = [
#     User(1, 'ricardo', 1234)
# ]

# username_mapping = {u.username: u for u in users}

# userid_mapping = {u.id: u for u in users}

# users = [
#     {
#         'id': 1,
#         'username': 'ricardo',
#         'password': 1234
#     }
# ]

# username_mapping = {
#     'ricardo': {
#         'id': 1,
#         'username': 'ricado',
#         'password': 1234
#     }
# }

# userid_mapping = {
#     1: {
#         'id': 1,
#         'username': 'ricado',
#         'password': 1234
#     }
# }

def authenticate(username, password):
    # user = username_mapping.get(username, None)
    user = UserModel.find_by_username(username)
    if user and user.password == password:
        return user

def identity(payload):
    user_id = payload['identity']
    # return userid_mapping.get(user_id, None)
    return UserModel.find_by_id(user_id)