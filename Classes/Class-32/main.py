import os
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

# Initialize the Gemini API client
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def generate_response(prompt, temperature=0.3):
    """Generate a response from Gemini API."""
    try:
        contents = [types.Content(role="user", parts=[types.Part.from_text(text=prompt)])]
        config_params = types.GenerateContentConfig(temperature=temperature)
        response = client.models.generate_content(
            model="gemini-2.0-flash", contents=contents, config=config_params)
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"

def run_activity():
    print("\n=== ZERO-SHOT, ONE-SHOT & FEW-SHOT LEARNING ACTIVITY ===\n")
    
    # Get user input
    category = input("Enter a category (e.g., animal, food, city): ")
    item = input(f"Enter a specific {category} to classify: ")
    
    # Zero-shot example
    print("\n--- ZERO-SHOT LEARNING ---")
    zero_shot = f"Is {item} a {category}? Answer yes or no."
    print(f"Prompt: {zero_shot}")
    print(f"Response: {generate_response(zero_shot)}")
    
    # One-shot example
    print("\n--- ONE-SHOT LEARNING ---")
    one_shot = f"""Determine if the item belongs to the category.
    
Example:
Category: fruit
Item: apple
Answer: Yes, apple is a fruit.

Now you try:
Category: {category}
Item: {item}
Answer:"""
    print(f"Response: {generate_response(one_shot)}")
    
    # Few-shot example
    print("\n--- FEW-SHOT LEARNING ---")
    few_shot = f"""Determine if the item belongs to the category.

Example 1:
Category: fruit
Item: apple
Answer: Yes, apple is a fruit.

Example 2:
Category: fruit
Item: carrot
Answer: No, carrot is not a fruit. It's a vegetable.

Example 3:
Category: vehicle
Item: bicycle
Answer: Yes, bicycle is a vehicle.

Now you try:
Category: {category}
Item: {item}
Answer:"""
    print(f"Response: {generate_response(few_shot)}")
    
    # Creative task with few-shot learning
    print("\n--- CREATIVE FEW-SHOT EXAMPLE ---")
    creative_prompt = f"""Write a one-sentence story about the given word.

Example 1: 
Word: moon
Story: The moon winked at the lovers as they shared their first kiss.

Example 2:
Word: computer
Story: The computer sighed as another cup of coffee was spilled on its keyboard.

Word: {item}
Story:"""
    print(f"Response: {generate_response(creative_prompt, temperature=0.7)}")
    
    # Reflection
    print("\n--- REFLECTION QUESTIONS ---")
    print("1. How did the responses differ between zero-shot, one-shot, and few-shot approaches?")
    print("2. Which approach gave the most helpful or accurate response?")
    print("3. How did the examples in the few-shot prompt influence the model's output?")

if __name__ == "__main__":
    run_activity()