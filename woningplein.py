import json
import time
from pathlib import Path


class WoningPlein:
    def __init__(self, playwright, already_reacted, headless=True):
        self.playwright = playwright
        self.already_reacted = already_reacted
        self.headless = headless
        self.browser = playwright.chromium.launch(headless=headless)
        self.context = self.browser.new_context()
        self.context.add_cookies(json.loads(Path("login/woning-plein_cookies.json").read_text()))  # login with cookie

    def delft(self):
        page=self.context.new_page()
        page.goto("https://www.woning-plein.nl")
        page.get_by_role("link", name="English").click()
        page.get_by_label("Place").click()
        time.sleep(1)
        page.get_by_label("Place").fill("Delft")
        time.sleep(1)
        page.get_by_label("Price").select_option("4")
        time.sleep(1)
        page.get_by_role("button", name="To search").click()
        time.sleep(5)
        listings = page.locator("div.col-xs-12")
        count = listings.count()
        print("Found " + str(count) + " potential listings in Delft")

        for index in range(count):

            listings.nth(index).click()
            new_page = page
            listing_url = new_page.url
            if listing_url in self.already_reacted.get_list():
                print("Already reacted, skipping")
                continue
            try:
                self.__fill_contact_form(new_page)
                self.already_reacted.add(listing_url)
            except TimeoutError:
                print("Timeout, maybe due to captcha")
                print("Page URL: " + new_page.url)


    def __fill_contact_form(self, page):
        page.get_by_role("link", name="Request viewing").click()
        time.sleep(2)
        page.locator(':has-text("Ik ben geen robot")').click()
        page.get_by_role("button", name="To steer").click()

