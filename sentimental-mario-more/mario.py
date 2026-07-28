from cs50 import get_int


def main():
    # Prompt the user for a valid integer
    while True:
        height = get_int("Height: ")
        # Check for correct usage
        if 1 <= height <= 8:
            break

    # Build the pyramid
    for i in range(1, height + 1):
        spaces = height - i
        bricks = i

        # Print out the pyramids and gaps
        print((" " * spaces) + ("#" * bricks) + "  " + ("#" * bricks))


if __name__ == "__main__":
    main()
