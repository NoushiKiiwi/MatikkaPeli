import random
import time
import sqlite3
import hashlib
import os

# Connect to the SQL database
conn = sqlite3.connect('database.db')
c = conn.cursor()

# Create tables if don't exist
c.execute('''CREATE TABLE IF NOT EXISTS normal
             (name text, score int)''')
c.execute('''CREATE TABLE IF NOT EXISTS timed
             (name text, score int)''')

def main_menu():
    """Prints the menu and checks input"""
    print("Welcome to the Math Game!")
    while True:
        print("\nMAIN MENU")
        print("1. See Highscores")
        print("2. Play")
        print("3. Play with 5 min timer")
        print("4. Quit")
        choice = input("Enter your choice: ")
        choices = ["1", "2", "3", "4"]
        if choice in choices:
            break
        else:
            print("Invalid choice. Please try again.")


def create_account(username, password):
    """Create and user account and insert it to database"""
    salt = os.urandom(32)

    #Ask user inputs
    print("Create account:")
    name = input("Create username: ")
    password = input("Create password: ")

    #Make secure password
    hashed_password = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
    #Insert password to database
    conn.execute("INSERT INTO Players (name, password, hash, salt) VALUES (?, ?, ?, ?); ", [username, password, hashed_password, salt])


def login(conn, username, password):
    """Ask for username and password and check if right from database"""

    fromdb = conn.execute("SELECT hash, salt FROM Players WHERE name = ?;", [username]).fetchall()

    #Check if login went OK
    if len(fromdb) != 0:
        verrattava_hash = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), fromdb[0][1], 100000)
        if verrattava_hash == fromdb[0][0]:
            print("Loging succeeded")
        else:
            print("Incorrect password")
    else:
        print("Incorrect username")
    
    return username


def generate_problem():
     #Choose random value to determine the calculation type
    value = random.randint(0,3)
    #Add
    if value == 0:
        return str(random.randint(1,100)) + " + " + str(random.randint(1,100)) 
    #Subtract
    elif value == 1:
        return  str(random.randint(1,100)) + " - " + str(random.randint(1,100))  
    #Multiply
    elif value == 2:
        return str(random.randint(0,10)) + " * " + str(random.randint(0,10)) 
    #Divide
    elif value == 3:
        return  str(random.randint(1,100)) + " / " + str(random.randint(1,10)) 


def play_game():
    """Game mode where the game stops if you answer wrong"""
    score = 0
    while True:
        problem = generate_problem()
        #Check that the user input is a float
        while True:
            try:
                answer = float(input(f"What is {problem}? "))
                break
            except:
                print(f"Insert a numeric value as an answer!")
            
        correctAnswer = round(eval(problem), 1)
        if answer == "quit":
            break
        elif int(answer) == eval(problem):
            score += 1
            print("Correct!")
        else:
            print(f"Incorrect. The right answer is {correctAnswer}. Your score was {score}.")
            break
    # In here update the normal table with the player's score
    # Put SQL code to update the table here


def play_timed_game():
    """Game mode where the game stops when timer runs out of time"""
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

# Function to display the highscores show only top 5
def display_highscores():
    normal_scores = c.execute("SELECT * FROM normal ORDER BY score DESC LIMIT 5").fetchall()
    timed_scores = c.execute("SELECT * FROM timed ORDER BY score DESC LIMIT 5").fetchall()
    print("Normal Mode High Scores Top-5:")
    for score in normal_scores:
        print(f"{score[0]}: {score[1]}")
    print("\nTimed Mode High Scores Top-5:")
    for score in timed_scores:
        print(f"{score[0]}: {score[1]}")


def main():

    # Start the game by getting the player's credentials
    player_name = login()

    while True:
        choice = main_menu()
        if choice == "4":
            print("Thank you for playing!")
            break
        elif choice == "1":
            display_highscores()
        elif choice == "2":
            play_game()
        else:
            play_timed_game()

    # Close the SQL connection
    conn.close()

if __name__ == "__main__":
    main()
