import random
import time
import sqlite3

# Connect to the SQL database
conn = sqlite3.connect('database.db')
c = conn.cursor()

# Create tables if don't exist
c.execute('''CREATE TABLE IF NOT EXISTS normal
             (name text, score int)''')
c.execute('''CREATE TABLE IF NOT EXISTS timed
             (name text, score int)''')

# Function to generate math problems
def generate_problem():
    # Code goes here
    pass

# Function to play the game without a timer
def play_game():
    score = 0
    while True:
        problem = generate_problem()
        answer = input(f"What is {problem}? ")
        if answer == "quit":
            break
        elif int(answer) == eval(problem):
            score += 1
            print("Correct!")
        else:
            print(f"Incorrect. Your score was {score}.")
            break
    # In here update the normal table with the player's score
    # Put SQL code to update the table here

# Function to play the game with a 5 minute timer
def play_timed_game():
    score = 0
    start_time = time.time()
    while time.time() - start_time < 300:
        problem = generate_problem()
        answer = input(f"What is {problem}? ")
        if answer == "quit":
            break
        elif int(answer) == eval(problem):
            score += 1
            print("Correct!")
        else:
            print(f"Incorrect. Your score was {score}.")
            break
    # Update the timed table with the player's score
    # Put SQL code to update the table here

# Function to display the highscores
def display_highscores():
    normal_scores = c.execute("SELECT * FROM normal").fetchall()
    timed_scores = c.execute("SELECT * FROM timed").fetchall()
    print("Normal Mode High Scores:")
    for score in normal_scores:
        print(f"{score[0]}: {score[1]}")
    print("\nTimed Mode High Scores:")
    for score in timed_scores:
        print(f"{score[0]}: {score[1]}")

# Function to prompt the user for their name and password
def get_credentials():
    name = input("Please enter your name: ")
    password = input("Please enter your password: ")
    # Implement SQL code to check the player's credentials here
    return name

# Main menu function
def main_menu():
    print("Welcome to the Math Game!")
    while True:
        print("\nMAIN MENU")
        print("1. See Highscores")
        print("2. Play")
        print("3. Play with 5 min timer")
        print("4. Quit")
        choice = input("Enter your choice: ")
        if choice == "1":
            display_highscores()
        elif choice == "2":
            play_game()
        elif choice == "3":
            play_timed_game()
        elif choice == "4":
            break
        else:
            print("Invalid choice. Please try again.")

# Start the game by getting the player's credentials
player_name = get_credentials()

# Display the main menu
main_menu()

# Close the SQL connection
conn.close()
