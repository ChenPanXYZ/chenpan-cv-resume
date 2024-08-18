from openai import OpenAI
from config import model, api_key
client = OpenAI(api_key=api_key)
import json
# read Chen-Pan-CV.tex.

try:
    with open("Chen-Pan-CV.tex", "r") as f:
        tex = f.read()

    the_message = f"""
Please generate a WordPress code for a WordPress post based on the latex below.
Note that I need to preserve the formatting of the LaTeX file as much as possible, and all the information including the contact information.
Latex:
{tex}
Please put the wordpress code in "wordpress_code".
Your response should be ready to copy and paste into a WordPress post. Never ever wrap the code in a code block (i.e., ```).

***NOTE***: Every section should be seperated by a horizontal line.
***NOTE***: Please remove my phone number.
***NOTE***: For email, you should use scrips_isolate.02@icloud.com.
***NOTE***: Please remove my website.
***NOTE***: For the contact information section. My name should be centered. My location should be in one line centerted. Email, LinkedIn, and GitHub should be in one line centered.
***NOTE***: Add Canada Flag Emoji 🇨🇦 in the location section after "CANADA".
"""
    
    completion = client.chat.completions.create(
    model = model,
    messages=[
        {
            "role": "user",
            "content": the_message,
        }
    ],
    response_format={
        "type": "json_schema",
        "json_schema": {
            "name": "response",
            "strict": True,
            "schema": {
                "type": "object",
                "properties": {
                    "wordpress_code": {
                        "type": "string",
                        "description": "The wordpress code"
                    },
                },
                "required": ["wordpress_code"],
                "additionalProperties": False,
            },
        },
    },
    temperature = 0,
    )
    response = completion.choices[0].message
    response = response.content
    response = json.loads(response)
    wordpress_code = response["wordpress_code"]

    # write the WordPress code to a file.
    with open("online_version.txt", "w") as f:
        f.write(wordpress_code)
    

except FileNotFoundError:
    print("File not found.")