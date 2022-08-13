from flask_app import app
from flask_app.models.dog_model import Dog
DATABASE = "login_registration_schema"


if __name__ == "__main__":
    app.run(debug=True)