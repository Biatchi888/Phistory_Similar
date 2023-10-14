from typing import Any
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from pymongo import MongoClient
from datetime import datetime  # Import datetime module

# Your webdriver path and Chrome options
webdriver_path = r'C:\Users\jenne\Desktop\chromedriver_win32\chromedriver.exe'
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument(f"webdriver.chrome.driver={webdriver_path}")

# Connect to MongoDB
client = MongoClient('mongodb+srv://capstonesummer1:9Q8SkkzyUPhEKt8i@cluster0.5gsgvlz.mongodb.net/')
db = client['Product_Comparison_System']
collection = db['qwerty']

def scrape_product_price(url, product_id):
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)

    # Implement your scraping logic here to get the new price
    # For example, find the original and discounted price elements and extract the price values
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    original_price_element = soup.find('span', class_='woocommerce-Price-amount amount').find('bdi')
    original_price = original_price_element.text.strip() if original_price_element else ''

    # You can similarly scrape the discounted price if it's available on the page
 
    driver.quit()

    # Update the product in MongoDB with the new price and date scraped
    current_date = datetime.utcnow().isoformat()  # Get the current date in ISO format
    

    # Prepare the update data
    update_data = {
        "$set": {
            "original_price": original_price,
        },
        "$push": {
            "price_history": {
                "price": original_price,
                "date_scraped": current_date
            }
        }
    }

    # Update the product in MongoDB based on the product_id
    collection.update_one({"id": product_id}, update_data)

# URLs and corresponding product IDs
url_to_product_id = {
    'https://shopmetro.ph/marketmarket-supermarket/product/bear-brand-adult-plus-300g/': '64e089c6536ea90428262ad7',
    'https://shopmetro.ph/marketmarket-supermarket/product/gardenia-regular-slice-600g/': '64e08ca4536ea90428262cbc',
    'https://shopmetro.ph/marketmarket-supermarket/product/alaska-evaporated-filled-milk-370ml/': '64e089a2536ea90428262abd',
    'https://shopmetro.ph/marketmarket-supermarket/product/san-marino-corned-tuna-180g/': '64e0895a536ea90428262a9d',
    'https://shopmetro.ph/marketmarket-supermarket/product/silver-swan-soy-sauce-200ml/': '64e08d26536ea90428262cfd',
    'https://shopmetro.ph/marketmarket-supermarket/product/argentina-meat-loaf-150g/': '64e088b1536ea90428262a2e',
    'https://shopmetro.ph/marketmarket-supermarket/product/cdo-karne-norte-100g/': '64e088cd536ea90428262a3f',
    'https://shopmetro.ph/marketmarket-supermarket/product/lorins-gin-plastic-super-patis-350ml/': '64e08cea536ea90428262cdb',
    'https://shopmetro.ph/marketmarket-supermarket/product/zonrox-bleach-original-1l/': '64e08c8d536ea90428262cb2',
    'https://shopmetro.ph/marketmarket-supermarket/product/wilkins-distilled-water-1l/': '64e08cc7536ea90428262ccf',


}

# Loop through the URLs and scrape/update the prices
for url, product_id in url_to_product_id.items():
    scrape_product_price(url, product_id)













#puregold

from django.shortcuts import render
from typing import Any
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from pymongo import MongoClient
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from datetime import datetime


# Your webdriver path and Chrome options
webdriver_path = r'C:\Users\jenne\Desktop\chromedriver_win32\chromedriver.exe'
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument(f"webdriver.chrome.driver={webdriver_path}")

# Connect to MongoDB
client = MongoClient('mongodb+srv://capstonesummer1:9Q8SkkzyUPhEKt8i@cluster0.5gsgvlz.mongodb.net/')
db = client['Product_Comparison_System']
collection = db['discount']


def scrape_website_1(url, category):
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)

    SCROLL_PAUSE_TIME = 2
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(SCROLL_PAUSE_TIME)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    html_content = driver.page_source
    driver.quit()

    soup = BeautifulSoup(html_content, 'html.parser')

    # Extract title using the new XPath
    title_element = soup.find('h1', class_='page-title')
    title = title_element.text.strip() if title_element else ''

    # Extract image using the new XPath
    image_element = soup.find('div', class_='product media').find('img')
    image = image_element['src'] if image_element and 'src' in image_element.attrs else ''


    # Extract original price using the new XPath
    original_price_element = soup.find('span', class_='price-wrapper')
    original_price = original_price_element.find('span', class_='price').text.strip() if original_price_element else ''

    product_details = {
        'image': image,
        'title': title,
        'url': url,
        'category': category,
        'supermarket': 'Puregold',
        'original_price': original_price,
        'discounted_price': '',  # You can add code to extract discounted price if available
    }

    collection.insert_one(product_details)  # Save the data to MongoDB

    return product_details


def home(request):

    website_data = [
    
        {'url': "https://puregold.com.ph/index.php/pgcatalog/product/view/fcategory/Sally's%20Deals/title/MONDE%20CHEESE%20BAR%20%2023GX10S%20BUY%203%20PCS%20,%20GET%201%20PC%20FREE%20SAME%20VARIANT%20%20/barcode/8288998",
         'category': 'Bread'},
        {'url': "https://puregold.com.ph/index.php/pgcatalog/product/view/fcategory/Sally's%20Deals/title/MONDE%20BANANA%20BAR%2020GX10S%20BUY%203%20PCS%20,%20GET%201%20PC%20FREE%20SAME%20VARIANT%20%20/barcode/8288981",
         'category': 'Bread'},
         
        {'url': "https://puregold.com.ph/index.php/pgcatalog/product/view/fcategory/Sally's%20Deals/title/NESTLE%20ALL%20PURPOSE%20CREAM%20250ML%20BUY%205PCS%20FREE%20EDEN%20FILLED%20CHEESE%20160G%201PC%20%20/barcode/8248862",
         'category': 'Milk'},
        {'url': "https://puregold.com.ph/index.php/pgcatalog/product/view/fcategory/Sally's%20Deals/title/MILO%20REGULAR%20ACTIV-GO%20WINNER%201KG%20%20/barcode/4800361418058",
         'category': 'Milk'},
         
        {'url': "https://puregold.com.ph/index.php/pgcatalog/product/view/fcategory/Sally's%20Deals/title/NESTLE%20CHUCKIE%20CHUCKIE%20110MLX6S%20BUY%202%20PACKS%20%20/barcode/8274380",
         'category': 'Milk'},
        {'url': "https://puregold.com.ph/index.php/pgcatalog/product/view/fcategory/Sally's%20Deals/title/BEAR%20BRAND%20FORTIFIED%20RECONSTITUTED%20MILK%20DRINK%20110ML%20BUY%203%20PCS%20%20@%20P40%20%20/barcode/8233240",
         'category': 'Milk'},

        {'url': "https://puregold.com.ph/index.php/pgcatalog/product/view/fcategory/Sally's%20Deals/title/NESTLE%20CHUCKIE%20CHUCKIE%20110MLX6S%20BUY%202%20PACKS%20%20/barcode/8274380",
         'category': 'Milk'},
        {'url': "https://puregold.com.ph/index.php/pgcatalog/product/view/fcategory/Sally's%20Deals/title/BEAR%20BRAND%20STERILIZED%20MILK%201L%20BUY%202%20PCS%20%20/barcode/8271396",
         'category': 'Milk'},

        {'url': "https://puregold.com.ph/index.php/pgcatalog/product/view/fcategory/Sally's%20Deals/title/NESTLE%20CHUCKIE%20CHUCKIE%20110MLX6S%20BUY%202%20PACKS%20%20/barcode/8274380",
         'category': 'Milk'},
        {'url': "https://puregold.com.ph/index.php/pgcatalog/product/view/fcategory/Sally's%20Deals/title/BEAR%20BRAND%20STERILIZED%20MILK%201L%20BUY%202%20PCS%20%20/barcode/8271396",
         'category': 'Milk'},

        {'url': "https://puregold.com.ph/index.php/pgcatalog/product/view/fcategory/Sally's%20Deals/title/BEAR%20BRAND%20STERILIZED%20200ML%20BUY%205%20PCS%20%20/barcode/8286772",
         'category': 'Milk'},
        {'url': "https://puregold.com.ph/index.php/pgcatalog/product/view/fcategory/Sally's%20Deals/title/WILKINS%20PURE%20500ML%20BUY%206%20PCS%20%20/barcode/8286864",
         'category': 'Water'},
         
        {'url': "https://puregold.com.ph/index.php/pgcatalog/product/view/fcategory/Sally's%20Deals/title/BEAR%20BRAND%20FORTIFIED%20POWDERED%20MILK%20DRINK%2033GX8S%20BUY%202%20TIES%20+%201%20TIE%20NESCAFE%20CREAMY%20WHITE%203%20IN%201%20TWIN%20PACK%2051GX10S%20%20/barcode/8286789",
         'category': 'Milk'},
        {'url': "https://puregold.com.ph/index.php/pgcatalog/product/view/fcategory/Sally's%20Deals/title/BEAR%20BRAND%20FORTIFIED%20POWDERED%20MILK%20DRINK%20WITH%20IRON%20&%20ZINC%20PLAIN%201.9KG%20BUY%201%20PACK%20,%20GET%20FREE%20%201%20PACK%20BEAR%20BRAND%20FORTIFIED%20POWDERED%20MILK%20DRINK%20WITH%20IRON%20&%20ZINC%20PLAIN%20680G%20%20/barcode/8286796",
         'category': 'Milk'},

        {'url': "https://puregold.com.ph/index.php/pgcatalog/product/view/fcategory/Sally's%20Deals/title/NESCAFE%20CLASSIC%20STICKS%201.9GX48S%20BUY%201%20PACK%20+%201%20PACK%20NESTLE%20COFFEE%20MATE%20ORIGINAL%2048SX5G%20,%20SAVE%20P25%20%20/barcode/8286819",
         'category': 'Coffee'},
        {'url': "https://puregold.com.ph/index.php/pgcatalog/product/view/fcategory/Sally's%20Deals/title/MILO%20ACTIV-GO%20WINNER%20REGULAR%201KG%20BUY%202%20PACKS%20,%20GET%20FREE%20%201%20PACK%20MY%20SAN%20FITA%20CRACKERS%20SINGLES%2030GX10S%20%20/barcode/8286833",
         'category': 'Milk'},

        {'url': "https://puregold.com.ph/index.php/pgcatalog/product/view/fcategory/Sally's%20Deals/title/BREEZE%20ACTIVBLEACH%20ECOCLEAN%20TECHNOLOGY%20LAUNDRY%20POWDER%20DETERGENT%20%201410G%20POUCH%20%20/barcode/4800888180414",
         'category': 'Laundry Aids'},
        {'url': "https://puregold.com.ph/index.php/pgcatalog/product/view/fcategory/Sally's%20Deals/title/SURF%20ROSE%20FRESH%20LAUNDRY%20LIQUID%20DETERGENT%202.5L%20POUCH%20%20/barcode/8934868158561",
         'category': 'Laundry Aids'},
         
        {'url': "https://puregold.com.ph/index.php/pgcatalog/product/view/fcategory/Sally's%20Deals/title/SURF%20CHERRY%20BLOSSOM%20LAUNDRY%20LIQUID%20DETERGENT%202.5L%20POUCH%20%20/barcode/8934868158547",
         'category': 'Laundry Aids'},
        {'url': "https://puregold.com.ph/index.php/pgcatalog/product/view/fcategory/Sally's%20Deals/title/BREEZE%20POWER%20MACHINE%20LIQUID%20LAUNDRY%20DETERGENT%203L%20BUY%201%20PC%20,%20GET%20FREE%201%20DOMEX%20MULTI-PURPOSE%20CLEANER%20CLASSIC%20250ML%20BOTTLE%20%20/barcode/8303066",
         'category': 'Laundry Aids'},

        {'url': "https://puregold.com.ph/index.php/pgcatalog/product/view/fcategory/Sally's%20Deals/title/SURF%20LAUNDRY%20DETERGENT%20POWDER%20BLOSSOM%20FRESH%207KG%20BUY%201%20PC%20,%20GET%20FREE%201%20SURF%20FABRIC%20CONDITIONER%20LUXE%20PERFUME%20POUCH%20670ML%20%20/barcode/8303059",
         'category': 'Laundry Aids'},
        {'url': "https://puregold.com.ph/index.php/pgcatalog/product/view/fcategory/Sally's%20Deals/title/SURF%20LAUNDRY%20DETERGENT%20POWDER%20BLOSSOM%20FRESH%207KG%20BUY%201%20PC%20,%20GET%20FREE%201%20SURF%20FABRIC%20CONDITIONER%20BLOSSOM%20FRESH%20670ML%20%20/barcode/8303042",
         'category': 'Laundry Aids'},

    
    ]
    
   

    product_details_list = []
    for website in website_data:
            category = website['category']
            product_details = scrape_website_1(website['url'], category)
            product_details_list.append(product_details)

    context = {
            'product_details_list': product_details_list,
        }
    return render(request, 'compare.html', context)