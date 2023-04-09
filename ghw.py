import tkinter as tk
from tkinter import ttk
import config
import requests
import time

# Replace with your actual ChatGPT API key
API_KEY = config.API_KEY


# Define a function to call the ChatGPT API

def call_chatgpt(prompt):
    headers = {
        "Authorization": f"Bearer {API_KEY}"
    }
    data = {
        "prompt": prompt,
        "max_tokens": 150  # Default 150
    }
    response = requests.post(
        "https://api.openai.com/v1/engines/text-davinci-002/completions", headers=headers, json=data)  # text-davinci-002 or 003
    response.raise_for_status()
    return response.json()["choices"][0]["text"].strip()


'''
def call_chatgpt(prompt):
    headers = {
        "Authorization": f"Bearer {API_KEY}"
    }
    data = {
        "prompt": prompt,
        "max_tokens": 150
    }

    for i in range(5):  # You can adjust the number of retries
        try:
            response = requests.post(
                "https://api.openai.com/v1/engines/text-davinci-002/completions", headers=headers, json=data)
            response.raise_for_status()
            return response.json()["choices"][0]["text"].strip()
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 429:
                wait_time = 2 ** i
                print(
                    f"Rate limit exceeded. Retrying in {wait_time} seconds...")
                time.sleep(wait_time)
            else:
                raise e
    raise Exception(
        "Failed to get a response from the API after multiple retries.")
'''


# Define functions for generating content in different formats

def generate_article_draft(text):
    prompt = f"Generate the first draft of an article based on the following text: {text}"
    return call_chatgpt(prompt)


def generate_twitter_format(text):
    prompt = f"Write a Twitter version of the following article: {text}"
    return call_chatgpt(prompt)


def generate_linkedin_format(text):
    prompt = f"Write a LinkedIn version of the following article starting with a catchy sentence: {text}"
    return call_chatgpt(prompt)


def generate_youtube_script(text):
    prompt = f"Write a YouTube video script based on the following article: {text}"
    return call_chatgpt(prompt)


# Define UI element event handlers

def on_generate_article_draft():
    input_text = text_input.get("1.0", tk.END).strip()
    if input_text:
        output_text = generate_article_draft(input_text)
        text_output.delete("1.0", tk.END)
        text_output.insert(tk.END, output_text)


def on_generate_all_formats():
    input_text = text_output.get("1.0", tk.END).strip()
    if input_text:
        twitter_text = generate_twitter_format(input_text)
        time.sleep(5)
        linkedin_text = generate_linkedin_format(input_text)
        time.sleep(5)
        youtube_text = generate_youtube_script(input_text)

        twitter_output.delete("1.0", tk.END)
        linkedin_output.delete("1.0", tk.END)
        youtube_output.delete("1.0", tk.END)

        twitter_output.insert(tk.END, twitter_text)
        linkedin_output.insert(tk.END, linkedin_text)
        youtube_output.insert(tk.END, youtube_text)


# Create the Tkinter UI
root = tk.Tk()
root.title("ChatGPT Article Generator")

mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(tk.N, tk.W, tk.E, tk.S))
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

# Create input and output text boxes
text_input = tk.Text(mainframe, wrap=tk.WORD)
text_output = tk.Text(mainframe, wrap=tk.WORD)
text_input.grid(column=0, row=0, sticky=(tk.N, tk.W, tk.E, tk.S))
text_output.grid(column=1, row=0, sticky=(tk.N, tk.W, tk.E, tk.S))

# Create output text boxes for Twitter, LinkedIn, and YouTube formats
twitter_output = tk.Text(mainframe, wrap=tk.WORD)
linkedin_output = tk.Text(mainframe, wrap=tk.WORD)
youtube_output = tk.Text(mainframe, wrap=tk.WORD)

twitter_output.grid(column=0, row=1, sticky=(tk.N, tk.W, tk.E, tk.S))
linkedin_output.grid(column=1, row=1, sticky=(tk.N, tk.W, tk.E, tk.S))
youtube_output.grid(column=2, row=1, sticky=(tk.N, tk.W, tk.E, tk.S))

# Create buttons
buttons_frame = ttk.Frame(mainframe)
generate_article_button = ttk.Button(
    buttons_frame, text="Generate Article Draft", command=on_generate_article_draft)
generate_all_formats_button = ttk.Button(
    buttons_frame, text="Generate All Formats", command=on_generate_all_formats)

# Configure button layout
generate_article_button.grid(column=0, row=0, padx=5, pady=5)
generate_all_formats_button.grid(column=1, row=0, padx=5, pady=5)
buttons_frame.grid(column=0, row=2, columnspan=3, sticky=(tk.W, tk.E))

# Configure grid weights
for i in range(3):
    mainframe.columnconfigure(i, weight=1)
    mainframe.rowconfigure(i, weight=1)

# Run the Tkinter main loop
root.mainloop()
