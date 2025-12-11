import random
from math import pi
from time import sleep

import playwright
from debugprint import Debug

from helpers.MessageReader import MessageReader
from helpers.config import USER_PHONE

rd_sleep = lambda : random.randint(1,4)*random.random()*pi

class Funda:
    def __init__(self, playwright, already_reacted, headless=True, debug_mode=False):
        debug = Debug("housing:funda")
        debug("Debug print activated for Funda")
        self.playwright = playwright
        self.browser = playwright.chromium.launch(headless=headless)
        self.context = self.browser.new_context(storage_state="login/funda_context")
        self.page = self.context.new_page()
        self.already_reacted = already_reacted
        self.debug_mode = debug_mode
        self.message_reader = MessageReader("Resources/messages_generic.txt")

    def delft(self):
        self.page.goto("https://www.funda.nl/")
        self.page.get_by_role("button", name="Huur").click()
        self.page.get_by_test_id("search-box").click()
        self.page.get_by_test_id("search-box").fill("delft")
        self.page.get_by_role("option", name="Delft Gemeente in Zuid-Holland").click()
        sleep(2)
        self.page.get_by_role("button", name="Filters").click()
        self.page.get_by_test_id("FilterRangepriceMax").get_by_placeholder("Geen max").click()
        self.page.get_by_test_id("FilterRangepriceMax").get_by_text("€ 1.500").click()
        self.page.get_by_text("Woonhuis", exact=True).click()
        self.page.get_by_text("Appartement", exact=True).click()
        self.page.get_by_test_id("FilterPanelFooterButton").click()
        sleep(3)
        self.__iterate_over_listings()


    def the_hague(self):
        self.page.goto("https://www.funda.nl/")
        self.page.get_by_role("button", name="Huur").click()
        self.page.get_by_test_id("search-box").click()
        self.page.get_by_test_id("search-box").fill("den haag")
        self.page.get_by_role("option", name="Den Haag Gemeente in Zuid-").click()
        sleep(2)
        self.page.get_by_role("button", name="Filters").click()
        self.page.get_by_test_id("FilterRangepriceMax").get_by_placeholder("Geen max").click()
        self.page.get_by_test_id("FilterRangepriceMax").get_by_text("€ 1.500").click()
        self.page.get_by_text("Woonhuis", exact=True).click()
        self.page.get_by_text("Appartement", exact=True).click()
        self.page.get_by_test_id("FilterPanelFooterButton").click()
        sleep(3)
        self.__iterate_over_listings()

    def rotterdam(self):
        self.page.goto("https://www.funda.nl/")
        self.page.get_by_role("button", name="Huur").click()
        self.page.get_by_test_id("search-box").click()
        self.page.get_by_test_id("search-box").fill("rotterdam")
        self.page.get_by_role("option", name="Rotterdam Gemeente in Zuid-Holland").click()
        sleep(2)
        self.page.get_by_role("button", name="Filters").click()
        self.page.get_by_test_id("FilterRangepriceMax").get_by_placeholder("Geen max").click()
        self.page.get_by_test_id("FilterRangepriceMax").get_by_text("€ 1.500").click()
        self.page.get_by_text("Woonhuis", exact=True).click()
        self.page.get_by_text("Appartement", exact=True).click()
        self.page.get_by_test_id("FilterPanelFooterButton").click()
        sleep(3)
        self.__iterate_over_listings()


    def __iterate_over_listings(self):
        debug = Debug("housing:funda:iterate_over_listings")
        # Wait for the elements to be present
        selector="img.size-full"
        self.page.wait_for_selector(selector, timeout=10000)

        # Now try the specific selector
        announcements = self.page.locator(selector)
        count = announcements.count()
        print("Found " + str(count) + " potential listings")

        for index in range(count):
            with self.context.expect_page() as new_page_info:
                debug("Clicking on listing number: " + str(index))
                announcements.nth(index).click(button="middle")
                sleep(rd_sleep())
            debug("Getting new page URL")
            new_page = new_page_info.value
            new_page.wait_for_load_state()  # waits for the page to load
            listing_url = new_page.url

            if listing_url == "about:blank":
                raise Exception("Blank page")

            if listing_url in self.already_reacted.get_list():
                print("Already reacted, skipping")
                continue

            if self.debug_mode:
                self.__fill_contact_form_fake(new_page)
            else:
                try:
                    self.__fill_contact_form(new_page, self.message_reader.get_random_message())
                    sleep(rd_sleep())
                    if self.__form_sent_successfully(new_page):
                        self.already_reacted.addlisting(listing_url)
                except Exception as e:
                    print("Error, skipping")
                    debug("Error on page: " + listing_url)
                    debug("Here's the exception: " + str(e))
                    continue

    def __fill_contact_form_fake(self, page):
        pass

        #for index in range(count):
        #    announcement = announcements[index]
        #    price = announcement.get_by_text("€").inner_text()
        #    price = re.sub(r'\D', '', price)
        #    print(price)



    def __fill_contact_form(self, page, message):
        debug = Debug("housing:funda:fill_contact_form")
        page.get_by_role("link", name="Neem contact op").first.click()
        sleep(rd_sleep())
        page.get_by_placeholder("Stel je vraag aan de makelaar").click()
        page.get_by_placeholder("Stel je vraag aan de makelaar").fill(message)
        page.get_by_label("Ik wil een bezichtiging").check()
        sleep(rd_sleep())
        page.get_by_text("Ma", exact=True).click()
        page.get_by_text("Di", exact=True).click()
        page.get_by_text("Wo", exact=True).click()
        page.get_by_text("Do", exact=True).click()
        try:
            page.get_by_text("Za", exact=True).click()
        except playwright._impl._errors.TimeoutError:
            debug("No Saturday available")
        try:
            page.get_by_text("Zo", exact=True).click()
        except playwright._impl._errors.TimeoutError:
            debug("No Sunday available")
        try:
            page.get_by_text("'s avonds").click()
        except playwright._impl._errors.TimeoutError:
            debug("No evening available, trying morning")
            page.get_by_text("'s morgens").click()

        page.get_by_label("Telefoonnummer").click()
        page.get_by_label("Telefoonnummer").fill(USER_PHONE)
        page.get_by_role("button", name="Verstuur bericht").click()


    def __form_sent_successfully(self, page):
        if page.locator('h2.text-xl.font-semibold', has_text='Gelukt, je aanvraag is binnen').is_visible():
            print("Form sent successfully")
            return True
        print("Something went wrong with the form")
        return False

    def close(self):
        self.context.close()
        self.browser.close()