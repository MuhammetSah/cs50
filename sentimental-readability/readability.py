def main():
    # Prompting user for a text
    text = input("Text: ")

    # Counting letter
    letter = sum( 1 for _ in text if _.isalpha())

    # Counting words
    word = len(text.split())

    # Counting sentences
    sentences = text.count("!") + text.count("?") + text.count(".")

    # Getting average per 100 words of sentences and letter
    letter = (letter / word) * 100
    sentences = (sentences / word) * 100

    # Coleman-Liau index
    index = round(0.0588 * letter - 0.296 * sentences - 15.8)

    if index >= 16:
        print("Grade 16+")
    elif index < 1:
        print("Before Grade 1")
    else:
        print(f"Grade {index}")


if __name__ == "__main__":
    main()
