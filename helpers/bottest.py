import playwright


class BotTest():
    def __init__(self, headless=True):
        self.headless = headless
        self.browser = playwright.chromium.launch(headless=headless)
        self.context = self.browser.new_context(
        user_agent='Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36')