import subprocess

from playwright.sync_api import Playwright, TimeoutError

from helpers.already_reacted import AlreadyReacted
from helpers.email import Email
from helpers.config import USER_FULL_NAME


def getClipboardData():
    p = subprocess.Popen(['xclip', '-selection', 'clipboard', '-o'], stdout=subprocess.PIPE)
    retcode = p.wait()
    data = p.stdout.read()
    return data


def close_dialog(page):
    elements = page.locator("div[role=\"document\"] span i")
    try:
        elements.nth(0).click()  # the first element should be the button to close the popup
    except TimeoutError:  # problems getting
        page.go_back()


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context(storage_state="login/huurstunt.json")
    email_client = Email()
    alreadyreacted = AlreadyReacted()
    # Open new page
    page = context.new_page()
    # Go to https://www.huurstunt.nl/
    page.goto("https://www.huurstunt.nl/", timeout=60000)
    # Click [placeholder="Woonplaats"]
    page.locator("[placeholder=\"Woonplaats\"]").click()
    # Fill [placeholder="Woonplaats"]
    page.locator("[placeholder=\"Woonplaats\"]").fill("nijmegen")
    # Click text=NijmegenPlaats6
    page.locator("text=NijmegenPlaats").click()
    # Select 800
    page.locator("select[name=\"price_till\"]").select_option("800")
    # Click button:has-text("Zoeken")
    with page.expect_navigation():
        page.locator("button:has-text(\"Zoeken\")").click()
        page.wait_for_load_state("networkidle")  # needed otherwise doesn't find the listings

        # expect(page).to_have_url("https://www.huurstunt.nl/huren/nijmegen/0-800/")
        # ---------------------

        listings = page.locator(".link-container")
        count = listings.count()
        print("Found " + str(count) + " potential listings")
        for index in range(count):
            listings.nth(index).click()
            page.wait_for_load_state("networkidle")  # needed to reliably find the email address
            if page.url in alreadyreacted.get_list():  # go to the next listing if we already reacted on this one
                print("We already reacted on this listing")
                page.go_back()
                continue
            try:
                page.locator("text=Toon e-mailadres").click()
                page.wait_for_timeout(2000)
                page.locator("i.fa-copy").click()
                email_address = getClipboardData().decode("utf-8")  # convert from bytes to string
                message = f"Greetings,\nI'm {USER_FULL_NAME} and I'm interested in the property you posted " \
                          f"here: {page.url}.\n Please let me know any additional information you may need from me.\n Best regards,\n{USER_FULL_NAME}"
                email_client.send_message(email_address, "Property on Huurstunt", message)
                alreadyreacted.addlisting(page.url)
                page.go_back()
            except TimeoutError:
                close_dialog(page)
                print("Timeout while trying to get email address, probably a wild popup appeared")

    context.close()
    browser.close()
