# from selenium import webdriver
from seleniumwire import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
from selenium.common.exceptions import NoSuchElementException
import itertools
import concurrent.futures


def create_webdriver(
    use_docker: bool = True,
    headless_mode: bool = True,
) -> webdriver.Chrome | webdriver.Remote:
    """Creates a Chrome WebDriver instance with desired configurations.

    Args:
        use_docker: Whether to create the driver in a Docker environment.
        headless_mode: Whether to run Chrome in headless mode.

    Returns:
        A configured Chrome WebDriver instance.
    """

    seleniumwire_options = {
        "auto_config": False,
    }

    chrome_options = Options()
    chrome_options.add_argument("--disable-dev-shm-usage")

    if headless_mode:
        chrome_options.add_argument("--headless")
        # pass

    if use_docker:
        driver = webdriver.Remote(
            command_executor="http://127.0.0.1:4444/wd/hub",
            options=chrome_options,
            # desired_capabilities=chrome_options.to_capabilities(),
            seleniumwire_options=seleniumwire_options,
        )
    else:
        driver = webdriver.Chrome(
            options=chrome_options, seleniumwire_options=seleniumwire_options
        )

    return driver


def get_class_details_giasudatviet(element):
    """Extracts the class details from the given element.

    Args:
        element: The element to extract the details from.

    Returns:
        A dictionary containing the class details.
    """

    details = {}
    for item in element.text.split("\n"):
        key, value = item.split(":")
        details[key.strip()] = value.strip()

    return details


def giasudatviet_scraping(giasudatviet_page_url) -> list:
    """Scraping for giasudatviet.com will return the available classes
    Args: None
    Returns:
        list the available classes
    """
    result = []
    # driver = create_webdriver(use_docker=False, headless_mode=False)
    driver = create_webdriver()
    while True:
        try:
            driver.get(giasudatviet_page_url)

            class_list = driver.find_element(
                By.CSS_SELECTOR,
                "body > div.wrapper > div.pageBody.clearfix > div.pageBodyInner.clearfix > div.col_c > div > div.newClass > div.class_list.clearfix",
            ).find_elements(By.CLASS_NAME, "item_c")
            for _class in class_list:
                info = _class.find_element(By.CSS_SELECTOR, "div.c_content.chuagiao")
                detailed_info_class = get_class_details_giasudatviet(info)
                detailed_info_class["url"] = _class.find_element(
                    By.CSS_SELECTOR, "div.social.clearfix > p > a"
                ).get_attribute("href")
                # print(detailed_info_class, "*"*10)
                result.append(detailed_info_class)

        except Exception as e:
            if e is NoSuchElementException:
                break

        break
    driver.quit()
    return result


def main():
    default_url = "https://giasudatviet.com/lop-day-can-gia-su.html?page=tim&keyword=&hinhthuc=&tinhthanh=701&quanhuyen=&trinhdo=0&gioitinh=&caphoc=0&monhoc=0&lophoc=10&p="
    urls = [default_url + str(i) for i in range(1, 11)]
    scraping_results = []

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []
        for url in urls:
            futures.append(
                executor.submit(giasudatviet_scraping, giasudatviet_page_url=url)
            )
        for future in concurrent.futures.as_completed(futures):
            scraping_results.append(future.result())

    return list(itertools.chain.from_iterable(scraping_results))


if __name__ == "__main__":
    start_time = time.time()
    print(main())
    print("--- %s seconds ---" % (time.time() - start_time))
