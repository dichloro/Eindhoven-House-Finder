from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException
import time
import pandas as pd

class Initiation:
    """
    Initialize a web browser and configure parameters for web scraping.
    """

    def __init__(self, bedrooms=None, max_price=None, headless=True):
        """
        Get inputs of optional parameters for filtering scraping search results.
        Google Chrome is used as the browser for web scraping. Users can configure
        the number of bedrooms and the maximum rental price.

        Parameters:
            bedrooms (int): Number of bedrooms for filtering search results.
            max_price (int): Maximum price for filtering search results.
            headless (bool): Whether to run the browser in headless mode.
        """

        chrome_options = webdriver.ChromeOptions()
        if headless:
            chrome_options.add_argument('--headless')
        self.browser = webdriver.Chrome(options=chrome_options)
        self.bedrooms = bedrooms
        self.max_price = max_price

    def access_browser(self, url):
        """
        Access the rental website in the web browser.

        Parameters:
            url (str): The URL to access.
        """

        try:
            self.browser.get(url) # Retrieve HTML content
            time.sleep(2)  # Allow time for loading page elements
        except WebDriverException as e:
            return str(e)
        return None

    def close_browser(self):
        self.browser.quit()

    def get_num_page(self, page):
        """
        Get the total number of pages from the rental website that lists all the 
        houses with the filtered price and bedrooms.

        Parameters:
            page (list): List of web element representing the pagination elements.

        Returns:
            int: The total number of pages.
        """
        try:
            if not page:
                return 1 # When there is only one page of houses, the web element = [] or None
            else:
                return int(page[-2].text) # Total number of pages
        except Exception as e:
            return 1
    
class ScraperH2S(Initiation):
    """
    Extract house information from Holland2Stay website.
    """

    def extract_house_info(self):
        """
        Extract house information such as address, price, and link from the web page.

        Returns:
            DataFrame: DataFrame containing the extracted house information.
        """
        try:
            address_elements = self.browser.find_elements(By.CLASS_NAME, 'residence_name')
            price_elements = self.browser.find_elements(By.CLASS_NAME, 'price_text')

            addresses = [elem.text for elem in address_elements]
            prices = [elem.text.split()[0].replace('€', '').replace(',', '').split('.')[0] for elem in price_elements]
            links = [f'https://holland2stay.com/residences/{address.split(",")[0].replace(" ","-").lower()}.html' for address in addresses]

            df = pd.DataFrame({'Address': addresses, 'Price (€)': prices, 'Link': links})
            df['Source'] = 'Holland2Stay'

            return df, None
        except Exception as e:
            return None, str(e)

    def scrape(self):
        """
        Generate urls based on users' pre-defined filtering parameters, and initiate
        the scraping process and return the house information.

        Returns:
            DataFrame: DataFrame containing the extracted house information.
        """

        base_url = 'https://holland2stay.com/residences?page={}&available_to_book%5Bfilter%5D=Available+in+lottery%2C336&available_to_book%5Bfilter%5D=Available+to+book%2C179&city%5Bfilter%5D=Eindhoven%2C29'

        if self.bedrooms != None:
            if self.bedrooms == 1:
                # Studios and lofts are counted as 1 bedroom
                base_url +=  '&no_of_rooms%5Bfilter%5D=Studio%2C104' + '&no_of_rooms%5Bfilter%5D=Loft+%28open+bedroom+area%29%2C6137' + '&no_of_rooms%5Bfilter%5D=1%2C105'
            elif self.bedrooms == 2:
                base_url += '&no_of_rooms%5Bfilter%5D=2%2C106'
            elif self.bedrooms == 3:
                base_url += '&no_of_rooms%5Bfilter%5D=3%2C108'
            elif self.bedrooms == 4:
                base_url += '&no_of_rooms%5Bfilter%5D=4%2C382'

        if self.max_price != None:
            base_url += f'&price%5Bfilter%5D=0-{self.max_price}%2C0_{self.max_price}'
        
        self.access_browser(base_url.format(1))
        page = self.browser.find_elements(By.XPATH, '//*[@id="__next"]/div/section/div/div/div[4]/div/div[2]/ul/li')
        num_page = self.get_num_page(page)

        # Extract house data from all the pages
        error_messages = []
        house_info = pd.DataFrame()
        for i in range(num_page):
            url = base_url.format(i + 1)
            self.access_browser(url)
            error = self.access_browser(url)
            if error:
                error_messages.append(error)
                continue
            
            df, error = self.extract_house_info()
            if error:
                error_messages.append(error)
                continue

            if df is not None:
                house_info = pd.concat([house_info, df], ignore_index=True)
             
        self.close_browser()
        return house_info, error_messages
    
class ScraperPararius(Initiation):
    """
    Extract house information from Pararius website.
    """
    
    def extract_house_info(self):
        """
        Extract house information such as address, price, and link from the web page.

        Returns:
            DataFrame: DataFrame containing the extracted house information.
        """

        try:
            address_elements = self.browser.find_elements(By.CLASS_NAME, 'listing-search-item__title')
            price_elements = self.browser.find_elements(By.CLASS_NAME, 'listing-search-item__price')
            link_elements = self.browser.find_elements(By.CSS_SELECTOR, '.listing-search-item__link.listing-search-item__link--title')

            addresses = [(' '.join(elem.text.split()[1:]) + ', Eindhoven') for elem in address_elements]
            prices = [elem.text.split()[0].replace('€', '').replace(',', '').split('.')[0] for elem in price_elements]
            links = [elem.get_attribute('href') for elem in link_elements]

            df = pd.DataFrame({'Address': addresses, 'Price (€)': prices, 'Link': links})
            df['Source'] = 'Pararius'

            return df, None
        except Exception as e:
            return None, str(e)

    def scrape(self):
        """
        Generate urls based on users' pre-defined filtering parameters, and initiate
        the scraping process and return the house information.

        Returns:
            DataFrame: DataFrame containing the extracted house information.
        """

        base_url = 'https://www.pararius.com/apartments/eindhoven'

        if self.bedrooms != None:
            base_url += f'/{self.bedrooms}-bedrooms'
        
        if self.max_price != None:
            base_url += f'/0-{self.max_price}'
        
        self.access_browser(base_url)
        page = self.browser.find_elements(By.XPATH, '/html/body/div[3]/div[3]/div[5]/div/wc-pagination/ul/li')
        num_page = self.get_num_page(page)

        # Extract house data from all the pages
        error_messages = []
        house_info = pd.DataFrame()
        for i in range(num_page):
            url = base_url + f'/page-{i+1}'
            error = self.access_browser(url)
            if error:
                error_messages.append(error)
                continue
            
            df, error = self.extract_house_info()
            if error:
                error_messages.append(error)
                continue

            if df is not None:
                house_info = pd.concat([house_info, df], ignore_index=True)
            
        self.close_browser()
        return house_info, error_messages

class ScraperXior(Initiation):
    """
    Extract house information from Xior website. 
    This class does not consider getting the number of pages and filtering
    parameters because there are only a few houses listed on Xior,
    and users can not choose the number of bedrooms on the website.
    """

    def extract_house_info(self):
        """
        Extract house information such as address, price, and link from the web page.

        Returns:
            DataFrame: DataFrame containing the extracted house information.
        """

        try:
            address_elements = self.browser.find_elements(By.CLASS_NAME, 'address')
            price_elements = self.browser.find_elements(By.CSS_SELECTOR, '.price.pull-right')
            link_elements = self.browser.find_elements(By.CSS_SELECTOR, 'a.room')

            addresses = [(elem.text.lower().capitalize() + ', Eindhoven') for elem in address_elements]
            prices = [elem.text.lstrip('€ ') for elem in price_elements]
            links = [elem.get_attribute('href') for elem in link_elements]

            df = pd.DataFrame({'Address': addresses, 'Price (€)': prices, 'Link': links})
            df['Source'] = 'Xior'
            return df, None
        except Exception as e:
            return None, str(e)

    def scrape(self):
        """
        Generate the url, initiate the scraping process and return the house information.

        Returns:
            DataFrame: DataFrame containing the extracted house information.
        """

        url = 'https://www.xior.be/en/city/eindhoven'
        error = self.access_browser(url)
        error_messages = []

        if error:
            error_messages.append(error)
        
        house_info, error = self.extract_house_info()
        if error:
            error_messages.append(error)

        self.close_browser()
        return house_info, error_messages