from flask_app import app
from flask_app.controllers import dogs_controllers, awards_controllers
DATABASE = "login_registration_schema"


if __name__ == "__main__":
    app.run(debug=True)