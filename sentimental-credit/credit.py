from cs50 import get_string
import re


def main():
    # Prompt user for the CC-Number
    card = get_string("Number: ")

    # Checksum Calculation
    checksum = 0
    reverse_card = card[::-1]

    for i in range(len(reverse_card)):
        digit = int(reverse_card[i])

        if i % 2 == 1:
            product = digit * 2
            checksum += (product % 10) + (product // 10)
        else:
            checksum += digit

    # If the calculation isn't 0 - checksum fails
    if checksum % 10 != 0:
        print("INVALID")
        return

    # Checking Brands (checking with re.match the starting point and length of the cards)
    if re.match(r"^3[47]\d{13}$", card):
        print("AMEX")
    elif re.match(r"^5[1-5]\d{14}$", card):
        print("MASTERCARD")
    elif re.match(r"4(\d{12}|\d{15})$", card):
        print("VISA")
    else:
        print("INVALID")


if __name__ == "__main__":
    main()
