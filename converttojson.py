import json
import re

with open("scholarships.json", "r") as file:
    datajson = json.load(file)

regex = re.compile(r"https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)")
datajsonnew = []

for idx, data in enumerate(datajson):
    newdata = {
        **data,
        "link": "https://luarkampus.id" + regex.findall(data["long_description"])[0][1]
    }
    datajsonnew.append(newdata)

print(datajsonnew)
with open("scholarships.json", "w") as file:
    json.dump(datajsonnew, file, indent=4)