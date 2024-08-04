import pandas as pd
from flask import Flask, render_template, request
import scraper
from geoservice import GeoService

class HouseFinder:
    """
    The HouseFinder calls two calsses geoservice and scraper to find houses and 
    retrieve related information.
    """

    def __init__(self, app):
        # Initialize the HouseFinder class with a flask application
        
        self.app = app
        self.setup_routes()

    def setup_routes(self):
        """
        Set up the routing for the flask application.
        """

        @self.app.route('/', methods=['GET', 'POST'])
        # The GET request displays the search form, while the POST request processes
        # the search form.

        def home():
            houses = None
            errors = None
            if request.method == 'POST':
                houses, errors = self.build_table()
            
            return render_template('search.html', houses=houses, errors=errors)

    def build_table(self):
        """
        Use the filtering parameters (could be undefined) to scrape house listings and compile 
        them into a table.
        
        Returns:
            tuple: A tuple containing the HTML representation of the DataFrame and any error messages.
        """

        bedrooms = request.form.get('bedrooms')
        max_price = request.form.get('max_price')
        
        h2s = scraper.ScraperH2S(bedrooms=bedrooms, max_price=max_price)
        pararius = scraper.ScraperPararius(bedrooms=bedrooms, max_price=max_price)
        xior = scraper.ScraperXior(bedrooms=bedrooms, max_price=max_price)

        # Retrieve house information
        h2s_info, err_h2s = h2s.scrape()
        pararius_info, err_pararius = pararius.scrape()
        xior_info, err_xior = xior.scrape()

        house_info = pd.concat([h2s_info, pararius_info, xior_info], ignore_index=True)

        # Calculate distance
        if not house_info.empty:
            calc_dist = GeoService(house_info)
            house_info = calc_dist.apply_coordinates_and_distance()
        else: 
            return None, 'No results found or error occurred'

        errors = ' '.join(filter(None, [err_h2s, err_pararius, err_xior]))    

        return house_info.to_html(classes='data', header="true"), errors

def create_app():
    app = Flask(__name__)
    HouseFinder(app)
    return app