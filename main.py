import random

def main():
    add()

#Chooses a random value between 0 and given 'maxValue'
def choose_value():
    maxValue = 100
    value = random.randint(0, maxValue)
    return value

#Chooses randomly values 'value1' and 'value2', then adds them to 'result' and prints the equation
def add():
    value1 = choose_value()
    value2 = choose_value()
    result = value1 + value2
    print(value1, " + ", value2) 
    answer = user_input()
    check_answer(answer, result)

#Prompts player for the answer and returns their answer
def user_input():
    answer = input('Input your answer: \n')
    return answer

#Compares players input to correct result
def check_answer(answer, result):
    print("The correct answer is: ", result)
    if answer == result:
        print("You answered right!")
    else:
        print("You answered wrong!")

if __name__ == "__main__":
    main()