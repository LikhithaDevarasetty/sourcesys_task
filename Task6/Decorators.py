def login_required(func):
    def wrapper(user):
        if user.get("is_logged_in"):
            return func(user)
        else:
            print("Access Denied. Please login.")
    return wrapper

@login_required
def view_dashboard(user):
    print(f"Welcome {user['name']} to dashboard")

user1 = {"name": "Likhitha", "is_logged_in": True}
user2 = {"name": "Namitha", "is_logged_in": False}

view_dashboard(user1)
view_dashboard(user2)