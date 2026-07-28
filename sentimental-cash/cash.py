from cs50 import get_float


def main():
    # Loop for correct usage
    while True:
        # Getting input from the user
        change = get_float("Change owed: ")
        # Checking for positive float value
        if change > 0:
            break

    # Converting change into cents
    cents = round(change * 100)

    # Creating a count for the coin amount
    coins = 0

    # Calculating quarters
    coins += cents // 25
    cents %= 25

    # Calculating dimes
    coins += cents // 10
    cents %= 10

    # Calculating nickels
    coins += cents // 5
    cents %= 5

    # Calculating pennies - remaining coins should be pennies from now on
    coins += cents

    print(coins)


if __name__ == "__main__":
    main()
