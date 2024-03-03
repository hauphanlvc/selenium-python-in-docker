from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import time


def create_webdriver(
    use_docker: bool = True, headless_mode: bool = True
) -> webdriver.Chrome | webdriver.Remote:
    """Creates a Chrome WebDriver instance with desired configurations.

    Args:
        use_docker: Whether to create the driver in a Docker environment.
        headless_mode: Whether to run Chrome in headless mode.

    Returns:
        A configured Chrome WebDriver instance.
    """

    chrome_options = Options()
    if headless_mode:
        chrome_options.add_argument("--headless")
        # pass

    if use_docker:
        driver = webdriver.Remote(
            command_executor="http://localhost:4444/wd/hub", options=chrome_options
        )
    else:
        driver = webdriver.Chrome(options=chrome_options)

    return driver


def main():
    # driver = create_webdriver(use_docker=False, headless_mode=False)
    driver = create_webdriver()
    driver.get("https://www.google.com")

    # Find the search input and enter a search term

    search_input = driver.find_element("name", "q")
    search_input.send_keys("example search term")
    search_input.send_keys(Keys.RETURN)

    # Print the page title
    print("Page title:", driver.title)

    # Quit the driver
    driver.quit()


if __name__ == "__main__":
    main()
