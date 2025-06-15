import streamlit as st
from spellchecker import SpellChecker

# Function to check grammar
def check_grammar(text):
    # Create a SpellChecker object
    spell = SpellChecker()
    
    # Split the text into words
    words = text.split()
    
    # Check each word for correct spelling
    incorrect_words = []
    for word in words:
        if word.lower() not in spell:
            incorrect_words.append(word)
    
    return incorrect_words

# Streamlit app
st.title("Grammar Check App")

# Input text box
text_input = st.text_area("Enter your text here:")

# Button to check grammar
if st.button("Check Grammar"):
    if text_input:
        incorrect_words = check_grammar(text_input)
        if incorrect_words:
            st.write("Incorrect words found:")
            for word in incorrect_words:
                st.write(word)
        else:
            st.success("No incorrect words found.")
    else:
        st.warning("Please enter some text to check.")

