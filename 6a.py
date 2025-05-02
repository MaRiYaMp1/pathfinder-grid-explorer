from itertools import permutations

def solve_cryptarithmetic():
    print("Cryptarithmetic Puzzle Solver")
    print("Enter the puzzle in the format: SEND + MORE = MONEY")
    puzzle = input("Enter the puzzle: ").upper().replace(" ", "")
    
    try:
        # Parse the input
        parts = puzzle.split('=')
        left_part = parts[0].split('+')
        word1 = left_part[0].strip()
        word2 = left_part[1].strip()
        result_word = parts[1].strip()
    except:
        print("Invalid input format. Please use format like 'SEND + MORE = MONEY'")
        return None
    
    # Get all unique letters
    letters = sorted(list(set(word1 + word2 + result_word)))
    if len(letters) > 10:
        print("Error: Too many unique letters (maximum 10)")
        return None
    
    print(f"\nSolving: {word1} + {word2} = {result_word}")
    print(f"Unique letters: {', '.join(letters)}")
    
    digits = range(10)
    first_letters = {word1[0], word2[0], result_word[0]}
    
    for perm in permutations(digits, len(letters)):
        sol = dict(zip(letters, perm))
        
        # Skip solutions where first letters are 0
        if any(sol[letter] == 0 for letter in first_letters):
            continue
            
        # Calculate numerical values
        def word_to_num(word):
            num = 0
            for c in word:
                num = num * 10 + sol[c]
            return num
        
        num1 = word_to_num(word1)
        num2 = word_to_num(word2)
        result = word_to_num(result_word)
        
        if num1 + num2 == result:
            print("\nSolution found:")
            print(f"{word1}: {num1}")
            print(f"{word2}: {num2}")
            print(f"{result_word}: {result}")
            print("Letter assignments:")
            for letter in letters:
                print(f"{letter}: {sol[letter]}")
            return sol
    
    print("\nNo solution found")
    return None

# Example usage:
# When prompted, enter: SEND + MORE = MONEY
solve_cryptarithmetic()
