# llm_client.py
# ---------------------------------------------------------
# Wraps whichever LLM provider we're using, so every agent calls
# one simple ask_llm() function without knowing the provider details.
# Default: Groq, chosen for speed — it runs open models on custom
# chips (LPUs) that reply far faster than typical hosted LLM APIs,
# which matters here because one trip-planning request can trigger
# several LLM calls across different agents.
#
# To switch to Google Gemini instead, replace this whole file with:
#
#   import google.generativeai as genai
#   import os
#   genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
#   model = genai.GenerativeModel("gemini-1.5-flash")
#
#   def ask_llm(system_prompt: str, user_prompt: str) -> str:
#       full_prompt = f"{system_prompt}\n\n{user_prompt}"
#       response = model.generate_content(full_prompt)
#       return response.text
#
# Every agent that calls ask_llm(...) keeps working unmodified either way.
# ---------------------------------------------------------
from groq import Groq
from config import GROQ_API_KEY

# One shared client, created once when this module is first imported
client = Groq(api_key=GROQ_API_KEY)

# NOTE: Groq deprecated the llama-3.1-8b-instant / llama-3.3-70b-versatile
# models. openai/gpt-oss-20b is their current recommended small, fast model
# for general-purpose reasoning tasks like the ones in this project.
# If this ever 404s again, run the snippet at the bottom of this file to
# list every model your key currently has access to, and update this string.
MODEL_NAME = "openai/gpt-oss-20b"


def ask_llm(system_prompt: str, user_prompt: str) -> str:
    """
    Sends a system prompt (the agent's role/instructions) and a user
    prompt (the actual task) to the LLM, and returns the plain text reply.
    """
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.3,
        # lower temperature = more focused, consistent replies —
        # we want reliable short explanations, not creative writing
    )
    return response.choices[0].message.content
    # .choices[0] is the first (and only, since we didn't ask for more)
    # completion; .message.content is the actual text the model wrote


# ---------------------------------------------------------
# If MODEL_NAME above ever returns a 404 "model_not_found" error again,
# run this file directly (python llm_client.py) to print every model
# name your API key currently has access to, then update MODEL_NAME.
# ---------------------------------------------------------
if __name__ == "__main__":
    for m in client.models.list().data:
        print(m.id)
