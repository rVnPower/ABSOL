import requests
from bs4 import BeautifulSoup
import json

# We will parse the data from VnExpress.

# Here we get the response from one of their articles.
response = requests.get("https://vnexpress.net/20-000-hoc-sinh-tp-hcm-se-truot-lop-10-cong-lap-4461594-p3.html")

# Check if the website is available
# print(response.status_code)

# Get the response's content
src = response.content

soup = BeautifulSoup(src, "lxml")
table = soup.find_all("td")[5:]

tree = {}
school = {}
current_district = ""

def assignKey(status):
    states = ["index", "name", "regLimit", "regTotal"]
    return states[status]

# Hard-coded value to check for something
status = 0

for element in table:
    buffer = ""

    # 'contents' function returns a list so we get the first element
    content = element.contents[0]

    try:
        content = content.contents[0] + '\n'
        buffer = '\n'
        status = -1
        current_district = content.strip()
        # print(content)
        tree[current_district] = []
    except AttributeError:
        # We do not need empty strings
        if content.strip() == "":
            continue

        key = assignKey(status)
        school[key] = content.strip()

        if status == 3:
            status = -1
            content += '\n'
            tree[current_district].append(school)
            school = {}
    
    # Output if you wanted to
    print(buffer + content, end=" ")
    status += 1 

# Dump the data to a .json file
with open("data.json", "w") as f:
    json.dump(tree, f)

