# Adapted from https://github.com/logicguy1/Discord-Nitro-Generator-and-Checker
# Converted into a Discord bot by https://github.com/dmimukto


from discord_webhook import DiscordWebhook
import requests
import random
import string
import time
import discord
import colored
import os
import discord.ext
from discord.utils import get
from discord.ext import commands, tasks
from discord.ext.commands import has_permissions,  CheckFailure, check
#^ basic imports for other features of discord.py and python ^

from keep_alive import keep_alive

client = discord.Client()

client = commands.Bot(command_prefix = '!') #put your own prefix here

def generator(self, amount): # Function used to generate and store nitro codes in a seperate file
    with open(self.fileName, "w", encoding="utf-8") as file: # Load up the file in write mode
        print("Wait, Generating for you") # Let the user know the code is generating the codes

        start = time.time() # Note the initaliseation time

        for i in range(amount): # Loop the amount of codes to generate
            code = "".join(random.choices(
                string.ascii_uppercase + string.digits + string.ascii_lowercase,
                k = 11
            )) # Generate the code id

            file.write(f"https://youtu.be/{code}\n") # Write the code

        # Tell the user its done generating and how long tome it took
        print(f"Genned {amount} codes | Time taken: {round(time.time() - start, 5)}s\n") #

def fileChecker(self, notify = None): # Function used to check nitro codes from a file
    valid = [] # A list of the valid codes
    invalid = 0 # The amount of invalid codes detected
    with open(self.fileName, "r", encoding="utf-8") as file: # Open the file containing the nitro codes
        for line in file.readlines(): # Loop over each line in the file
            nitro = line.strip("\n") # Remove the newline at the end of the nitro code

            # Create the requests url for later use
            url = f"https://discordapp.com/api/v6/entitlements/gift-codes/{nitro}?with_application=false&with_subscription_plan=true"

            response = requests.get(url) # Get the responce from the url

            if response.status_code == 200: # If the responce went through
                print(f" Valid | {nitro} ") # Notify the user the code was valid
                valid.append(nitro) # Append the nitro code the the list of valid codes

                if notify is not None: # If a webhook has been added
                    DiscordWebhook( # Send the message to discord letting the user know there has been a valid nitro code
                        url = notify,
                        content = f"Valid Nito Code detected! @everyone \n{nitro}"
                    ).execute()
                else: # If there has not been a discord webhook setup just stop the code
                  break
                  #await ctx.send(f"{url} is Valid!!!!!!!") # Stop the loop since a valid code was found

            else: # If the responce got ignored or is invalid ( such as a 404 or 405 )
                print(f" Invalid | {nitro} ") # Tell the user it tested a code and it was invalid
                invalid += 1 # Increase the invalid counter by one

    return {"valid" : valid, "invalid" : invalid} # Return a report of the results

def quickChecker(self, nitro, notify = None): # Used to check a single code at a time
    # Generate the request url
    url = f"https://discordapp.com/api/v6/entitlements/gift-codes/{nitro}?with_application=false&with_subscription_plan=true"
    response = requests.get(url) # Get the response from discord

    if response.status_code == 200: # If the responce went through
        print(f" Valid | {nitro} ", flush=True, end="" if os.name == 'nt' else "\n") # Notify the user the code was valid
        with open("Nitro Codes.txt", "w") as file: # Open file to write
            file.write(nitro) # Write the nitro code to the file it will automatically add a newline

        if notify is not None: # If a webhook has been added
            DiscordWebhook( # Send the message to discord letting the user know there has been a valid nitro code
                url = notify,
                content = f"Valid Nito Code detected! @everyone \n{nitro}"
            ).execute()

        return True # Tell the main function the code was found

    else: # If the responce got ignored or is invalid ( such as a 404 or 405 )
        print(f" Invalid | {nitro} ", flush=True, end="" if os.name == 'nt' else "\n") # Tell the user it tested a code and it was invalid
        return False # Tell the main function there was not a code found

@client.event
async def on_ready():
    print("bot online")


@client.command()
async def mine(ctx, num):
  num = int(num)
  valid = [] # Keep track of valid codes
  invalid = 0 # Keep track of how many invalid codes was detected
  for i in range(num): # Loop over the amount of codes to check
    try: # Catch any errors that may happen
        code = "".join(random.choices( # Generate the id for the gift
            string.ascii_uppercase + string.digits + string.ascii_lowercase,
            k = 24
        ))
        url = f"https://discordgift.site/{code}" # Generate the url

        result = self.quickChecker(url, webhook) # Check the codes

        if result:
            await ctx.send(f" Valid Nitro Detected! | {url} ") # If the code was valid
            valid.append(url) # Add that code to the list of found codes
        else: # If the code was not valid
            invalid += 1 # Increase the invalid counter by one
    except Exception as e: # If the request fails
        invalid += 1
        await ctx.send(f"{i} | {url} ") # Tell the user an error occurred
  await ctx.send(f"""
Results:
 Valid: {len(valid)}
 Invalid: {invalid}
 Valid Codes: {', '.join(valid )}""")

keep_alive()



client.run(os.getenv("TOKEN"))
