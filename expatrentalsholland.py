import time

from helpers.config import (USER_EMAIL, USER_PHONE, USER_FIRST_NAME, USER_LAST_NAME, 
                            USER_FULL_NAME, USER_ADDRESS_STREET, USER_ADDRESS_NUMBER, 
                            USER_ADDRESS_CITY)

class Expatrentalsholland:

    def __init__(self, playwright, already_reacted, headless=True):
        self.playwright = playwright
        self.already_reacted = already_reacted
        self.headless = headless
        self.browser = playwright.chromium.launch(headless=headless)
        self.context = self.browser.new_context()

    def delft(self):
        page = self.context.new_page()
        page.goto("https://www.expatrentalsholland.com/")
        page.get_by_placeholder("City or street").click()
        page.get_by_placeholder("City or street").fill("delft")
        page.locator("#ui-id-2").click()
        page.locator("#price_end").select_option("1250")
        page.get_by_role("button", name="Search now ").click()
        time.sleep(1)
        listings = page.locator(".pandlist > div")
        count=listings.count()
        print("Found "+str(count)+" potential listings in Delft")
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
                                  f"")
                self.already_reacted.addlisting(listing_url)
            except TimeoutError:
                print("Timeout while waiting for textarea, probably we need to update the button selector")
                print("Page URL: " + new_page.url)
            finally:
                new_page.close()

        self.context.close()
        self.browser.close()

    def __fill_contact_form(self, page, message):
        # Create initials from first name
        initials = '.'.join([name[0] for name in USER_FIRST_NAME.split()]) + '.'
        page.get_by_placeholder("Initials").click()
        page.get_by_placeholder("Initials").fill(initials)
        page.get_by_placeholder("Initials").press("Tab")
        page.get_by_placeholder("Lastname").fill(USER_LAST_NAME)
        page.get_by_placeholder("Address").click()
        page.get_by_placeholder("Address").fill(USER_ADDRESS_STREET)
        page.get_by_placeholder("Housenumber").click()
        page.get_by_placeholder("Housenumber").fill(USER_ADDRESS_NUMBER)
        page.get_by_placeholder("City").click()
        page.get_by_placeholder("City").fill(USER_ADDRESS_CITY)
        page.get_by_placeholder("Phone number").click()
        page.get_by_placeholder("Phone number").fill(USER_PHONE)
        page.get_by_placeholder("E-mail adress").click()
        page.get_by_placeholder("E-mail adress").fill(USER_EMAIL)


