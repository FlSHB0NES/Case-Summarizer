# GPT-4 Business Case Analysis

This program uses the OpenAI GPT model to analyze and summarize business cases from a marketing standpoint. It provides a detailed summary of the case, highlights key terms, and allows users to ask follow-up questions related to the case.

## Requirements

- Python 3.6+
- OpenAI Python library
- NLTK library
- Rich library

## Installation

To install the required dependencies, run the following command:

```
pip install -r requirements.txt
```

## Usage

Place the business case text files in the `text_inputs` subdirectory. Run the program with the following command, replacing `<business_case_file.txt>` with the name of the business case file you want to analyze:

```
python script.py <business_case_file.txt>
```

The program will display the summary of the business case and prompt you for questions related to the case. Type your questions and press Enter. To exit the program, type 'quit' and press Enter.

The chat logs will be saved in the `chat_logs` subdirectory.

## Configuration

You can customize the preprocessing options and GPT model settings by modifying the `config.ini` file. The available options are:

- `remove_whitespace`: Remove extra whitespaces (True/False)
- `remove_punctuation`: Remove punctuation marks (True/False)
- `remove_stopwords`: Remove common stopwords (True/False)
- `system_message`: System message for the AI assistant
- `gpt_model`: GPT API model to be used