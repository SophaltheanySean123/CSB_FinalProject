import re

# Example text to search
text = "Hello world, this is a test."

# Define the regex pattern
pattern = re.compile(r"[a-zA-Z]+,{1}\s{1}")

# Find all matches in the text
matches = pattern.findall(text)

# Print the matches
print(matches)
