from geopy.geocoders import Nominatim
from geopy.distance import geodesic

class GeoService:
    """
    This class is used to handle geo-related tasks, such as getting 
    coordinates and calculating distances to a specific location.
    """

    def __init__(self, df):
        """
        Initialize the GeoService class with a house information
        DataFrame.

        Parameters: 
            df (DataFrame): The DataFrame that contains address information
        """
        self.df = df
        self.geolocator = Nominatim(user_agent="HouseFinder") # The geocoder object used for geocoding addresses.

    def get_coordinates(self, address):
        """
        Get the latitude and longitude coordinates for a given address.

        Parameters:
            address (str): The address for which to fetch coordinates.

        Returns:
             tuple: A tuple containing the latitude and longitude coordinates of the address.
             Returns None if coordinates cannot be retrieved.    
        """

        try:
            location = self.geolocator.geocode(address)
            if location:
                return (location.latitude, location.longitude)
            else:
                return (None, None)
        except Exception as e:
            return (None, None)

    def get_distance(self, coords): 
        """
        Calculate the distance between given coordinates and the Centraal Station.

        Parameters:
            coords (tuple): Coordinates containing the latitude and longitude coordinates.

        Returns:
            float: The distance in kilometers between the given coordinates and the station.
            Returns None if coordinates are invalid or missing.

        """
        
        station_coords = (51.4429623, 5.4795265) # Eindhoven Centraal Station coordinates
        
        if None not in coords:
            return round(geodesic(coords, station_coords).km,2)
        else:
            return None

    def apply_coordinates_and_distance(self):
        """
        Apply geocoding to the addresses in the DataFrame and calculate distances to the station.

        Returns:
            DataFrame:he original DataFrame with additional a column for distance.
        """

        self.df['Coordinates'] = self.df['Address'].apply(
            lambda address: self.get_coordinates(address))

        # Calculate distance to the station
        self.df['Distance to Eindhoven Centraal (km)'] = self.df['Coordinates'].apply(
            lambda coords: self.get_distance(coords))

        # Remove the unwanted column for house coordinates and adjust the order of columns
        self.df = self.df.drop(columns='Coordinates')
        distance = self.df.pop('Distance to Eindhoven Centraal (km)')
        self.df.insert(2, 'Distance to Eindhoven Centraal (km)', distance)

        return self.df
        