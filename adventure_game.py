# Before running, make sure to install the google-genai package and set up your API key for Gemini API access. 
#   You can do this by running:
#pip install google-genai
# Create a .py file in you venv called GoogleGenAI_productKey.py and add the following line to it, replacing: 
#   My_API_Key = "myKeyDDXSFHB21" with your actual API key.
import time # This is used to add a short delay before API calls to avoid hitting rate limits too quickly during testing. You can adjust or remove this as needed.

import GoogleGenAI_productKey as keys
my_key = keys.My_API_Key
f"""
Text-based Adventure Game: Treasure Quest on a Game Show
This game lets players explore, make choices, and find treasure while managing view counts.
"""

import random

# Global variable for views
views = random.randint(5, 7)

# Global variable for early exit of the game loop when the game is won or lost, or for development testing
end_game_yet = False

def display_views():
    print(f"Current views: {views}")

import google.genai as genai
import json

# Replace with your actual API Key
#client = genai.Client(api_key=my_key, http_options={'api_version': 'v1'})
client = genai.Client(api_key=my_key) # reverting to cleaner version...

def get_creative_scenario(game_seed, situation_preceeding, risky_option_preceding, safe_option_preceding, choice_made_preceding, views_preceeding):
    # Set up the model with a system instruction for consistent formatting
    
    prompt = f"""
    Generate a creative, high-stakes fictional situation and two distinct response options for a player.  The first will be a risky, entertaining choice that could lead to a dramatic outcome, while the second will be a safe, mundane option that is less likely to cause excitement.
    The situation should be engaging and suitable for a text-based adventure game, and bear in mind (for this game seed ={game_seed}), and the preceding situations and the player choices made, along with the current viewer count, which were situation = {situation_preceeding}, risky_option = {risky_option_preceding}, safe_option = {safe_option_preceding}, choice_made = {choice_made_preceding}, and current_viewer_count = {views_preceeding}.
    If the player chooses the risky and more entertaining solution to the problem, they will be rewarded, and their views count will go up by a random value of +2 to +5 views.  
    If the player chooses the safer and more mundane option, then their views count will go down by a random value of -2 to -3 views.  
    If their views go too low, they will be ejected from the game by being killed by a wandering monster.  
    At the start of the game, the total views count begins with a random value between 5 and 7.
    Return the data in the following JSON format:
    {{
      "situation": "string",
      "risky_option": "string",
      "safe_option": "string"
    }}
    """
    time.sleep(1) # Adding a short delay to avoid hitting rate limits too quickly during testing
    
    try:
        response = client.models.generate_content(
            #model="models/gemini-1.5-flash", # Using this absolute path to bypass the 404
            #model="gemini-2.0-flash", # Using this absolute path to bypass the 404
            #model="gemini-2.0-flash-lite", # More generous free-tier model
            model="gemini-3.1-flash-lite", # Even more generous free-tier model (as of 6/24/24, RPM=15, RPD = 500)
            contents=prompt,
            config={
                'response_mime_type': 'application/json',
            }
        )
        # If 'response.text' causes an error, use the index-based path 
        # as a fallback just in case the SDK version is slightly older
        try:
            raw_text = response.text
        except AttributeError:
            raw_text = response.candidates[0].content.parts[0].text

        # Parse the JSON string from the response
        global game_data
        game_data = json.loads(response.text)
        
        print(f"SITUATION: {game_data['situation']}\n")
        print(f"1) {game_data['risky_option']}")
        print(f"2) {game_data['safe_option']}")
        
        return game_data

    except Exception as e:
        # This will now tell us exactly which line failed if it happens again
        print(f"An error occurred: {e}")
        import traceback
        traceback.print_exc() # This helps see the line number during debugging
        #for m in client.models.list(): 
        #    print(m.name)
        return None

def print_title_art():
    art = r"""
\__    ___/______   ____ _____    ________ _________   ____   \_____  \  __ __   ____   _______/  |_  /\
  |    |  \_  __ \_/ __ \\__  \  /  ___/  |  \_  __ \_/ __ \   /  / \  \|  |  \_/ __ \ /  ___/\   __\ \/
  |    |   |  | \/\  ___/ / __ \_\___ \|  |  /|  | \/\  ___/  /   \_/.  \  |  /\  ___/ \___ \  |  |   /\
  |____|   |__|    \___  >____  /____  >____/ |__|    \___  > \_____\ \_/____/  \___  >____  > |__|   \/
                       \/     \/     \/                   \/         \__>           \/     \/           
  ________                          _________.__                    ___________    .___.__  __  .__               
 /  _____/_____    _____   ____    /   _____/|  |__   ______  _  __ \_   _____/  __| _/|__|/  |_|__| ____   ____  
/   \  ___\__  \  /     \_/ __ \   \_____  \ |  |  \ /  _ \ \/ \/ /  |    __)_  / __ | |  \   __\  |/  _ \ /    \ 
\    \_\  \/ __ \|  Y Y  \  ___/   /        \|   Y  (  <_> )     /   |        \/ /_/ | |  ||  | |  (  <_> )   |  \
 \______  (____  /__|_|  /\___  > /_______  /|___|  /\____/ \/\_/   /_______  /\____ | |__||__| |__|\____/|___|  /
        \/     \/      \/     \/          \/      \/                        \/      \/                         \/                                
    """
    print(art)

def adjust_views(risky=True):
    global views, player_name, game_seed
    if risky:
        change = random.randint(2, 5)
        views += change
        print(f"Risky choice! Views increased by {change}.")
    else:
        change = random.randint(2, 3)
        views -= change
        print(f"Safe choice! Views decreased by {change}.")
    display_views()
    if views <= 0:
        #print("Views dropped to zero or below! A wandering monster appears and kills you! In your next life, try being more entertaining!")
        game_over(player_name,game_seed)
        return False
    if views >= 20:
        #print("Views rose to 20! Wow, you're the next big star!")
        win_game(player_name,game_seed)
        return False
    return True

def start_game():
    print_title_art()
    global views
    views = random.randint(5, 7)  # Reset views at start
    print("Welcome to 'Treasure Quest: Game Show Edition'!")
    print("You are on a live game show where the audience watches your every move.")
    print("Your goal: Find the legendary treasure!")
    print("Choices affect your view count. Stay above 0 or get ejected!")
    display_views()
    global player_name
    player_name = input("Enter your name, adventurer: ")
    global game_seed
    game_seed = player_name + str(random.randint(1, 1000))  # Unique seed for this game session
    print(f"Hello, {player_name}! Your quest begins now.")
    print("You stand at a crossroads. Choose your path:")
    print("1. Enter the dark forest")
    print("2. Explore the mysterious cave")
    choice = input("Enter 1 or 2: ")
    if choice == "1":
        forest_path()
    elif choice == "2":
        cave_path()
    else:
        print("Invalid choice. Try again.")
        start_game()

def forest_path():
    print("\nYou enter the dark forest. The trees are dense, and strange sounds echo.")
    global situation_preceeding
    situation_preceeding = "Problem: You need to cross a river blocking your path."
    global choice_made_preceding
    choice_made_preceding = ""
    global risky_option_preceding
    risky_option_preceding = "1. Risky: Swim across (entertaining but dangerous)"
    global safe_option_preceding
    safe_option_preceding = "2. Safe: Climb a tree to scout ahead, first (mundane but reliable)"
    print("Problem: You need to cross a river blocking your path.")
    print("1. Risky: Swim across (entertaining but dangerous)")
    print("2. Safe: Climb a tree to scout ahead, first (mundane but reliable)")
    choice = input("Enter 1 or 2: ")
    choice_made_preceding = choice
    if choice == "1":
        if not adjust_views(risky=True):
            #game_over()
            return
        print("You swim across! The audience loves it. You find a clue leading to the treasure.")
        print("But wait, there's more...")
        sub_choice()
    elif choice == "2":
        if not adjust_views(risky=False):
            #game_over()
            return
        print("You decide to climb a tree. You determine that it's safe to swim across, anyway, but the crowd is yawning... You lose views for being boring, but you survive to continue your journey...")
        sub_choice()
    else:
        print("Invalid choice.")
        forest_path()
    

def sub_choice():
    global end_game_yet, game_data
    end_game_yet = False #useful for debugging, as it allows us to bypass the game loop exit when testing the sub_choice function independently
    global situation_preceeding, risky_option_preceding
    global safe_option_preceding, choice_made_preceding
    global api_failures
    api_failures = 0

    while (views > 0 and views < 20) and end_game_yet == False:
        scenario = get_creative_scenario(game_seed, situation_preceeding, risky_option_preceding, safe_option_preceding, choice_made_preceding, views)
        if scenario is None:
            print("The game show is experiencing technical difficulties! Trying again...")
            api_failures += 1
            if api_failures >= 3:
                print("Multiple API failures. Ending game for now. Please try again later.")
                return
                #restart_game()?
            continue
        #print(f"SITUATION: {game_data['situation']}\n")
        #print(f"1) {game_data['risky_option']}")
        #print(f"2) {game_data['safe_option']}")
        
        choice = input("Enter 1 or 2: ")
        situation_preceeding = game_data['situation'] # This is the NEW situation
        risky_option_preceding = game_data['risky_option']
        safe_option_preceding = game_data['safe_option']
        choice_made_preceding = choice
        if choice == "1":
            if not adjust_views(risky=True):
                end_game_yet = True
                return
            print("\nOutcome: The audience is thrilled with your bravery!")

            #print("You climb and get the map! The treasure is in the cave. You win!")
            #end_game_yet = True
            #win_game()
        elif choice == "2":
            if not adjust_views(risky=False):
                #end_game_yet = True
                #game_over()
                return
            print("\nOutcome: You survived, but the crowd is yawning...")
            #end_game_yet = True
            #game_over()

        else:
            print("Invalid choice.")
            continue

def cave_path():
    global situation_preceeding
    situation_preceeding = "You enter the mysterious cave. It's dark and eerie."
    global choice_made_preceding
    choice_made_preceding = ""
    global risky_option_preceding
    risky_option_preceding = "1. Risky: Who needs torches? Heroes let their eyes adjust to the darkness and then proceed (entertaining but risky)"
    global safe_option_preceding
    safe_option_preceding = "2. Safe: Light a torch (boring but safe)"
    print(f"\n{situation_preceeding}")
    print("Problem: You need to light a torch to proceed.")
    print(f"{risky_option_preceding}")
    print(f"{safe_option_preceding}")
    choice = input("Enter 1 or 2: ")
    choice_made_preceding = choice
    if choice == "1":
        if not adjust_views(risky=True):
            #end_game_yet = True
            #game_over()
            return
        print("Torches are for n00bs! Your eyes adjust, as the audience sees the cave's hidden beauty coming into view through the feed to your ocular implants we've installed. They love it!")
        print("But wait, there's more...")
        sub_choice()
        #win_game()
    elif choice == "2":
        if not adjust_views(risky=False):
            end_game_yet = True
            game_over()
            return
        print("You decide to climb a tree. You determine that it's safe to swim across, anyway, but the crowd is yawning... You lose views for being boring, but you survive to continue your journey...")
        sub_choice()
        #end_game_yet = True
        #game_over()
    else:
        print("Invalid choice.")
        cave_path()

def get_creative_scenario_win(player_name,game_seed):
    # Set up the model with a system instruction for consistent formatting
    
    prompt = f"""
    The player made it! after a series of challenges, the player has exceeded the views threshold required to win.  Generate a 
    creative conclusion to this saga where {player_name} is congratulated and presented with their prize. Bear in mind the most recent series of 
    situations and choices made, for this session's game seed ={game_seed}.
    Return the data in the following JSON format:
    {{
      "victory_text": "string"
    }}
    """
    time.sleep(1) # Adding a short delay to avoid hitting rate limits too quickly during testing
    
    try:
        response = client.models.generate_content(
            #model="models/gemini-1.5-flash", # Using this absolute path to bypass the 404
            #model="gemini-2.0-flash", # Using this absolute path to bypass the 404
            #model="gemini-2.0-flash-lite", # More generous free-tier model
            model="gemini-3.1-flash-lite", # Even more generous free-tier model (as of 6/24/24, RPM=15, RPD = 500)
            contents=prompt,
            config={
                'response_mime_type': 'application/json',
            }
        )
        # If 'response.text' causes an error, use the index-based path 
        # as a fallback just in case the SDK version is slightly older
        try:
            raw_text = response.text
        except AttributeError:
            raw_text = response.candidates[0].content.parts[0].text

        # Parse the JSON string from the response
        global game_data
        game_data = json.loads(response.text)
        
        print(f"{game_data['victory_text']}\n")
        
        return game_data

    except Exception as e:
        # This will now tell us exactly which line failed if it happens again
        print(f"An error occurred: {e}")
        import traceback
        traceback.print_exc() # This helps see the line number during debugging
        #for m in client.models.list(): 
        #    print(m.name)
        return None

def get_creative_scenario_loss(player_name,game_seed):
    # Set up the model with a system instruction for consistent formatting
    
    prompt = f"""
    The player has failed to meet the views threshold required to win.  Generate a 
    creative conclusion to this saga where {player_name} meets their demise, just 
    after being told to be more entertaining in their next life. Bear in mind the most 
    recent series of situations and choices made, for this session's game seed ={game_seed}.
    Return the data in the following JSON format:
    {{
      "failure_text": "string"
    }}
    """
    time.sleep(1) # Adding a short delay to avoid hitting rate limits too quickly during testing
    
    try:
        response = client.models.generate_content(
            #model="models/gemini-1.5-flash", # Using this absolute path to bypass the 404
            #model="gemini-2.0-flash", # Using this absolute path to bypass the 404
            #model="gemini-2.0-flash-lite", # More generous free-tier model
            model="gemini-3.1-flash-lite", # Even more generous free-tier model (as of 6/24/24, RPM=15, RPD = 500)
            contents=prompt,
            config={
                'response_mime_type': 'application/json',
            }
        )
        # If 'response.text' causes an error, use the index-based path 
        # as a fallback just in case the SDK version is slightly older
        try:
            raw_text = response.text
        except AttributeError:
            raw_text = response.candidates[0].content.parts[0].text

        # Parse the JSON string from the response
        global game_data
        game_data = json.loads(response.text)
        
        print(f"{game_data['failure_text']}\n")
        
        return game_data

    except Exception as e:
        # This will now tell us exactly which line failed if it happens again
        print(f"An error occurred: {e}")
        import traceback
        traceback.print_exc() # This helps see the line number during debugging
        #for m in client.models.list(): 
        #    print(m.name)
        return None

def win_game(player_name,game_seed):
    #print("And what do we have here...? Look down! Congratulations! You found the treasure!")
    global api_failures
    api_failures = 0
    get_creative_scenario_win(player_name,game_seed)
    #while api_failures < 3:
    #    scenario = get_creative_scenario_win(player_name,game_seed)
    #    if scenario is None:
    #            print("The game show is experiencing technical difficulties! Trying again...")
    #            api_failures += 1
    #    else:
    #        print("Multiple API failures. Ending game for now. Please try again later.")
    #        return
    restart_game()

def game_over(player_name,game_seed):
    #print("Game Over!")
    global api_failures
    api_failures = 0
    get_creative_scenario_loss(player_name,game_seed)
    #while api_failures < 3:
    #    scenario = get_creative_scenario_loss(player_name,game_seed)
    #    if scenario is None:
    #            print("The game show is experiencing technical difficulties! Trying again...")
    #            api_failures += 1
    #    else:
    #        print("Multiple API failures. Ending game for now. Please try again later.")
    #        return
    restart_game()

def restart_game():
    choice = input("Play again? (y/n): ")
    if choice.lower() == "y":
        start_game()
    else:
        print("Thanks for playing!")

# Run the game
if __name__ == "__main__":
    start_game()