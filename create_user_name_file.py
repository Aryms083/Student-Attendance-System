import pickle

user_names = {}  # Start with an empty dictionary

# Optionally, add initial usernames if needed:
user_names[0] = "Aryan Maheshwari"
user_names[1] = "Shashank Yadav"

with open('username.p', 'wb') as file:
    pickle.dump(user_names, file)

print("username.p file created successfully!")
