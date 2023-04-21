import random
import time
import sqlite3

# Connect to the SQL database
conn = sqlite3.connect('database.db')
c = conn.cursor()

# Create tables if don't exist
<<<<<<< Updated upstream
c.execute('''CREATE TABLE IF NOT EXISTS normal
             (name text, score int)''')
c.execute('''CREATE TABLE IF NOT EXISTS timed
             (name text, score int)''')
=======
c.execute('''CREATE TABLE IF NOT EXISTS Players(
            id INTEGER PRIMARY KEY, 
            username VARCHAR(40) NOT NULL UNIQUE, 
            password VARCHAR(60) NOT NULL,
            hash VARCHAR(60),
            salt VARCHAR(60))''')
c.execute('''CREATE TABLE IF NOT EXISTS ScoreAmounts(
            id INTEGER PRIMARY KEY, 
            playerId INTEGER NOT NULL, 
            score INTEGER NOT NULL, 
            gameMode VARCHAR(10))''')
c.execute('''CREATE TABLE IF NOT EXISTS ScoreTimed(
            id INTEGER PRIMARY KEY, 
            playerId INTEGER NOT NULL, 
            score INTEGER NOT NULL, 
            gameMode VARCHAR(10), 
            seconds INTEGER)''')
#playerId can be changed to playerName if name becomes primary key.

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

>>>>>>> Stashed changes

# Function to generate math problems
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

# Function to play the game without a timer
def play_game():
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
<<<<<<< Updated upstream
=======
    #add_score(playerId, score)
>>>>>>> Stashed changes

# Function to play the game with a 5 minute timer
def play_timed_game():
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
<<<<<<< Updated upstream
=======
    #add_timedScore(playerId, score, 300)
    
def add_timedScore(playerId, score, seconds):
    c.execute("INSERT INTO ScoreTimed (playerId, score, seconds) VALUES (?, ?, ?)", [playerId, score, seconds])
>>>>>>> Stashed changes

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

<<<<<<< Updated upstream
# Main menu function
def main_menu():
    print("Welcome to the Math Game!")
=======
def main():

    # Start the game by getting the player's credentials
    #player_name = login()

>>>>>>> Stashed changes
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
