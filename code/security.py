# Importing our safe string method and the user class that
# we created in user.py we can import directly as the files
# are in the same folder
from werkzeug.security import safe_str_cmp
from models.user import UserModel

# Identifying the user by comparing the username and
# password they enter to the user in the database
# (using the User class method)
# Returing the user, fed to JWT to make the token
def authenticate(username, password):
    user = UserModel.find_by_username(username)
    if user and safe_str_cmp(user.password, password):
        return user


# Used when requesting an end point where authentication needed
# Payload comes from request, contains user id, search in the database
# (using the User class method)
# If match then we know user is authenticated
def identity(payload):
    user_id = payload['identity']
    return UserModel.find_by_id(user_id)
