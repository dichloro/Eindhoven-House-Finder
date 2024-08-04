# House Finder

House Finder is a web-based application designed to scrape and aggregate Eindhoven real estate listings from Dutch rental websites (Holland2Stay, Pararius, and Xior). It helps users find available properties that match specific preferences such as number of bedrooms and price range. This tool is particularly useful for people to find a house for rent in Eindhoven. Users can use this application without python installed.

## Features

- Scrape real estate listings from multiple sources.
- Filter properties by number of bedrooms and maximum price.
- Calculate the ditance between properties and the city center of Eindhoven (Centraal Station)
- Display results in a user-friendly web interface.

## Getting Started

### Prerequisites

To run on your local machine for development and testing purposes, you need these modules:

- Python 3.8 or newer
- flask
- selenium
- pandas
- geopy
- webbrowser

### Executing Program

Run the command below in Powershell: `python main.py`
Navigate to `http://127.0.0.1:5000` to access the web interface.

You can also directly run the executable: `./HouseFinder.exe`

### Searching for Houses

Use the web form to enter search preferences such as number of bedrooms and maximum price. Results will be displayed after clicking the search button.

## Notes and Limitations

The product only assists in searching for available houses, and users still need to manually register house visits through accessing the websites. Data extraction will be performed in compliance with the terms of use and copyright policies of the target websites.

It is crucial to use this scraper responsibly to avoid overloading the servers of the target websites. Frequent requests can be detected as anomalous activity, potentially leading to your IP address being blocked by the website. Also, Highly frequent searches may violate the terms of service of the websites being scraped.

When specifying the maximum price on the Holland2Stay website, the scraper may return listings that are slightly above the specified price range. This issue is caused from how prices are structured and displayed on the source website and is beyond the control of this application.

The feature to export results to an Excel file has not been implemented in the application. The reason is depending on the user's system settings and permissions, the application might not be allowed to write files to certain directories.

Currently, this application is designed to run only on Windows operating systems. 

## Future Improvements

- Reduce application size: It is possible to optimize the codebase and reduce dependencies, which will decrease the overall size of the application. This will help in making the installation process faster and require less storage space.

- Improve scraping efficiency: To reduce the time to scrape data from websites, it is better to implement multithreaded scraping techniques. This approach will allow the application to process multiple data streams concurrently so that it can minimize the wait times.

- Compatibility: Make the application compatible with macOS and Linux.