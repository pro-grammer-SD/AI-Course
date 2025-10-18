# 1. IMPORT necessary libraries:
#    - google.genai (for interacting with the Gemini API)
#    - config (for API key management)

# 2. DEFINE function generate_response(prompt, temperature=0.3):
#    - Initialize the genai client using the API key from config
#    - Create the content structure based on the user's prompt
#    - Configure the temperature and generate the response from Gemini API
#    - Return the response text

# 3. DEFINE function run_activity():
#    - PRINT introductory message explaining zero-shot, one-shot, and few-shot learning
#    - Step 1: Get user input for category and specific item (e.g., animal, food, city)
   
#    - Part 1: Zero-Shot Learning
#      - Generate a zero-shot learning prompt (e.g., "Is X a Y?")
#      - Display the AI's response to this prompt

#    - Part 2: One-Shot Learning
#      - Provide a one-shot learning prompt with a single example
#      - Display the AI's response to this one-shot prompt

#    - Part 3: Few-Shot Learning
#      - Provide a few-shot learning prompt with multiple examples
#      - Display the AI's response to the few-shot prompt

#    - Part 4: Creative Few-Shot Learning Example
#      - Create a creative prompt (e.g., a one-sentence story)
#      - Display the AI's creative response with a slightly higher temperature (0.7)

#    - Part 5: Reflection
#      - Ask reflection questions to encourage users to think about the differences between the learning approaches and the model's output

# 4. IF __name__ == "__main__":
#    - Call the run_activity() function to run the activity
