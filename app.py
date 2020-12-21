import logging
import time
import codecs

from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait

from infinite_scroll import InfiniteScroll

logging.basicConfig(level="DEBUG")
log = logging.getLogger(__name__)


def create_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--incognito")
    # options.add_argument("--headless")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")

    return webdriver.Chrome("chromedriver", options=options)


driver = create_driver()


def main():
    uri = "https://www.vivino.com/explore?e=eJwNyjEOgCAQBdHb_BoLy-28gbEyxqy4EhIBsxDQ20szzZugNCD4SAaBXxqNgf1om" \
          "WF7Jjxd3UWV1UvhG-kg5eKjyztXUXaCRKdki1bWrc-ZGv-DgRxE&cart_item_source=nav-explore"

    driver.get(uri)
    previous_height = driver.execute_script("return document.body.scrollHeight")
    stop = False
    iterations = 0

    while stop is False:
        try:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")

            # Wait for up to N seconds for scroll event.
            wait = WebDriverWait(driver, 3600)

            new_height = wait.until(InfiniteScroll(previous_height, log))
            previous_height = new_height

            # Pause
            time.sleep(1)
            log.debug(f"Content length: {len(driver.page_source)} bytes.")
            iterations = iterations + 1
            log.debug(f"Iterations: {iterations}")
        except Exception as ex:
            print("End of page reached")
            stop = True

    # Write page source to file
    with codecs.open("vivino_page_source.html", "w", "utf-8") as writer:
        writer.write(driver.page_source)


if __name__ == "__main__":
    main()
