import os
import json
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.llms import OpenAI

# Define the directory containing the text files
directory = "event_htmls"

# Define the output JSON file
output_file = "events.json"

# LangChain prompt template
prompt_template = """
You will be provided raw text as input. The text would contain information about biking events scraped from a website called BikeMonkey.

Your task is to extract the following attributes from given text into a valid JSON format. Ensure the output JSON is properly nested and adheres to the structure defined below:

### *Attributes to Extract:*  
1. *Event Details:*  
   - Event name  
   - Event location  
   - Event date  
   - Event host (organizer)  
   - Host base location  
   - Event attributes  

2. *Event Classification:*  
   - Type (e.g., fondo, race, multi-day tour)  
   - Surface (e.g., road, gravel, MTB)  

3. *Registration and Links:*  
   - Event registration (link)  
   - Event URL  

4. *Route Details:*  
   - Route(s) name  
   - Route(s) length  
   - Route(s) map trace  
   - Route(s) elevation  
   - Route(s) elevation profile  

### *JSON Output Format:*  

The extracted data should follow this structure:  

{
  "event": {
    "name": "<Event Name>",
    "location": "<Event Location>",
    "date": "<Event Date>",
    "host": "<Event Host>",
    "host_base_location": "<Host Base Location>",
    "attributes": "<Event Attributes>"
  },
  "classification": {
    "type": "<Type>",
    "surface": "<Surface>"
  },
  "registration": {
    "link": "<Event Registration Link>",
    "url": "<Event URL>"
  },
  "routes": [
    {
      "name": "<Route Name>",
      "length": "<Route Length>",
      "map_trace": "<Route Map Trace>",
      "elevation": "<Route Elevation>",
      "elevation_profile": "<Route Elevation Profile>"
    }
    // Additional routes can be added as separate objects
  ]
}

Handle missing data gracefully. If an attribute is not found, set its value to null in the JSON.

Input:
{input_text}

Output:
"""

# Initialize LangChain LLM
llm = OpenAI(temperature=0, model="GPT-4o mini")
prompt = PromptTemplate(template=prompt_template, input_variables=["input_text"])
chain = LLMChain(llm=llm, prompt=prompt)

# Function to process files and extract JSON
def process_files(directory):
    results = []
    for filename in os.listdir(directory):
        if filename.endswith(".txt"):
            file_path = os.path.join(directory, filename)
            with open(file_path, "r") as file:
                raw_text = file.read()
                # Get response from the LangChain chain
                response = chain.run(input_text=raw_text)
                try:
                    # Parse response to JSON
                    event_json = json.loads(response)
                    results.append(event_json)
                except json.JSONDecodeError as e:
                    print(f"Error decoding JSON for file {filename}: {e}")
    return results

# Process files and write to output
if __name__ == "__main__":
    extracted_data = process_files(directory)
    with open(output_file, "w") as json_file:
        json.dump(extracted_data, json_file, indent=4)
    print(f"Data has been extracted and saved to {output_file}.")
