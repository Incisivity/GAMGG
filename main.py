import os
import random
from cryptography.fernet import Fernet

def generate_key():
    key = Fernet.generate_key()
    with open("privatekey.txt", "wb") as key_file:
        key_file.write(key)

def load_key():
    try:
        with open("privatekey.txt", "rb") as key_file:
            return key_file.read()
    except FileNotFoundError:
        generate_key()
        return load_key()  # Retry after generating the key

def encrypt(data, key):
    cipher_suite = Fernet(key)
    return cipher_suite.encrypt(data.encode())

def decrypt(encrypted_data, key):
    cipher_suite = Fernet(key)
    return cipher_suite.decrypt(encrypted_data).decode()

def generate_problem(difficulty):
    num1 = random.randint(1, difficulty * 5)
    num2 = random.randint(1, difficulty * 5)
    operator = random.choice(['+', '-', '*'])
    expression = f"{num1} {operator} {num2}"
    answer = eval(expression)
    return expression, answer

def save_data(money, difficulty, key):
    with open("gamedata", "wb") as file:
        data = f"{money},{difficulty}"
        encrypted_data = encrypt(data, key)
        file.write(encrypted_data)

def load_data(key):
    try:
        with open("gamedata", "rb") as file:
            encrypted_data = file.read()
            decrypted_data = decrypt(encrypted_data, key)
            money, difficulty = map(int, decrypted_data.split(","))
            return money, difficulty
    except (FileNotFoundError, ValueError):
        return 0, 1  # Default values if the file doesn't exist or is corrupted

def main():
    key = load_key()
    total_money, difficulty = load_data(key)
    session_earnings = 0  # Track earnings for the current session

    while True:
        os.system("clear" if os.name == "posix" else "cls")  # Clear console screen

        problem, correct_answer = generate_problem(difficulty)

        print(f"\nCurrent Money: ${total_money} | Earnings: ${session_earnings}")
        print(f"\nSolve the following math problem to earn money:")
        print(problem)

        user_answer = float(input("Your answer: "))

        if user_answer == correct_answer:
            earned_money = random.randint(5, 20)
            total_money += earned_money
            session_earnings += earned_money
            difficulty += 1  # Increase difficulty
            print(f"Correct! You earned ${earned_money}. Your total money: ${total_money}")
        else:
            penalty = round(total_money * 0.1)
            total_money = max(0, total_money - penalty)
            session_earnings -= penalty
            difficulty = max(1, difficulty - 1)  # Decrease difficulty, but not below 1
            print(f"Wrong answer. Penalty: ${penalty}. Your total money remains ${total_money}")

        save_data(total_money, difficulty, key)

if __name__ == "__main__":
    main()
