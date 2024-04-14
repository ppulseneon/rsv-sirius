users = []

def add_user(user):
    if user in users:
        return False
    users.append(user)
    return True

def find_user(id):
    for user in users:
        if user.id == id:
            return user
    return None

def edit_status(id, status):
    for user in users:
        if user.id == id:
            user.action = status

def set_token(id, token):
    for user in users:
        if user.id == id:
            user.token = token

def set_coords(id, latitude, longitude):
    for user in users:
        if user.id == id:
            user.latitude = latitude
            user.longitude = longitude