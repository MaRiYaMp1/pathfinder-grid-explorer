from difflib import SequenceMatcher

# Take user input
str1 = input("Enter the first sentence: ")
str2 = input("Enter the second sentence: ")

# Calculate similarity ratio
similarity = SequenceMatcher(None, str1, str2).ratio()

# Display score
print(f"\nSimilarity Score: {similarity:.2f}")
