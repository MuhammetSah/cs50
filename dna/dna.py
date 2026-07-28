import csv
import sys


def main():

    # Check for command-line usage
    if len(sys.argv) != 3:
        print("Usage: python dna.py data.csv sequence.txt")
        sys.argv.exit(1)

    # Read database file into a variable
    with open(sys.argv[1], "r") as csv_file:
        reader = csv.DictReader(csv_file)
        database = [row for row in reader]

    # Read DNA sequence file into a variable
    with open(sys.argv[2], "r") as txt_file:
        sequence = txt_file.read()

    # Find longest match of each STR in DNA sequence
    str_count = {}
    # Check if the first element is a name and skip it
    for key in database[0].keys():
        if key == "name":
            continue
        # If its not a name add up the count
        str_count[key] = longest_match(sequence, key)

    # Check database for matching profiles
    for row in database:
        match = True
        # If the first element is a name - skip it
        for key in row.keys():
            if key == "name":
                continue
            # Checking if the value is not equal so the program can skip this person
            if int(row[key]) != str_count[key]:
                match = False
                break
        # If a match is found - Print out the name
        if match:
            print(row["name"])
            return

    # If no matches found - print out No match
    print("No match")


def longest_match(sequence, subsequence):
    """Returns length of longest run of subsequence in sequence."""

    # Initialize variables
    longest_run = 0
    subsequence_length = len(subsequence)
    sequence_length = len(sequence)

    # Check each character in sequence for most consecutive runs of subsequence
    for i in range(sequence_length):

        # Initialize count of consecutive runs
        count = 0

        # Check for a subsequence match in a "substring" (a subset of characters) within sequence
        # If a match, move substring to next potential match in sequence
        # Continue moving substring and checking for matches until out of consecutive matches
        while True:

            # Adjust substring start and end
            start = i + count * subsequence_length
            end = start + subsequence_length

            # If there is a match in the substring
            if sequence[start:end] == subsequence:
                count += 1

            # If there is no match in the substring
            else:
                break

        # Update most consecutive matches found
        longest_run = max(longest_run, count)

    # After checking for runs at each character in sequence, return longest run found
    return longest_run


main()
