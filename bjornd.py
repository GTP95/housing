import random
import time
from math import pi

from debugprint import Debug

from helpers.MessageReader import MessageReader
from helpers.config import USER_EMAIL, USER_PHONE, USER_FIRST_NAME, USER_LAST_NAME, USER_FULL_NAME

rd_sleep = lambda : random.randint(1,4)*random.random()*pi


def is_bart_hendriks(page):
    if "Hendriks" in page.locator('.gallery-contact-text').text_content():
        return True
    return False


def form_sent_successfully(page):
    if page.locator('.form-ajax-success').is_visible():
        print("Message sent")
        return True

    elif page.locator('.form-ajax-warning').is_visible():
        print("Detected as bot")
        return False
    else:
        print("Can't tell if message was sent")
        return False


def fill_contact_form(page, message, date_and_time):
    debug = Debug("housing:bjornd:fill_contact_form")
    debug("Filling contact form")
    page.get_by_placeholder("First name*").click()
    page.get_by_placeholder("First name*").fill(USER_FIRST_NAME)
    page.get_by_placeholder("First name*").press("Tab")
    page.get_by_placeholder("Surname*").fill(USER_LAST_NAME)
    page.get_by_placeholder("Surname*").press("Tab")
    page.get_by_placeholder("Email*").fill(USER_EMAIL)
    page.get_by_placeholder("Email*").press("Tab")
    page.get_by_placeholder("Telephone*").fill(USER_PHONE)
    page.get_by_placeholder("Your question").click()
    page.get_by_placeholder("Your question").fill(message)
    page.get_by_placeholder("Preference for date and time").click()
    page.get_by_placeholder("Preference for date and time").fill(date_and_time)
    page.locator("label").filter(has_text="I agree with the Privacy").locator("div").nth(1).click()
    time.sleep(rd_sleep())
    page.get_by_role("button", name="Send").click()


def fill_contact_form_fake(page):
    debug = Debug("housing:bjornd:fill_contact_form")
    debug("Filling contact form with fake data")
    page.get_by_placeholder("First name*").click()
    page.get_by_placeholder("First name*").fill("John")
    time.sleep(rd_sleep())
    page.get_by_placeholder("First name*").press("Tab")
    page.get_by_placeholder("Surname*").fill("Doe")
    time.sleep(rd_sleep())
    page.get_by_placeholder("Surname*").press("Tab")
    page.get_by_placeholder("Email*").fill("fake@example.com")
    page.get_by_placeholder("Email*").press("Tab")
    page.get_by_placeholder("Telephone*").fill("+06123456")
    page.get_by_placeholder("Your question").click()
    page.get_by_placeholder("Your question").fill("Hello guys")
    time.sleep(rd_sleep())
    page.get_by_placeholder("Preference for date and time").click()
    page.get_by_placeholder("Preference for date and time").fill("Sooner or later")
    page.locator("label").filter(has_text="I agree with the Privacy").locator("div").nth(1).click()
    time.sleep(rd_sleep())
    page.get_by_role("button", name="Send").click()


def filter_listings(page, city, accommodation_type, max_rent, min_rent="0"):
    page.get_by_placeholder("Search by address").click()
    page.locator("select[name=\"city\"]").select_option(city)
    page.get_by_text("Price: € 0 - No max.").nth(1).click()
    if min_rent != "0":
        page.locator("select[name=\"rentalsPriceMin\"]").select_option(min_rent)
    page.locator("select[name=\"rentalsPriceMax\"]").select_option(max_rent)
    page.locator("select[name=\"mainType\"]").select_option(accommodation_type)




class Bjornd:

    def __init__(self, playwright, already_reacted, headless=True, debug_mode=False):
        self.playwright = playwright
        self.already_reacted = already_reacted
        self.headless = headless
        self.browser = playwright.chromium.launch(headless=headless)
        self.context = self.browser.new_context()
        self.debug_mode=debug_mode
        debug = Debug("housing:bjornd")
        debug("Debug print activated for Bjornd")
        self.date_and_time = "Weekend any time, weekdays late in the afternoon, except Friday"
        self.message = f"""Greetings,
        
        I'm {USER_FIRST_NAME} and I'm interested in this accommodation. I'm a PhD student and my gross income is 2770€ per month.
        If my income is not enough to rent this property, my parents can guarantee for me.
        Please let me know if you need any additional information from me.
        Best regards,
        
        {USER_FULL_NAME}"""

        self.message_reader=MessageReader("Resources/messages_hendriks.txt")

        self.combinedMessage= """"""

    def delft_single(self):
        debug = Debug("housing:bjornd:delft_single")
        debug("Debugging delft_single")
        print("Looking in Delft")
        page = self.context.new_page()
        page.goto("https://www.bjornd.nl/")
        time.sleep(rd_sleep())
        # get rid of cookie dialog, just in case
        page.get_by_role("button", name="Alle cookies toestaan").click()
        page.get_by_role("navigation").locator("div").get_by_role("link").first.click()
        time.sleep(rd_sleep())
        page.get_by_role("link", name="Listings", exact=True).click()
        page.get_by_role("navigation").get_by_role("link", name="Rental listings").click()

        filter_listings(page, "Delft", "apartment", "1500")
        time.sleep(rd_sleep())
        self.iterate_over_listings(page)


    def the_hague(self):
        debug = Debug("housing:bjornd:the_hague")
        debug("Debugging the_hague")
        print("Looking in The Hague")
        page=self.navigate_to_listings()
        time.sleep(rd_sleep())
        filter_listings(page, "Den Haag", "apartment", "1500")
        time.sleep(rd_sleep())
        self.iterate_over_listings(page)

    def delft_combined(self):
        debug = Debug("housing:bjornd:delft_combined")
        debug("Debugging delft_combined")
        page = self.context.new_page()
        page.goto("https://www.bjornd.nl/")
        time.sleep(rd_sleep())
        #trying to get rid of cookie dialog here causes the whole program to crash if it isn't found. Not worth it.
        page.get_by_role("navigation").locator("div").get_by_role("link").first.click()
        time.sleep(rd_sleep())
        page.get_by_role("link", name="Listings", exact=True).click()
        page.get_by_role("navigation").get_by_role("link", name="Rental listings").click()

        filter_listings(page, "Delft", "apartment", "2000", "1500")

        time.sleep(rd_sleep())

        self.iterate_over_listings(page)

        #And now repeat for houses
        page = self.context.new_page()
        page.goto("https://www.bjornd.nl/")
        time.sleep(rd_sleep())
        page.get_by_role("navigation").locator("div").get_by_role("link").first.click()
        time.sleep(rd_sleep())
        page.get_by_role("link", name="Listings", exact=True).click()
        page.get_by_role("navigation").get_by_role("link", name="Rental listings").click()

        filter_listings(page, "Delft", "house", "2000", "1500")

        time.sleep(rd_sleep())

        self.iterate_over_listings(page)


    def navigate_to_listings(self):
        page = self.context.new_page()
        page.goto("https://www.bjornd.nl/")
        page.get_by_role("navigation").locator("div").get_by_role("link").first.click() #Language selection. Crucial for elements identified by text
        time.sleep(rd_sleep())
        page.get_by_role("link", name="Listings", exact=True).click()
        page.get_by_role("navigation").get_by_role("link", name="Rental listings").click()
        return page

    def iterate_over_listings(self, page):
        debug = Debug("housing:bjornd:iterate_over_listings")
        debug("Debugging iterate_over_listings")
        if page.locator('.alert').is_visible():
            print("No listings found")
            return
        announcements = page.locator("div.col-lg-3").filter(has_not_text="Rented")
        count = announcements.count()
        print("Found " + str(count) + " potential listings")

        for index in range(count):
            with self.context.expect_page() as new_page_info:
                debug("Clicking on listing number: " + str(index))
                announcements.nth(index).click(button="middle")
                time.sleep(rd_sleep())
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
                fill_contact_form_fake(new_page)
            elif is_bart_hendriks(new_page):
                fill_contact_form(new_page, self.message_reader.get_random_message(), self.date_and_time)
            else:
                fill_contact_form(new_page, self.message, self.date_and_time)

            time.sleep(2)

            if form_sent_successfully(new_page):
                self.already_reacted.addlisting(new_page.url)

            debug("Moving to next listing")


    def close(self):
        self.context.close()
        self.browser.close()