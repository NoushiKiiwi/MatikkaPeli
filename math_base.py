import random
import time
import sqlite3
import hashlib
import os

# Connect to the SQL database
c = sqlite3.connect('mathgamedb.db')
c.isolation_level = None

# Create tables if don't exist
c.execute('''CREATE TABLE IF NOT EXISTS Players(
            username VARCHAR(40) PRIMARY KEY,
            hash VARCHAR(60),
            salt VARCHAR(60))''')
#Score table in normal game
c.execute('''CREATE TABLE IF NOT EXISTS ScoreAmounts(
            id INTEGER PRIMARY KEY, 
            username INTEGER NOT NULL, 
            score INTEGER NOT NULL, 
            gameMode VARCHAR(10))''')
#Score table in timed game
c.execute('''CREATE TABLE IF NOT EXISTS ScoreTimed(
            id INTEGER PRIMARY KEY, 
            username INTEGER NOT NULL, 
            score INTEGER NOT NULL, 
            gameMode VARCHAR(10), 
            seconds INTEGER)''')

def account_menu():
    """Prints the login and account creation menu"""
    while True:
        print("\nLogin or create account."
            "\n1. Login"
            "\n2. Create account")
        choice = input("Enter your choice: ")
        choices = ["1", "2"]
        if choice in choices:
            return choice
        else:
            print("Invalid choice. Please try again.")

def main_menu():
    """Prints the menu and checks input"""
    while True:
        print("\nMAIN MENU")
        print("1. See Highscores")
        print("2. Play")
        print("3. Play with 5 min timer")
        print("4. Quit")
        choice = input("Enter your choice: ")
        choices = ["1", "2", "3", "4"]
        if choice in choices:
            return choice
        else:
            print("Invalid choice. Please try again.")


def create_account():
    """Create a user account and insert it into the database"""
    salt = os.urandom(32)

    # Ask user inputs
    print("Create account:")
    while True:
        username = input("Create username: ")
        # Check if the username already exists in the database
        result = c.execute("SELECT username FROM Players WHERE username = ?;",
                            [username]).fetchone()
        if result is None:
            break
        print("Username already exists. Please try another.")

    password = input("Create password: ")

    # Make secure password
    hashed_password = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), 
                                          salt, 100000)
    # Insert password to database
    c.execute("INSERT INTO Players (username, hash, salt) VALUES (?, ?, ?); ", 
              [username, hashed_password, salt])

    print(f"\nWelcome {username} to the Math Game!")

    return username


def login():
    """Ask for username and password and check if right from database"""
    # get user input
    username = input("Enter your username: ")

    # Fetch the data from the players table
    test = c.execute("SELECT * FROM players")
    users = test.fetchall()
    
    # check if the user exists
    for user in users:
        if user[0] == username:
            # verify their password
            password = input("Enter your password: ")
            fromdb = c.execute(
                "SELECT username, hash, salt FROM Players WHERE username = ?;", 
                [username]).fetchone()
            if fromdb is not None:
                stored_hash = fromdb[1]
                salt = fromdb[2]
                input_hash = hashlib.pbkdf2_hmac('sha256', 
                                                 password.encode('utf-8'), 
                                                 salt, 100000)
                if input_hash == stored_hash:
                    print(f"\nWelcome {username}!")
                else:
                    print("Incorrect password, try again.")
                    login()

            return username
    
    print("Incorrect username")

    while True:
        choice = input("Do you want to try again? (y/n)")
        if choice.lower() == "y":
            return login()
        elif choice.lower() == "n":
            quit()
        else:
            print("Please input only y or n")


def generate_problem():
    """Generates math problems"""
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


def play_game(username):
    """Mode where you play until wrong answer"""
    score = 0
    while True:
        problem = generate_problem()
        #Checking for correct input
        while True:
            answer = input(f"What is {problem}? ")
            #Typing 'quit' exits the game
            if answer == "quit":
                return
            #Check that the answer is a number
            try:
                answer = float(answer)
                break
            except:
                print(f"Insert a numeric value as an answer!")
            
        correctAnswer = round(eval(problem), 1)
        if answer == correctAnswer:
            score += 1
            print("Correct!")
        else:
            print(f"Incorrect. The right answer is {correctAnswer}.") 
            print(f"Your score was {score}.")
            break
    #Updates the score table
    add_score(username, score)


def add_score(username, score):
    """Add the score to the database"""
    c.execute("INSERT INTO ScoreAmounts (username, score) VALUES (?, ?)", 
              [username, score])


def play_timed_game(username):
    """Mode where you play until time runs out"""
    score = 0
    wrong = 0
    start_time = time.time()
    while time.time() - start_time < 300:
        problem = generate_problem()
        #Checking for correct input
        while True:
            answer = input(f"What is {problem}? ")
            #Typing 'quit' exits the game
            if answer == "quit":
                return
            #Check that the answer is a number
            try:
                answer = float(answer)
                break
            except:
                print(f"Insert a numeric value as an answer!")
        correctAnswer = round(eval(problem), 1)
        if answer == correctAnswer:
            score += 1
        else:
            wrong += 1
    print(f"Times up! You got {score} correct and {wrong} wrong!")
    # Updates the timed table with the player's score
    add_timedScore(username, score, 300)


def add_timedScore(username, score, seconds):
    """Add the score to the database"""
    c.execute(
        "INSERT INTO ScoreTimed (username, score, seconds) VALUES (?, ?, ?)", 
        [username, score, seconds])


def display_highscores():
    """Display the highscores"""
    normal_scores = c.execute(
        "SELECT * FROM ScoreAmounts ORDER BY score DESC LIMIT 5").fetchall()
    timed_scores = c.execute(
        "SELECT * FROM ScoreTimed ORDER BY score DESC LIMIT 5").fetchall()
    print("\nNormal Mode High Scores:")
    for score in normal_scores:
        print(f"{score[1]}: {score[2]}")
    print("\nTimed Mode High Scores:")
    for score in timed_scores:
        print(f"{score[1]}: {score[2]}")

def main():

    username = ""
    while True:
        account_choice = account_menu()
        if account_choice == "1":
            username = login()
            break
        else:
            username = create_account()
            break

    while True:
        choice = main_menu()
        if choice == "1":
            display_highscores()
        elif choice == "2":
            play_game(username)
        elif choice == "3":
            play_timed_game(username)
        else:
            break
        
    # Close the SQL connection
    c.close()

if __name__ == "__main__":
        main()