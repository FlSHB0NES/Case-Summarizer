import openai
import sys
import configparser
import string
import re
import os
from rich import print as rprint
from rich.text import Text
import nltk

# Download the 'stopwords' resource if not already available
try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')
from nltk.corpus import stopwords


# Replace with your OpenAI API key
openai.api_key = "<insert API key here>"

def preprocess_text(input_string, remove_whitespace=True, remove_punctuation=False, remove_stopwords=False):
    # Remove extra whitespace
    if remove_whitespace:
        input_string = ' '.join(input_string.split())

    # Remove punctuation
    if remove_punctuation:
        input_string = input_string.translate(str.maketrans('', '', string.punctuation))

    # Remove stopwords
    if remove_stopwords:
        stop_words = set(stopwords.words('english'))
        words = input_string.split()
        input_string = ' '.join([word for word in words if word.lower() not in stop_words])

    return input_string


def save_chat_log(messages, filename):
    logs_subdir = "chat_logs"  # Name of the subdirectory to save chat logs

    # Create the subdirectory if it doesn't exist
    if not os.path.exists(logs_subdir):
        os.makedirs(logs_subdir)

    # Save the chat log in the subdirectory
    filepath = os.path.join(logs_subdir, filename)
    with open(filepath, 'w') as file:
        for message in messages:
            role = message['role'].upper()
            content = message['content']
            content = re.sub(r"<h>|</h>|<k>|</k>", "", content)
            file.write(f"\n{role}: {content}\n")

def apply_styles(text):
    styled_text = Text()

    # Split the text into segments based on the tags
    segments = re.split(r"(<h>.*?</h>|<k>.*?</k>)", text)

    for segment in segments:
        if "<h>" in segment and "</h>" in segment:
            header = re.sub(r"<h>|</h>", "", segment)
            styled_text.append(header, style="bold white underline")
        elif "<k>" in segment and "</k>" in segment:
            key_term = re.sub(r"<k>|</k>", "", segment)
            styled_text.append(key_term, style="bold yellow")
        else:
            styled_text.append(segment)

    return styled_text


def chat_with_gpt(messages):
    response = openai.ChatCompletion.create(
        model=gpt_model,
        messages=messages
    )
    return response.choices[0].message.content.strip()

if len(sys.argv) < 2:
    rprint("Usage: python script.py <business_case_file.txt>")
    sys.exit(1)

input_filename = sys.argv[1]
input_subdir = "text_inputs"  # Name of the subdirectory containing the text input files
filename = os.path.join(input_subdir, input_filename)  # Add the subdirectory to the file path

# Read config file
config = configparser.ConfigParser()
config.read(os.path.join(os.path.dirname(__file__), 'config.ini'))

# Preprocessing options
remove_whitespace = config.getboolean('preprocessing', 'remove_whitespace')
remove_punctuation = config.getboolean('preprocessing', 'remove_punctuation')
remove_stopwords = config.getboolean('preprocessing', 'remove_stopwords')

# System message
system_prompt = config.get('settings', 'system_message')
first_message = config.get('settings', 'first_message')
gpt_model = config.get('settings', 'gpt_model')

with open(filename, 'r') as file:
    business_case = preprocess_text(file.read(), remove_whitespace, remove_punctuation, remove_stopwords)

messages = [
    {"role": "system", "content": system_prompt},
    {"role": "user", "content": f"{first_message} {business_case}"}
]

raw_response = chat_with_gpt(messages)
summary = apply_styles(raw_response)
messages.append({"role": "assistant", "content": raw_response})

rprint("\nSummary of the business case:")
rprint(Text("=" * 40, "cyan"))
rprint(summary)
rprint(Text("=" * 40, "cyan"))

while True:
    rprint("\nEnter your question about the case (type 'quit' to exit):")
    user_question = input()

    if user_question.lower() == 'quit':
        log_filename = "chat_log.txt"
        save_chat_log(messages, log_filename)
        print(f"\nChat log saved to {log_filename}\nRename file if you wish to preserve the log.")
        break

    messages.append({"role": "user", "content": user_question})
    raw_gpt_response = chat_with_gpt(messages)
    gpt_response = apply_styles(raw_gpt_response)
    messages.append({"role": "assistant", "content": raw_gpt_response})

    rprint(f"\n{gpt_model} Assistant:")
    rprint(Text("-" * 40, "cyan"))
    rprint(gpt_response)
    rprint(Text("-" * 40, "cyan"))