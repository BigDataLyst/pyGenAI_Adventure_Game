# pyGenAI_Adventure_Game
created a text-based adventure game inspired by "Dungeon Crawler Carl" by Matt Dinniman which utilizes Google's Gemini to generate content via API calls.

Initial upload of my genAI text-based adventure game, adventure_game.py, inspired by "Dungeon Crawler Carl" by Matt Dinniman
Preliminary setup:
Two files here: 
adventure_game.py
GoogleGenAI_productKey.py
The second is a stand-in file which you will need to have updated with your personal Google API key (see instructions below).

Bash
pip install google.genai

Python
import google.generativeai as genai
import json

Create a separate file with your key, e.g.,
GoogleGenAI_productKey.py, with the following:
###
# GoogleGenAI_productKey.py
# visit aistudio.google.com to create your own free tier Google API Key
My_API_Key ="your_actual_api_key_here"
###

This will be called by the main program with these lines at the top of the script adventure_game.py, stored in the same folder as the above key file:

import time #To add a short delay to avoid free tier rate limits, add time.sleep(1) in order to throttle your API calls
import GoogleGenAI_productKey as keys
my_key = keys.My_API_Key

For more on the book and it's author which inspired my game, visit here to check out "Dungeon Crawler Carl" by Matt Dinniman: https://mattdinniman.com/
