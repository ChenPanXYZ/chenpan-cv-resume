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
***NOTE***: For email, you should use total.haddock08@icloud.com.
***NOTE***: Please remove my website.
***NOTE***: For the contact information section. My name must be centered. My location need to be in a seperate line, also centered. Other contact information should be in one line using this: <a href="mailto:total.haddock08@icloud.com">Email</a> | <a href="https://www.linkedin.com/in/chenpanxyz/">LinkedIn</a> | @ChenPanXYZ
***NOTE***: Add Canada Flag Emoji 🇨🇦 in the location section after "CANADA".
***NOTE***: Do not increase the font size of the title, location, and the contact information. The font size should be the same as the rest of the text.
***NOTE***: at the end, add the following code:
<!-- wp:heading -->
<h2 class="wp-block-heading">Disclaimer</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>GPT-4o-mini automatically generated this page. Please click <a href="https://chenpanxyz.github.io/chenpan-cv-resume/Chen-Pan-CV.pdf">here</a> to access the official CV in PDF format.</p>
<!-- /wp:paragraph --></div>
<!-- /wp:group --> 
***NOTE***: Please do not include the QR Code in the html code.
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