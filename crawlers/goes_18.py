import re
import os
from bs4 import BeautifulSoup 
from crawlers.satellite_crawler import SatelliteCrawler

class GOES_18(SatelliteCrawler):
    """
    Concrete satellite spider class for GOES-18 which extends the base class, SatelliteCrawler.
    This method of splitting spiders into separate classes will help with keeping longevity of spider
    runner classes and update issues easier that may occur during website HTML updates. This spider hierarchy
    requires using the Tor network and using the default settings (including ControlPort) to access the network.

    @author Vincent.Nigro
    @version 0.0.1
    @modified 8/12/22
    """

    GOES_18_RESOLUTIONS = ['339', '678', '1808', '5424', '10848', '21696']

    GOES_18_IMAGES = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13',
    '14', '15', '16', 'AirMass', 'DMW', 'DayCloudPhase', 'DayConvection', 'Dust', 'FireTemperature',
    'GEOCOLOR', 'NightMicrophysics', 'SWD', 'Sandwich']

    GOES_18_TITLES = ['Band 1', 'Band 2', 'Band 3', 'Band 4', 'Band 5', 'Band 6', 'Band 7', 'Band 8', 'Band 9',
    'Band 10', 'Band 11', 'Band 12', 'Band 13', 'Band 14', 'Band 15', 'Band 16', 'AirMass RGB',
    'Derived Motion Winds', 'Day Cloud Phase RGB', 'Day Convection RGB', 'Dust', 'Fire Temperature', 'GeoColor',
    'Nighttime Microphysics', 'Split Window Differential', 'Sandwich RGB']

    GOES_18_DIRECTORY = 'GOES-18'
    GOES_18_BASE_URL_EXTENSION = 'GOES18-ABI-FD'
    GOES_18_URL = 'https://cdn.star.nesdis.noaa.gov/GOES18/ABI/FD/'
    
    def __init__(self, url, satellite, resolution, image_types):
        """
        A concrete constructor which accepts a full base path to a URL to begin crawl, satellite name, and
        an appropriate resolution size to search for during crawl process.

        @param url: str - A string containing a full URL path to some website to begin web crawl.
        @param satellite: str - A string containing a representative name for the GOES-18 satellite crawler.
        @param resolution: int - An integer representation of a pixel resolution to search for in web crawler. 
        @param image_types: list - A list of image titles to compare during generation of links to reduce computation.
        """

        super().__init__(url, satellite)
        self.__resolution = resolution
        self.__image_types = image_types


    def get_links(self, pw):
        """
        Implemented abstract public method which performs GOES-18 specific base page extraction and extraction
        of links from the appropriate containing objects.

        @param pw: str - A string containing the Tor password for the given system configuration.
        @return links: {} - A key-value mapping of a title key in a standard format and its appropriate image link.
        """

        links = {}
        
        # If the resolution is not in the known set of resolutions, return an empty map
        if self.__resolution not in self.GOES_18_RESOLUTIONS:
            return links
        
        # For each image type, attempt to get the appropriate link for the desired resolution
        for i in range(0, len(self.GOES_18_IMAGES)):

            # If image types were provided, ensure we are not scraping pages for stuff that are not desired 
            if len(self.__image_types) > 0 and self.GOES_18_TITLES[i] not in self.__image_types:
                continue
            
            # Get the page for the provided full image page 
            page = self._extract_content(self.get_url() + self.GOES_18_IMAGES[i] + '/', pw)

            # Generate bs soup object and extract list of 'a' elements containing each image link
            soup = BeautifulSoup(page.text, self.SOUP_PARSER)
            a_elements = soup.findAll(self.A_ELEMENT, href=True)
            
            # Find latest link for resolution provided
            for a_element in reversed(a_elements):
                href = str(a_element[self.HREF_ATTRIBUTE])
                
                # If the extension base and the resolution is in the link, we found the latest link
                if self.GOES_18_BASE_URL_EXTENSION in href and self.__resolution in href and '.jpg' in href:
                    title = self.__generate_title(self.GOES_18_TITLES[i], href)
                    link = self.GOES_18_URL + self.GOES_18_IMAGES[i] + '/' + href
                    self._logger.info("Scraped link " + link + " for image " + title + ".")
                    links[title] = link
                    break

        return links


    def __generate_title(self, base_title, href):
        """
        Will generate a full title with the standard format of 'TITLE - DATE - HH-MM UTC'. An example would be
        'Band 1 - YYYY-MM-DD - 03-30 UTC'.

        @param base_title: str - A string representing the type of image: Ex: 'Band 1'.
        @param href: str - A string representing a link a partial link: Ex: 20222241750_GOES18-ABI-FD-01-10848x10848.jpg
        """
        title = ''
        date_info = href.split('_')[0] # In YYYYJJJHHMM format: 20222241750
        date = self._julian_to_date(date_info[:7])

        title = base_title + ' - ' + date.strftime('%Y-%m-%d') + ' - ' + \
            date_info[-4:-2] + '-' + date_info[-2:] + ' UTC'
        
        return title


    def _create_img_dir(self, title):
        """
        Protected abstract method implementation which is called during the base SatelliteCrawlers' pulldown_images
        method. This method is to generate the directory string path of where an image should be placed or already
        exists.

        @param title: str - A string containing the following standard format: 'TITLE - DATE - HH-MM UTC'
        which describes the image being queried.
        @return dir_path: str - A directory string containing the following standard format: 'GOES-18/DATE/HH-MM UTC/TITLE'
        where the image downloaded should be placed, or already has been placed.
        """

        dir_path = ""
        
        today = re.split(self.TITLE_DELIMITER, title)[1]
        utctime = re.split(self.TITLE_DELIMITER, title)[-1].replace(":", "-")

        dir_path = self.GOES_18_DIRECTORY + "/" + str(today) + "/" + utctime + "/" + title
        
        self._logger.debug("Image directory path for title " + title + ": " + dir_path + ".")
        
        return dir_path


    def create_satellite_directory(self):
        """
        Implemented public abstract method which creates a high-level directory with the static 
        GOES_18_DIRECTORY string if it does not exist.
        """

        if not os.path.exists(self.GOES_18_DIRECTORY):
            self._logger.debug("Creating directory at path: " + self.GOES_18_DIRECTORY)
            os.makedirs(self.GOES_18_DIRECTORY)


    def get_resolution(self):
        """
        Public accessor method for retrieving the private member containing the configured resolution
        for the current GOES-18 instance.
        """

        return self.__resolution