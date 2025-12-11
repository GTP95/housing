import sys
import time
from playwright.sync_api import Playwright, TimeoutError
from debugprint import Debug
import json
from pathlib import Path

from helpers.config import USER_FIRST_NAME, USER_FULL_NAME

def delft(playwright: Playwright, already_reacted, headless) -> None:
    debug = Debug("housing:kamernet:delft")
    browser = playwright.chromium.launch(headless=headless)
    context = browser.new_context()   #using default Chrome ua doesn't help with login
    context.add_cookies(json.loads(Path("login/kamernet_cookies.json").read_text()))    #login with cookie
    page = context.new_page()

    # Go to https://kamernet.nl/en
    debug("Navigating to Kamernet's website")
    page.goto("https://kamernet.nl/en", wait_until="load")

    time.sleep(2)

    select_city(page, "Delft")

    time.sleep(5)
    announcements = page.locator(".MuiCardContent-root")  # .tile-new-advert  .rowSearchResultRoom
    count = announcements.count()
    print("Found " + str(count) + " potential listings in Delft")
    for index in range(count):
        with context.expect_page() as new_page_info:
            announcements.nth(index).click()
        new_page = new_page_info.value
        listing_url=new_page.url
        if listing_url in already_reacted.get_list():
            print("Already reacted, skipping")
            continue
        try:
            fill_contact_form(new_page,
                              f"Greetings,\nI'm {USER_FIRST_NAME} and I'm looking for a place to stay in Delft. \n"
                              f"Thank you for your availability,\n\n{USER_FULL_NAME}")
            already_reacted.addlisting(listing_url)
        except TimeoutError:
            print("Timeout while waiting for textarea, probably we need to update the button selector")
            print("Page URL: "+new_page.url)
        finally:
            new_page.close()

    context.close()
    browser.close()


def utrecht(playwright: Playwright, already_reacted, headless) -> None:
    browser = playwright.chromium.launch(headless=headless)
    context = browser.new_context()
    context.add_cookies(json.loads(Path("login/kamernet_cookies.json").read_text()))  # login with cookie
    page = context.new_page()

    # Go to https://kamernet.nl/en
    page.goto("https://kamernet.nl/en", wait_until="load")

    time.sleep(2)
    select_city(page, "Utrecht")
    time.sleep(5)
    announcements = page.locator(".MuiCardContent-root")  # .tile-new-advert  .rowSearchResultRoom
    count = announcements.count()
    print("Found " + str(count) + " potential listings in Utrecht")
    for index in range(count):
        with context.expect_page() as new_page_info:
            announcements.nth(index).click()
        new_page = new_page_info.value
        listing_url=new_page.url
        if listing_url in already_reacted.get_list():
            print("Already reacted, skipping")
            continue
        try:
            fill_contact_form(new_page,
                              f"Greetings,\nI'm {USER_FIRST_NAME} and I'm looking for a place to stay in Utrecht. \n "
                              f"I'm interested in this accommodation, please let me know if you need additional "
                              f"information from my side\nThank you for your availability,\n\n{USER_FULL_NAME}")
            already_reacted.addlisting(listing_url)
        except TimeoutError:
            print("Timeout while waiting for textarea, probably we need to update the button selector")
            print("Page URL: " + new_page.url)
        finally:
            new_page.close()

    context.close()
    browser.close()


def rotterdam(playwright: Playwright, already_reacted, headless: bool):
    browser = playwright.chromium.launch(headless=headless)
    context = browser.new_context()
    context.add_cookies(json.loads(Path("login/kamernet_cookies.json").read_text()))  # login with cookie
    page = context.new_page()

    # Go to https://kamernet.nl/en
    page.goto("https://kamernet.nl/en", wait_until="load")

    time.sleep(2)
    select_city(page, "Rotterdam")
    time.sleep(5)
    announcements = page.locator(".MuiCardContent-root")  # .tile-new-advert  .rowSearchResultRoom
    count = announcements.count()
    print("Found " + str(count) + " potential listings in Rotterdam")
    for index in range(count):
        with context.expect_page() as new_page_info:
            announcements.nth(index).click()
        new_page = new_page_info.value
        listing_url = new_page.url
        if listing_url in already_reacted.get_list():
            print("Already reacted, skipping")
            continue
        try:
            fill_contact_form(new_page,
                              f"Greetings,\nI'm {USER_FIRST_NAME} and I'm looking for a place to stay in Rotterdam. \n "
                              f"Thank you for your availability,\n\n{USER_FULL_NAME}")
            already_reacted.addlisting(listing_url)
        except TimeoutError:
            print("Timeout while waiting for textarea, probably we need to update the button selector")
            print("Page URL: " + new_page.url)
        finally:
            new_page.close()

    context.close()
    browser.close()



def login(page, email, password, context):
    page.get_by_role("link", name="Log in").click()
    page.get_by_role("link", name="Cookie-settings").click()
    page.get_by_role("button", name="Save settings").click()
    time.sleep(2)
    page.get_by_role("link", name="Log in").click()
    page.locator("#btnLoginEmail_inline div").first.click()
    page.get_by_placeholder("Email address").click()
    page.get_by_placeholder("Email address").fill(email)
    page.get_by_placeholder("Email address").press("Tab")
    page.get_by_role("textbox", name="Password").fill(password)
    time.sleep(5)
    page.get_by_role("button", name="Log in").click()
    page.wait_for_load_state("load")
    print("Per form login NOW!")
    time.sleep(30)
    cookies = context.cookies()
    Path("login/kamernet_cookies.json").write_text(json.dumps(cookies))


def select_city(page, city):
    debug=Debug("housing:kamernet:select_city")
    debug("Selecting city")
    page.get_by_label("City or postal code").click()

    match city:
        case "Delft":
            try:
                page.get_by_test_id("location-autocomplete").get_by_label("City or postal code").fill("delf")
                page.get_by_role("option", name="Delft").click()
                page.get_by_test_id("submit-button").click()
            except TimeoutError:
                debug("Timeout, manually triggering search by navigating to results page")
                page.goto("https://kamernet.nl/en/for-rent/rooms-delft?radius=5&minSize=2&maxRent=33&searchview=1")

        case "Utrecht":
            try:
                page.get_by_test_id("location-autocomplete").get_by_label("City or postal code").fill("utre")
                page.get_by_role("option", name="Utrecht").click()
                page.get_by_test_id("submit-button").click()
            except TimeoutError:
                debug("Timeout, manually triggering search by navigating to results page")
                page.goto("https://kamernet.nl/en/for-rent/rooms-utrecht?radius=1&minSize=2&maxRent=33&searchview=1")

        case "Rotterdam":
            try:
                page.get_by_test_id("location-autocomplete").get_by_label("City or postal code").fill("rott")
                page.get_by_role("option", name="Rotterdam", exact=True).click()
                page.get_by_test_id("submit-button").click()
            except TimeoutError:
                debug("Timeout, manual triggering search by navigating to results page")
                page.goto("https://kamernet.nl/en/for-rent/rooms-rotterdam?radius=1&minSize=2&maxRent=33&searchview=1")
        case _:
            print("City not defined", file=sys.stderr)

def fill_contact_form(page, message):
    debug = Debug("housing:kamernet:fill_contact_form")

    debug("Filling contact form")
    page.wait_for_load_state("load")
    # Click ton "Contact" button
    page.get_by_role("button", name="Contact landlord").nth(1).click()
    page.wait_for_load_state("load")

    # Fill text=Write a personal message... Custom message | Standard messageSend message >> textarea[name="Message"]
    page.locator("label").filter(has_text="Introduce yourself. Have").click()
    page.get_by_label("Introduce yourself. Have").fill(message)

    # Click #BtnSendMessage
    page.get_by_role("button", name="Send message").click()
    print("Message sent")
