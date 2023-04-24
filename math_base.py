import random
import time
import sqlite3
import hashlib
import os

# Connect to the SQL database
conn = sqlite3.connect('mathgamedb.db')
c = conn.cursor()

# Create tables if don't exist
#Players username table
c.execute('''CREATE TABLE IF NOT EXISTS Players(
            username VARCHAR(40) PRIMARY KEY, 
            password VARCHAR(60) NOT NULL,
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
            return choice
        else:
            print("Invalid choice. Please try again.")


def create_account():
    """Create and user account and insert it to database"""
    salt = os.urandom(32)

    #Ask user inputs
    print("Create account:")
    username = input("Create username: ")
    password = input("Create password: ")

    #Make secure password
    hashed_password = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
    #Insert password to database
    conn.execute("INSERT INTO Players (username, password, hash, salt) VALUES (?, ?, ?, ?); ", [username, password, hashed_password, salt])
    return username


def login(conn):
    """Ask for username and password and check if right from database"""
    username = input("Insert username: ")
    password = input("Insert password: ")

    fromdb = conn.execute("SELECT hash, salt FROM Players WHERE username = ?;", [username]).fetchall()

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
        elif answer == correctAnswer:
            score += 1
            print("Correct!")
        else:
            print(f"Incorrect. The right answer is {correctAnswer}. Your score was {score}.")
            break
    # In here update the normal table with the player's score
    # Put SQL code to update the table here
    add_score(username, score)


def add_score(username, score):
    """Add the score to the database"""
    c.execute("INSERT INTO ScoreAmounts (username, score) VALUES (?, ?)", [username, score])


def play_timed_game(username):
    """Mode where you play until time runs out"""
    score = 0
    start_time = time.time()
    while time.time() - start_time < 300:
        problem = generate_problem()
        while True:
            try:
                answer = float(input(f"What is {problem}? "))
                break
            except:
                print(f"Insert a numeric value as an answer!")
        correctAnswer = round(eval(problem), 1)
        if answer == "quit":
            break
        elif answer == correctAnswer:
            score += 1
            print("Correct!")
        else:
            print(f"Incorrect. The right answer is {correctAnswer}. Your score was {score}.")
            break
    # Update the timed table with the player's score
    # Put SQL code to update the table here
    add_timedScore(username, score, 300)


def add_timedScore(username, score, seconds):
    """Add the score to the database"""
    c.execute("INSERT INTO ScoreTimed (username, score, seconds) VALUES (?, ?, ?)", [username, score, seconds])



def display_highscores():
    """Display the highscores"""
    normal_scores = c.execute("SELECT * FROM normal").fetchall()
    timed_scores = c.execute("SELECT * FROM timed").fetchall()
    print("Normal Mode High Scores:")
    for score in normal_scores:
        print(f"{score[0]}: {score[1]}")
    print("\nTimed Mode High Scores:")
    for score in timed_scores:
        print(f"{score[0]}: {score[1]}")


def main():

    # Start the game by getting the player's credentials
    #player_name = login()
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
    conn.close()

if __name__ == "__main__":
    main()