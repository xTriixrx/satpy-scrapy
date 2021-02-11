import re
import os
from crawlers.satellite_crawler import SatelliteCrawler

class DSCOVR(SatelliteCrawler):
    """
    Concrete satellite spider class for DSCOVR which extends the base class, SatelliteCrawler.
    This method of splitting spiders into separate classes will help with keeping longevity of spider 
    runner classes and update issues easier that may occur during website HTML updates. This spider hierarchy
    requires using the Tor network and using the default settings (including ControlPort) to access the network.

    @author Vincent.Nigro
    @version 0.0.1
    @modified 2/10/21
    """

    IMG_FIELD = 'image'
    DATE_FIELD = 'date'
    DSCOVR_NATURAL = 'natural'
    DSCOVR_DIRECTORY = 'DSCOVR'
    DSCOVR_ENHANCED = 'enhanced'
    DSCOVR_URL = 'https://epic.gsfc.nasa.gov/api/'
    DSCOVR_ARCHIVE_URL = 'https://epic.gsfc.nasa.gov/archive/'

    def __init__(self, url, satellite):
        """
        A concrete constructor which accepts a full base path to a URL to begin crawl, satellite name, and
        an appropriate resolution size to search for during crawl process.
        
        @param url: str - A string containing a full URL path to some website to begin web crawl.
        @param satellite: str - A string containing a representative name for the DSCOVR satellite crawler.
        """

        super().__init__(url, satellite)


    def get_links(self, pw):
        """
        Implemented abstract public method which performs DSCOVR specific base page extraction and extraction
        of links from the appropriate containing objects.

        @param pw: str - A string containing the Tor password for the given system configuration.
        @return links: {} - A key-value mapping of a title key in a standard format and its appropriate image link.
        """

        links = {}
        
        # Get JSON response from each image page which provides latest images available
        natural_json = self._extract_content(self.get_url() + self.DSCOVR_NATURAL).json()
        enhanced_json = self._extract_content(self.get_url() + self.DSCOVR_ENHANCED).json()

        # Get links subsets containing key, value pairs for each set of JSON response
        natural_links = self.__generate_links_set(natural_json, self.DSCOVR_NATURAL)
        enhanced_links =  self.__generate_links_set(enhanced_json, self.DSCOVR_ENHANCED)
        
        # Merge individual dictionaries into one
        links = {**natural_links, **enhanced_links}
        
        return links


    def __generate_links_set(self, json_set, img_type):
        """
        Generates a subset of the final links dictionary by generating the title and link for each entry in a
        json subset of entries for some image type (either 'natural' or 'enhanced').

        @param json_set: [] - A list json entries for which each entry must have a key-value pair added to links.
        @param img_type: str - A string containing the type of image set being processed.
        @return links: {} A key-value mapping of a title key in a standard format and its appropriate image link.
        """

        links = {}

        for entry in json_set:
            img = entry[self.IMG_FIELD]
            date = entry[self.DATE_FIELD]
            
            title = self.__generate_title(img_type, date)
            link = self.__generate_link(img_type, date, img)
            links[title] = link
        
        return links


    def __generate_link(self, img_type, date, img):
        """
        Generates a link for a given entry by using the date field formatted as YYYY-MM-DD HH:MM:SS, an image
        title provided by NASAs' EPIC DSCOVR API, and the image type associated with that image title.

        @param img_type: str - A string containing the type of image being generated.
        @param date: str - A string containing a date field formatted as YYYY-MM-DD HH:MM:SS.
        @param img: str - A string containing a standard image title name which is provided by EPIC API.
        @return link: str - A generated link to retrieve a single image for the date, and img_type provided.
        """

        link = ''
        date_fields = date.split(' ')[0].split('-')

        link = self.DSCOVR_ARCHIVE_URL + '/' + img_type + '/' + date_fields[0] + '/' + date_fields[1] + '/' \
            + date_fields[2] + '/png/' + img + '.png'
        
        return link


    def _create_img_dir(self, title):
        """
        Protected abstract method implementation which is called during the base SatelliteCrawlers' pulldown_images
        method. This method is to generate the directory string path of where an image should be placed or already
        exists.

        @param title: str - A string containing the following standard format: 'TITLE - DATE - HH-MM UTC'
        which describes the image being queried.
        @return dir_path: str - A directory string containing the following standard format: 'DSCOVR/DATE/HH-MM UTC/TITLE'
        where the image downloaded should be placed, or already has been placed.
        """
        
        dir_path = ''
        
        today = re.split(self.TITLE_DELIMITER, title)[1]
        utctime = re.split(self.TITLE_DELIMITER, title)[-1].replace(':', '-')

        dir_path = self.DSCOVR_DIRECTORY + os.sep + str(today) + os.sep + utctime + os.sep + title
        
        return dir_path


    def __generate_title(self, img_type, date):
        """
        Using a date provided by the EPIC API, performs the necessary formatting to generate the standardized
        title format.
        
        @param img_type: str - A string containing the type of image being generated.
        @param date: str - A string containing a date field formatted as YYYY-MM-DD HH:MM:SS.
        @return title: str - A string containing the following standard format: 'TITLE - DATE - HH-MM UTC'
        """
        
        title = ''
        date_fields = date.split(' ')
        utc_fields = date_fields[1].split(':')

        title = img_type.capitalize() + ' Color - ' + date_fields[0] + ' - ' + utc_fields[0] + '-' \
            + utc_fields[1] + ' ' + self.UTC_STRING

        return title


    def create_satellite_directory(self):
        """
        Creates a high-level directory with the static DSCOVR_DIRECTORY string if it does not exist.
        """

        if not os.path.exists(self.DSCOVR_DIRECTORY):
            os.makedirs(self.DSCOVR_DIRECTORY)