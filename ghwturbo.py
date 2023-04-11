import tkinter as tk
from tkinter import ttk
import config
import openai

openai.organization = "org-UDN3rNJTrNehJ1QmvH17jil5"
openai.api_key = config.API_KEY
openai.Model.list()


# Define a function to call the ChatGPT API

def call_chatgpt(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a ghostwriter who excels at writing catchy content. You are given a topic and a tone from your client and must respect it no matter what. Do not respond anything else other than what is aksed. Feel free to include emojis if you feel the need."},
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content.strip()


# Define functions for generating content in different formats

def generate_article_draft(text):
    prompt = f"Generate the first draft of an article based on the following text: {text}"
    return call_chatgpt(prompt)


def generate_twitter_format(text, tone):
    # to add: length of thread, thread or not ... images ...
    prompt = f"Write a {tone.lower()} Twitter thread version of the following article (don't forget to include a hook and seperate each tweet): {text}"
    return call_chatgpt(prompt)


def generate_linkedin_format(text, tone):
    # to add: starting with a catchphrase ... carousel ...
    prompt = f"Write a {tone.lower()} LinkedIn version starting with a catchphrase of the following article: {text}"
    return call_chatgpt(prompt)


def generate_youtube_script(text, tone):
    # to add: length of video ...
    prompt = f"Write a {tone.lower()} YouTube video script based on the following article: {text}"
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
    tone = tone_combobox.get()
    tone = "" if (tone == "Neutral") else tone

    if input_text:
        twitter_text = generate_twitter_format(input_text, tone)
        linkedin_text = generate_linkedin_format(input_text, tone)
        youtube_text = generate_youtube_script(input_text, tone)

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

# Add tone selection combobox
tone_label = ttk.Label(mainframe, text="Tone:")
tone_combobox = ttk.Combobox(mainframe, state="readonly", values=[
    "Neutral",
    "Authoritative",
    "Conversational",
    "Enthusiastic",
    "Humorous",
    "Analytical",
    "Professional"
])
tone_combobox.set("Neutral")
tone_label.grid(column=2, row=0, padx=5, pady=5, sticky=(tk.W, tk.E))
tone_combobox.grid(column=3, row=0, padx=5, pady=5, sticky=(tk.W, tk.E))

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
