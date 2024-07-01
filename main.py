from playwright.sync_api import sync_playwright


def screenshot_website(url):
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(url)
        page.screenshot(path=f'./screenshots/screenshot.png')
        browser.close()


screenshot_website('http://playwright.dev')
