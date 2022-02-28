import requests
from bs4 import BeautifulSoup

response = requests.get("https://vueuse.org/functions.html")
soup = BeautifulSoup(response.text, "html.parser")
function_details = soup.findAll("div", {"class": "whitespace-nowrap overflow-hidden overflow-ellipsis"})

function_data = []

for f in function_details:
    function = {}
    link = f.find("a", {"class": "rounded items-center"})
    browser_url = link["href"] if "https:" in link["href"] else f"https://vueuse.org{link['href']}"
    function["url"] = browser_url
    function["title"] = link.text
    function["subTitle"] = f.find("span", {"class": "overflow-hidden overflow-ellipsis"}).text.capitalize()
    function_data.append(function)
print(function_data)
