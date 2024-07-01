from playwright.sync_api import sync_playwright
from urllib.parse import urlparse
import os
from openai import OpenAI
from dotenv import load_dotenv
import base64

load_dotenv()

client = OpenAI(
    # This is the default and can be omitted
    api_key=os.environ.get("OPENAI_API_KEY"),
)


def screenshot_from_url(url):
    domain = urlparse(url).netloc
    return f'./screenshots/screenshot-{domain}.png'


def screenshot_website(url):
    screenshot_path = screenshot_from_url(url)
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(url)
        page.screenshot(path=screenshot_path)
        browser.close()
    return screenshot_path


def analyze_website(screenshot_path):
    categories = open('categories.txt', 'r').read()
    screenshot_b64 = base64.b64encode(open(screenshot_path, 'rb').read()).decode('utf-8')

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": [
                    {
                        "type": "text",
                        "text": f"Please pick the most appropriate category from the following list:\n\n```\n{categories}\n```\n\nPlease only reply with the name of the category which best describes the site and nothing else."
                    }
                ]
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/png;base64,{screenshot_b64}"
                        }
                    }
                ]
            },
            {
                "role": "assistant",
                "content": [
                    {
                        "type": "text",
                        "text": "Computers Electronics and Technology > Programming and Developer Software"
                    }
                ]
            }
        ],
        temperature=1,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    return response.choices[0].message.content


urls = open('urls.txt', 'r').read().splitlines()

for url in urls:
    try:
        print(url, analyze_website(screenshot_website(url)))
    except:
        print(f"Failed to fetch {url}")
