from google import genai

client = genai.Client(api_key="AIzaSyDkFQMFl1EmQPMCdyvvObz0VdvE91rVT5c")

response = client.models.generate_content(
    model="gemini-2.0-flash",
    contents="Explain how AI works",
)

with open("output.txt", "w") as file:
    file.write(response)

print(response)
