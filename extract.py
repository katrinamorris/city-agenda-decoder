import re

def extract_resolutions(file_path):
    """
    Reads a raw text file of a city agenda, searches for individual resolutions,
    and returns them as a list of cleaned strings.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
        return []

    # REGEX BREAKDOWN:
    # (?i)             -> Case-insensitive matching (matches "A RESOLUTION OF" or "A resolution of")
    # \bA\s+RESOLUTION\s+OF\b -> Matches the literal starting phrase, accounting for variable spacing
    # (.*?)            -> Non-greedy capture group; grabs all text up until...
    # (?=(?:\bA\s+RESOLUTION\s+OF\b|\Z)) -> A positive lookahead. It stops capturing when it sees 
    #                                      the next resolution start OR the end of the file (\Z).
    pattern = re.compile(r'(?i)\bA\s+RESOLUTION\s+OF\b(?P<resolution_text>.*?)(?=(?:\bA\s+RESOLUTION\s+OF\b|\Z))', re.DOTALL)
    
    matches = pattern.finditer(content)
    resolutions = []
    
    for i, match in enumerate(matches, 1):
        # Re-attach the starting phrase and clean up extra whitespace/newlines
        text = match.group('resolution_text').strip()
        full_resolution = f"A RESOLUTION OF {text}"
        
        # Collapse multiple internal consecutive newlines/spaces for readability
        cleaned_text = re.sub(r'\s+', ' ', full_resolution)
        
        resolutions.append(cleaned_text)
        
    return resolutions

# --- Example Usage ---
if __name__ == "__main__":
    # Simulate a raw text file layout
    dummy_agenda_data = """
    CITY OF MIAMI AGENDA PACKET - JUNE 2026
    Item 1. Roll Call
    Item 2. Approvals
    
    A RESOLUTION OF THE MIAMI CITY COMMISSION, WITH ATTACHMENT(S), 
    APPROVING THE CITY MANAGER'S AWARD RECOMMENDATION FOR RFP NO. 2046386 
    TO STAR CONTROLS, INC. PROVIDING FOR EFFECTIVE DATE.
    
    Discussion on Item 2 follows here. Some miscellaneous text.
    
    a resolution of the miami city commission, by a 4/5ths vote,
    ratifying an emergency contract with Waste Management Inc.
    
    End of agenda text.
    """
    
    # Save dummy data to test the script
    test_filename = "test_agenda.txt"
    with open(test_filename, "w", encoding="utf-8") as f:
        f.write(dummy_agenda_data)
        
    # Run the extractor
    extracted = extract_resolutions(test_filename)
    
    print(f"Successfully extracted {len(extracted)} resolutions:\n")
    for idx, res in enumerate(extracted, 1):
        print(f"--- RESOLUTION #{idx} ---")
        print(res)
        print("\n")
