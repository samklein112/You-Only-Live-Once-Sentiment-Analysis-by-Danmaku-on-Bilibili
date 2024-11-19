import requests
import pandas as pd
from lxml import etree

# Define the URL for the API request
url = "https://api.bilibili.com/x/v1/dm/list.so?oid=1523044575"

# Set up headers for the API request
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Connection": "keep-alive"
}
# Send the request
response = requests.get(url, headers=headers)
response.encoding = "utf-8"

# Parse the response to extract danmaku content
html_content = etree.fromstring(response.content)
danmakus = html_content.xpath("//d")

# Extract the attributes from the danmaku elements
data = []
for danmaku in danmakus:
    attr = danmaku.attrib['p'].split(',')
    data.append([
        attr[0],  # time in video
        attr[1],  # mode
        attr[2],  # size
        attr[3],  # color
        attr[4],  # timestamp
        attr[5],  # user ID
        attr[6],  # comment ID
        danmaku.text  # comment text
    ])

# Create a DataFrame from the extracted data
columns = ["time", "mode", "size", "color", "timestamp", "user_id", "comment_id", "text"]
df = pd.DataFrame(data, columns=columns)

# Save the DataFrame to a CSV file
df.to_csv("danmaku_data.csv", index=False, encoding='utf-8-sig')

print(f"Extracted {len(df)} comments.")

