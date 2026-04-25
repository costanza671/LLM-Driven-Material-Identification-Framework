"""
This function extracts crystallographic information from natural language using a language model.

Rule for space group handling:
-------------------------------------
The space group (symbol and number) must ONLY be provided when it is explicitly known or uniquely determined from the input description.

Definitions:
- space_group_symbol: Hermann–Mauguin notation (e.g. Fd-3m, Fm-3m)
- space_group_number: International space group number (1–230)

Guidelines:
- If the structure is unambiguous (e.g. "diamond structure"), include both symbol and number:
    e.g. diamond → Fd-3m (227)
- If the material or structure is ambiguous or depends on conditions not specified (e.g. "iron"), DO NOT guess:
    e.g. iron → could be bcc (Im-3m, 229) or fcc (Fm-3m, 225)
    in such cases return 'unknown' for space group fields

Notes: Space groups precisely describe crystal symmetry and cannot be approximated (guessing them can lead to incorrect scientific conclusions). Therefore, I want to restrict my outputs to known values.
"""

import json #JSON parsing utilities
import google.generativeai as genai #Library for accessing Google's Gemini language models


def llm_parse_material(text, api_key):
    """
    Parse natural language descriptions of materials into structured crystallographic data using Gemini. 
    Returns a dictionary containing the chemical formula and optional structural information. 
    This may include a prototype and space group when they are known or clearly implied.
    """

    # Configure the Gemini API with the provided key
    genai.configure(api_key=api_key)

    # Initialize the Gemini model (fast + lightweight version)
    model = genai.GenerativeModel("gemini-2.5-flash")

    # Impose JSON output and prevents the model from guessing missing data
    prompt = """
Return ONLY valid JSON with no extra text:

{
  "formula": "chemical formula (e.g. Si, GaN, Cu)",
  "structure": {
    "prototype": "graphite, diamond, fcc, bcc, perovskite, zincblende, etc. or unknown",
    "space_group_symbol": "Hermann–Mauguin notation (e.g. P6_3/mmc, Fd-3m) or unknown",
    "space_group_number": "integer space group number or unknown"
  }
}

Rules:
- Map element names to chemical symbols (silicon → Si)
- Only include space group data if it is clearly known or unambiguous
- Never guess or infer missing crystallographic information
- Use "unknown" when information is not explicitly provided
- Output must be valid JSON only, with no extra commentary
"""

    # Send the prompt + user input to the model
    response = model.generate_content(prompt + "\nInput: " + text)

    try:
        # Extract JSON safely from model output by locating the first '{' and last '}'
        start = response.text.find("{")
        end = response.text.rfind("}") + 1
        # Parse extracted substring into a Python dictionary
        return json.loads(response.text[start:end])

    except Exception as e:
        # Raise a clear error if the model output is not valid JSON
        raise ValueError(f"LLM returned invalid JSON: {response.text}") from e
