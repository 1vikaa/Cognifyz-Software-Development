"""
Cognifyz Technologies - Software Development Internship
Level 1 - Task 1: Basic text-based game (Number Guessing Game)

Rules:
  - The computer picks a secret number in a range set by the difficulty.
  - The player has a limited number of attempts to guess it.
  - After each guess the game says "too high" or "too low".
  - Score = remaining attempts * difficulty multiplier.
"""

import random

DIFFICULTIES = {
    "1": {"name": "Easy",   "max_number": 50,  "attempts": 10, "multiplier": 1},
    "2": {"name": "Medium", "max_number": 100, "attempts": 7,  "multiplier": 2},
    "3": {"name": "Hard",   "max_number": 200, "attempts": 6,  "multiplier": 3},
}


def choose_difficulty():
    print("\nChoose difficulty:")
    for key, d in DIFFICULTIES.items():
        print(f"  {key}. {d['name']} (1-{d['max_number']}, {d['attempts']} attempts)")
    while True:
        choice = input("Enter 1, 2 or 3: ").strip()
        if choice in DIFFICULTIES:
            return DIFFICULTIES[choice]
        print("Invalid choice, please try again.")


def read_guess(max_number):
    while True:
        text = input(f"Your guess (1-{max_number}): ").strip()
        if not text.isdigit():
            print("Please enter a whole number.")
        elif not 1 <= int(text) <= max_number:
            print(f"The number must be between 1 and {max_number}.")
        else:
            return int(text)


def play_round():
    level = choose_difficulty()
    secret = random.randint(1, level["max_number"])
    attempts_left = level["attempts"]

    print(f"\nI'm thinking of a number between 1 and {level['max_number']}.")

    while attempts_left > 0:
        guess = read_guess(level["max_number"])
        attempts_left -= 1

        if guess == secret:
            score = (attempts_left + 1) * level["multiplier"]
            print(f"Correct! You guessed it. Score: {score}")
            return score
        elif guess < secret:
            print("Too low!", end=" ")
        else:
            print("Too high!", end=" ")

        if attempts_left > 0:
            hint = "Very close!" if abs(guess - secret) <= 5 else ""
            print(f"{hint} Attempts left: {attempts_left}")
        else:
            print(f"\nOut of attempts! The number was {secret}.")
    return 0


def main():
    print("=" * 40)
    print("      NUMBER GUESSING GAME")
    print("=" * 40)
    total_score = 0
    rounds = 0

    while True:
        total_score += play_round()
        rounds += 1
        print(f"Total score after {rounds} round(s): {total_score}")
        again = input("\nPlay again? (y/n): ").strip().lower()
        if again != "y":
            break

    print(f"\nThanks for playing! Final score: {total_score}")


if __name__ == "__main__":
    main()
