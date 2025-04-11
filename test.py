from google import genai
import os

api_key = os.getenv("GEMINI_API")
client = genai.Client(api_key=api_key)

response = client.models.generate_content(
    model="gemini-2.0-flash",
    contents='''You are provided with a plaintext version of an income statement. Your task is to extract the relevant financial figures and convert the information into a formatted JSON file with the following hierarchy and fields:

    - **Revenue**
    - **Cost of Goods Sold**
    - **Gross Profit**
    - **Operating Expenses:**
    - Sales, General, & Administrative
    - Research & Development
    - Other Operating Expense
    - Total Operating Expenses
    - **Operating Profit**
    - **Net Interest Income**
    - **Other Non-Operating Income**
    - **Pre-Tax Income**
    - **Income Tax**
    - **Minority Interest**
    - **Other Non-recurring**
    - **Net Income**

    Assume that the plaintext may contain extra information such as headers, footers, notes, and additional details not needed for the JSON output. Your output should include only the above-listed fields, which may differ in wording in the plaintext, and you should ignore any extra data not relevant to these fields.''',
)

with open("output.txt", "w") as file:
    file.write(response)

print(response)
