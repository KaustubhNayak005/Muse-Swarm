import os
from typing import Annotated
from groq import Groq

def generate_character_profile(
    theme: Annotated[str, "A brief theme or concept for the character, e.g., 'steampunk inventor' or 'rogue AI'."]
) -> str:
    """
    Generates a unique and detailed profile for a fictional character based on a theme by making a separate LLM call.

    Args:
        theme (str): The guiding theme for the character.

    Returns:
        str: A formatted string containing the character's unique name, backstory, and motivation.
    """
    print(f"--- DYNAMIC TOOL EXECUTED with theme: {theme} ---")

    # 1. Initialize the Groq client for this specific tool.
    #    It uses its own API key from the .env file.
    try:
        # Note: This uses the SPECIALIST key. You can use the same key as your main agents.
        client = Groq(api_key=os.environ.get("GROQ_API_KEY_SPECIALIST"))
    except Exception as e:
        return f"Error initializing Groq client for tool: {e}"

    # 2. Create a new, specific prompt for the specialist LLM.
    char_prompt = f"You are a character creation engine. Generate a single, detailed fictional character profile based ONLY on the following theme: '{theme}'. Include a unique name, a compelling backstory (2-3 sentences), and a clear motivation. Format the output with clear headings for 'Name', 'Backstory', and 'Motivation'."

    # 3. Make a separate, focused API call.
    try:
        # Here we use a specific model for the specialist task.
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": char_prompt,
                }
            ],
            model="qwen/qwen3-32b", # Using the 'reasoning' model as our specialist
        )
        character_profile = chat_completion.choices[0].message.content
        return f"--- Character Profile ---\n{character_profile}"
    
    except Exception as e:
        # If the API call fails, return a useful error message back to the agent.
        return f"An error occurred inside the character generator tool: {e}"