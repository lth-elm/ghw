import tkinter as tk
from tkinter import ttk
import requests
# import time

# Replace with your actual ChatGPT API key
API_KEY = "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"


# Define a function to call the ChatGPT API

def call_chatgpt(prompt):
    headers = {
        "Authorization": f"Bearer {API_KEY}"
    }
    data = {
        "prompt": prompt,
        "max_tokens": 150
    }
    response = requests.post(
        "https://api.openai.com/v1/engines/text-davinci-002/completions", headers=headers, json=data)
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
    prompt = f"Write a LinkedIn version of the following article: {text}"
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


def on_generate_twitter_format():
    input_text = text_output.get("1.0", tk.END).strip()
    if input_text:
        output_text = generate_twitter_format(input_text)
        text_output.delete("1.0", tk.END)
        text_output.insert(tk.END, output_text)


def on_generate_linkedin_format():
    input_text = text_output.get("1.0", tk.END).strip()
    if input_text:
        output_text = generate_linkedin_format(input_text)
        text_output.delete("1.0", tk.END)
        text_output.insert(tk.END, output_text)


def on_generate_youtube_script():
    input_text = text_output.get("1.0", tk.END).strip()
    if input_text:
        output_text = generate_youtube_script(input_text)
        text_output.delete("1.0", tk.END)
        text_output.insert(tk.END, output_text)


# Create the Tkinter UI
root = tk.Tk()
root.title("ChatGPT Article Generator")

# Create input and output text boxes
text_input = tk.Text(root, wrap=tk.WORD)
text_output = tk.Text(root, wrap=tk.WORD)
text_input.pack(expand=True, fill=tk.BOTH)
text_output.pack(expand=True, fill=tk.BOTH)

# Create buttons
buttons_frame = ttk.Frame(root)
generate_article_button = ttk.Button(
    buttons_frame, text="Generate Article Draft", command=on_generate_article_draft)
generate_twitter_button = ttk.Button(
    buttons_frame, text="Twitter Format", command=on_generate_twitter_format)
generate_linkedin_button = ttk.Button(
    buttons_frame, text="LinkedIn Format", command=on_generate_linkedin_format)
generate_youtube_button = ttk.Button(
    buttons_frame, text="YouTube Script", command=on_generate_youtube_script)

# Configure button layout
generate_article_button.grid(column=0, row=0, padx=5, pady=5)
generate_twitter_button.grid(column=1, row=0, padx=5, pady=5)
generate_linkedin_button.grid(column=2, row=0, padx=5, pady=5)
generate_youtube_button.grid(column=3, row=0, padx=5, pady=5)
buttons_frame.pack(fill=tk.X)

# Run the Tkinter main loop
root.mainloop()
