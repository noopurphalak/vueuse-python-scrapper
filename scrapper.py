import json

import requests
from bs4 import BeautifulSoup

response = requests.get("https://vueuse.org/functions.html")
soup = BeautifulSoup(response.text, "html.parser")
function_sections = soup.findAll("h3", {"class": "!text-16px !tracking-wide !m-0"})
function_data = []

for f in function_sections:
    function_type = f.text.lower()
    next_sibling = f.next_sibling

    while (
        next_sibling
        and next_sibling.name == "div"
        and " ".join(next_sibling["class"]) == "whitespace-nowrap overflow-hidden overflow-ellipsis"
    ):
        function = {}
        link = next_sibling.find("a", {"class": "rounded items-center"})
        browser_url = link["href"] if "https:" in link["href"] else f"https://vueuse.org{link['href']}"
        function["url"] = browser_url
        function["title"] = link.text
        function["subTitle"] = next_sibling.find(
            "span", {"class": "overflow-hidden overflow-ellipsis"}
        ).text.capitalize()
        function["type"] = function_type
        function_data.append(function)
        try:
            next_sibling = next_sibling.next_sibling.next_sibling.next_sibling
            if next_sibling.name == "h3" and " ".join(next_sibling["class"]) == "!text-16px !tracking-wide !m-0":
                pass
            else:
                next_sibling = next_sibling.next_sibling
        except (Exception):
            next_sibling = None
print(json.dumps(function_data))
