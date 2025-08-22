import requests
from bs4 import BeautifulSoup

url = "https://ayoub-etoullali.netlify.app/"
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

# Extract headings and paragraphs
info = [p.text for p in soup.find_all('p')]
print(info)
