import time
import csv
import os
from bs4 import BeautifulSoup as Bs4

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.webdriver import Service
from selenium.webdriver.common.by import By

def run():
    while True:
        service = Service(executable_path=ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service)

        def save_state(page, product):
            with open("waschraum/memory.txt", "w") as file:
                file.write(f"{page},{product}")

        def load_state():
            if os.path.exists("waschraum/memory.txt"):
                with open("waschraum/memory.txt", "r") as file:
                    state = file.read().split(',')
                    return int(state[0]), int(state[1])
            return 1, 0

        with open('waschraum/data.csv', 'w') as file:
            writer = csv.writer(file)
            writer.writerow((
                "Product Name",
                "Original Data Column 1 (Breadcrumb)",
                "Original Data Column 2 (Ausführung)",
                "Supplier Article Number",
                "EAN/GTIN",
                "Article Number",
                "Product Description",
                "Supplier",
                "Supplier-URL",
                "Product Image URL",
                "Manufacturer",
                "Original Data Column 3",
            ))

        driver.get('https://store.igefa.de/c/waschraum-hygiene/AycY6LWMba5cXn5esuFfRL')
        time.sleep(2)

        accept_cookies = driver.find_element(By.ID, 'CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll')
        accept_cookies.click()

        start_page, start_product = load_state()

        find_class_pages = driver.find_elements(By.CLASS_NAME, 'ant-pagination-item')
        get_last_page = int(find_class_pages[-1].get_attribute('title'))

        for i in range(start_page, get_last_page):
            driver.get(f'https://store.igefa.de/c/waschraum-hygiene/AycY6LWMba5cXn5esuFfRL?page={i}')
            time.sleep(2)
            elements = driver.find_elements(By.CSS_SELECTOR, '[data-testid="productCard_productName"]')
            x = start_product if i == start_page else 0


            def find_manufacturer(element):
                cells = element.find_all('td', class_='ant-table-cell')

                for i in range(len(cells)):
                    if "Hersteller" in cells[i].text:
                        return cells[i + 1].text.strip()

                return None

            while x < len(elements):
                try:
                    elements[x].click()
                    time.sleep(3)

                    src = driver.page_source
                    soup = Bs4(src, 'lxml')

                    product_name = soup.find('h1', {'data-testid': 'pdp-product-info-product-name'}).text.split(": ")[-1] or 'null'
                    original_data_column_1 = soup.find('span', class_='ant-typography CategoryBreadcrumbs_breadcrumb__e6d88').find('a').get('href') or 'null'
                    original_data_column_2 = soup.find('div', class_='ant-typography-secondary').text.split(": ")[-1] or 'null'
                    supplier_article_number = soup.find('div', {'data-testid': 'product-information-sku'}).text.split(": ")[-1] or 'null'
                    ean_gtin = soup.find('div', {'data-testid': 'product-information-gtin'}).text.split(": ")[-1] or 'null'
                    article_number = soup.find('div', class_='ProductInformation_variantInfo__5cb1d').text.split(': ')[-1] or 'null'
                    product_description = soup.find('div', class_='ProductDescription_description__4e5b7').find('p').get_text(separator=" ").strip() or 'null'
                    product_image_url = soup.find('img', {'class': 'image-gallery-image'}).get('src') or 'null'
                    supplier = 'igefa Handelsgesellschaft'
                    supplier_url = driver.current_url or 'null'
                    manufacturer = find_manufacturer(soup) or 'null'
                    original_data_column_3 = 'null'


                    with open('waschraum/data.csv', 'a') as file:
                        writer = csv.writer(file)
                        writer.writerow((
                            product_name,
                            original_data_column_1,
                            original_data_column_2,
                            supplier_article_number,
                            ean_gtin,
                            article_number,
                            product_description,
                            supplier,
                            supplier_url,
                            product_image_url,
                            manufacturer,
                            original_data_column_3
                        ))

                    print(f"{product_name} saved.")
                    save_state(i, x + 1)

                    driver.back()
                    time.sleep(2)
                    elements = driver.find_elements(By.CSS_SELECTOR, '[data-testid="productCard_productName"]')
                    x += 1
                except Exception as e:
                    print(e)
                    save_state(i, x)
                    break

        driver.quit()


