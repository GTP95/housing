import time

from helpers.config import USER_EMAIL, USER_PASSWORD, USER_FIRST_NAME, USER_FULL_NAME

#quasi fatto, hanno un limite sulle proprietà che si può chiedere di vedere, max 5
class Ikwilhuren:
    def __init__(self, playwright, already_reacted, headless=True):
        self.playwright=playwright
        self.already_reacted=already_reacted
        self.headless=headless
        self.browser = playwright.chromium.launch(headless=headless)
        self.context = self.browser.new_context()

    def __login(self):
        page = self.context.new_page()
        page.goto("https://ikwilhuren.nu/")
        page.get_by_role("button", name="Alle cookies toestaan").click()
        page.get_by_role("button", name="nl nl").click()
        page.get_by_role("link", name="en nl").click()
        page.locator("#layout-header").get_by_role("link", name="Login").click()
        page.get_by_label("Inloggen").get_by_label("E-mail address").click()
        page.get_by_label("Inloggen").get_by_label("E-mail address").fill(USER_EMAIL)
        page.get_by_label("Inloggen").get_by_label("E-mail address").press("Tab")
        page.get_by_label("Password").fill(USER_PASSWORD)
        page.get_by_role("button", name="Login").click()

    def delft(self):
        self.__login()
        page = self.context.new_page()
        page.goto("https://ikwilhuren.nu/")
        page.locator("#select2-selAdres-container").click()
        page.get_by_role("searchbox").fill("del")
        page.get_by_role("option", name="Gemeente Delft").click()
        page.get_by_role("button", name="Zoeken").click()
        time.sleep(2)
        listings=page.locator("div.col-sm-6")
        count=listings.count()
        print("Found {} potential listings in Delft".format(count))
        for index in range(count):
            with self.context.expect_page() as new_page_info:
                listings.nth(index).click()
            new_page = new_page_info.value
            listing_url = new_page.url
            if listing_url in self.already_reacted.get_list():
                print("Already reacted, skipping")
                continue
            try:
                self.__fill_contact_form(new_page,
                                  f"Greetings,\nI'm {USER_FIRST_NAME} and I'm looking for a place to stay in Delft. \nI'm interested in this accommodation, please let me know if you need additional "
                                  f"information from my side\nThank you for your availability,\n\n{USER_FULL_NAME}")
                self.already_reacted.addlisting(listing_url)
            except TimeoutError:
                print("Timeout while waiting for textarea, probably we need to update the button selector")
                print("Page URL: " + new_page.url)
            finally:
                new_page.close()

        self.context.close()
        self.browser.close()


    def __fill_contact_form(page, message):
        pass