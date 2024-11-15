import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
import anvil.users
import jwt
import datetime
# This is a server module. It runs on the Anvil server,
# rather than in the user's browser.
#
# To allow anvil.server.call() to call functions here, we mark
# them with @anvil.server.callable.
# Here is an example - you can replace it with your own:
#
# @anvil.server.callable
# def say_hello(name):
#   print("Hello, " + name + "!")
#   return 42
#

if "anvil.app" in anvil.server.get_app_origin():
  my_anvil_app = "https://gmr6it4cqebirfcy.anvil.app/2XHXJME7WI4NEAFYUU5NE44L"
else:
  my_anvil_app = "https://devtest.tdmgroup.net:8001"



SECRET_KEY = "verysecretkey"

def get_jwt_token():
  return 

@anvil.server.route("/token/:token")
def process_jwt(token):

  try:
      # print("token", token)
      
      decoded_token = jwt.decode(token, SECRET_KEY, algorithms=["HS256"]) or None
      print("decoded_token", decoded_token)
      user_id = decoded_token["sub"] or None
      print("user_id", user_id)
      existing_user = app_tables.users.get(email=user_id)
      if not existing_user:
        anvil.users.signup_with_email(user_id,"XXXXXasdjaskldjskdfjlgkjl3jh23k4j2kls;oldf[]asas03042ol",remember= True)
      user_from_tables = app_tables.users.get(email=user_id)
      anvil.users.force_login(user_from_tables, remember=True)
      print(f"Welcome {user_from_tables['email']}, you have successfully logged in!")
      response = anvil.server.HttpResponse(302, "Redirecting to TDM-Platform...")
      response.headers['Location'] = f"{my_anvil_app}"
      return response
  except jwt.ExpiredSignatureError:
      return "Token has expired"
  except jwt.InvalidTokenError as e:
      return f"Invalid token: \n{token}\n{e}"

@anvil.server.callable
def generate_jwt(expiration_minutes=1):
    """
    Generates a JWT token for the currently logged-in user with a specified expiration time.
    
    Parameters:
        expiration_minutes (int): How many minutes until the token expires.
    
    Returns:
        str: The generated JWT token, or None if no user is logged in.
    """
    # Get the current logged-in user
    user = anvil.users.get_user()
    
    # Check if there is a logged-in user
    if not user:
        raise anvil.users.AuthenticationFailed("User is not logged in")

    # Define the token payload
    payload = {
        "user_id": user.get_id(),
        "email": user['email'],  # Adjust if 'username' is stored under a different key
        "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=1)
    }

    # Encode the payload using the secret key
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")

    # Return the generated token (string format)
    return token


def is_user_authenticated_in_server():
  return anvil.users.get_user()