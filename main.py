#!/usr/bin/env python3

from playwright.sync_api import sync_playwright

from bjornd import Bjornd
from funda import Funda
from helpers.already_reacted import AlreadyReacted

with sync_playwright() as playwright:
    headless = False    #Requires xvfb. In this way I can get the correct url (workaround for Chromium bug)
    debug_mode=False
    already_reacted = AlreadyReacted()
    exit_code=0


    try:
        print("Looking on Funda")
        funda_instance = Funda(playwright, already_reacted, headless, debug_mode)
        print("Looking in Delft")
        funda_instance.delft()
        print("Looking in The Hague")
        funda_instance.the_hague()
        print("Looking in Rotterdam")
        funda_instance.rotterdam()
        funda_instance.close()

    except Exception as e:
        exit_code=1
        print("An error occurred, taking a screenshot and closing the browser")
        print(e)
        funda_instance.page.screenshot(path="error.png")
        funda_instance.close()
        print("Falling back to Bjornd")
        print("Looking on Bjornd")
        bjornd_instance = Bjornd(playwright, already_reacted, headless, debug_mode)
        bjornd_instance.delft_single()
        bjornd_instance.the_hague()


    finally:
        already_reacted.close()

print("DONE")
exit(exit_code)