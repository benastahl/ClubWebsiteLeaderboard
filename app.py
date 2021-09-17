from flask import Flask
from flask import render_template
import jyserver.Flask as Server
import json

app = Flask(__name__)


def writer(data, filename):
    with open(filename, "w") as f:
        json.dump(data, f, indent=2)


def user_data():
    with open("user_info.json", "r") as user_info_raw:
        user_info = json.load(user_info_raw)["users"]
    return user_info


@Server.use(app)
class App:
    def __init__(self):
        self.user_count = 0
        self.username = None
        self.email = None
        self.github = None
        self.user_data = {}

    def error_handle(self):
        for value in self.user_data.values():
            if not value:
                print("ERROR OCCURRED: MISSING DATA!")
                return True
        return False

    def log_user(self):
        with open("user_info.json") as user_info_raw:
            user_info = json.load(user_info_raw)

            # Check for duplicate user
            for logged_user in user_info["users"]:
                if logged_user["username"] == self.username:
                    self.js.document.getElementById('Submit Form Error').innerHTML = "Username already taken."
                    return False
                elif logged_user["email"] == self.email:
                    self.js.document.getElementById('Submit Form Error').innerHTML = "Email already taken."
                    return False
                elif logged_user["github"] == self.github:
                    self.js.document.getElementById('Submit Form Error').innerHTML = "Github Account already taken."
                    return False

            # Log user info
            user_info["users"].append(self.user_data)
            writer(data=user_info, filename="user_info.json")
            return True

    def new_user(self):
        self.username = str(self.js.document.getElementById('Club Username').value)
        self.email = str(self.js.document.getElementById('Club Email').value)
        self.github = str(self.js.document.getElementById('Github Account Name').value)

        self.user_data = {
            "username": self.username,
            "email": self.email,
            "github": self.github,
        }

        # Form Error Handling
        field_error = self.error_handle()
        if field_error:
            self.js.document.getElementById('Submit Form Error').innerHTML = f"Please fill in all fields."
        else:
            print("NEW USER DETECTED! USER:", self.user_data)
            logger = self.log_user()
            if logger:
                self.js.document.getElementById('Submit Form Error').innerHTML = f"Submitted successfully! {self.user_data}"
            else:
                print("Dup Detected.")



@app.route('/signup')
def user_signup():
    logged_user_info = user_data()
    return App.render(render_template('signup.html', user_data=logged_user_info))


if __name__ == '__main__':
    app.run(debug=True)
