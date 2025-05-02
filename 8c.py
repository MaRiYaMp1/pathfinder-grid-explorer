from textblob import TextBlob

# Take user input
text = input("Enter text for spell checking: ")

# Perform spell correction
blob = TextBlob(text)
corrected_text = blob.correct()

# Display result
print(f"\nCorrected Text: {corrected_text}")
