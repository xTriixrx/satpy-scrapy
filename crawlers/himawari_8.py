import re
import os
from bs4 import BeautifulSoup 
from crawlers.satellite_crawler import SatelliteCrawler

class HIMAWARI_8(SatelliteCrawler):
    """
    Concrete satellite spider class for HIMAWARI-8 which extends the base class, SatelliteCrawler.
    This method of splitting spiders into separate classes will help with keeping longevity of spider 
    runner classes and update issues easier that may occur during website HTML updates. This spider hierarchy
    requires using the Tor network and using the default settings (including ControlPort) to access the network.

    @author Vincent.Nigro
    @version 0.0.1
    @modified 1/24/21
    """

    ARCHIVE_TEXT = '4 Wk Archive'
    HIMAWARI_8_DIRECTORY = 'HIMAWARI-8'
    HIMAWARI_8_BASE_LINK = 'http://rammb.cira.colostate.edu/ramsdis/online/'
    HIMAWARI_8_URL = 'http://rammb.cira.colostate.edu/ramsdis/online/himawari-8.asp'
    
    def __init__(self, url, satellite):
        """
        A concrete constructor which accepts a full base path to a URL to begin crawl, satellite name, and
        an appropriate resolution size to search for during crawl process.
        
        @param url: str - A string containing a full URL path to some website to begin web crawl.
        @param satellite: str - A string containing a representative name for the HIMAWARI-8 satellite crawler.
        """

        super().__init__(url, satellite)

    def get_links(self, pw):
        """
        Implemented abstract public method which performs HIMAWARI-8 specific base page extraction and extraction
        of links from the appropriate containing objects.

        @param pw: str - A string containing the Tor password for the given system configuration.
        @return links: {} - A key-value mapping of a title key in a standard format and its appropriate image link.
        """

        links = {}
        archive_links = []
        archive_pages = []
        
        page = self._extract_content(self.get_url(), pw)

        # Generate bs soup object and extract first 3 archive links for full disk HIMAWARI 8
        soup = BeautifulSoup(page.text, self.SOUP_PARSER)
        archive_link_containers = soup.findAll(self.A_ELEMENT, text=re.compile(self.ARCHIVE_TEXT))[:3]
        
        # Extract relative links via HREF property in each archive link container
        
        for archive_link_container in archive_link_containers:
            # Concatenate base HIMAWARI link to the containers' relative link path
            archive_links.append(self.HIMAWARI_8_BASE_LINK + archive_link_container.get(self.HREF_ATTRIBUTE))

        # Request each archive pages' content through Tor
        for archive_link in archive_links:
            page = self._extract_content(archive_link, pw)
            archive_pages.append(page)
        
        # Extract a links dictionary containing a title:url mapping
        links = self.__extract_hires_uris(archive_pages)
        
        return links


    def _create_img_dir(self, title):
        """
        Protected abstract method implementation which is called during the base SatelliteCrawlers' pulldown_images
        method. This method is to generate the directory string path of where an image should be placed or already
        exists.

        @param title: str - A string containing the following standard format: 'TITLE - DATE - HH-MM UTC'
        which describes the image being queried.
        @return dir_path: str - A directory string containing the following standard format: 'HIMAWARI-8/DATE/HH-MM UTC/TITLE'
        where the image downloaded should be placed, or already has been placed.
        """

        dir_path = ""
        
        today = re.split(self.TITLE_DELIMITER, title)[1]
        utctime = re.split(self.TITLE_DELIMITER, title)[-1].replace(":", "-")

        dir_path = self.HIMAWARI_8_DIRECTORY + "/" + str(today) + "/" + utctime + "/" + title
        
        return dir_path


    def __extract_hires_uris(self, archive_pages):
        """
        Private method which performs unique extraction of desired high resolution image links from the 
        list of requests.Response objects set.

        @param archive_pages: [] - A list of requests.Response objects each containing data for generating the 
        standardized title format and the URL link for the lates high resolution image.
        @return links: {} - A key-value mapping of a title key in a standard format and its appropriate image link
        """

        links = {}
        
        for archive_page in archive_pages:
            soup = BeautifulSoup(archive_page.text, self.SOUP_PARSER)
        
            # Gets the latest archive row
            latest_row = soup.findAll(self.TR_ELEMENT)[1]

            # Get the "td" elements in latest row 
            properties = latest_row.findAll(self.TD_ELEMENT)
            utc = properties[0].text + " " + self.UTC_STRING
            
            # Gets the last property in the latest archive row which contains the relative path to hi-res img
            relative_path = properties[-1].findAll(self.A_ELEMENT)[0].get(self.HREF_ATTRIBUTE)
            link = self.HIMAWARI_8_BASE_LINK + relative_path
            
            # generates a standard title format for generic pulldown_images function
            title = self.__generate_title(utc, relative_path)
            
            links[title] = link

        return links


    def __generate_title(self, utc, path):
        """
        Using a UTC formatted time and a relative path containing the partial title, performs the necessary 
        formatting to generate the standardized title format.

        @param utc: str - A string formatted as: '2021-01-24 21:30 UTC'.
        @param path: str - A string containing the relative path which contains some partial title.
        @return title: str - A string containing the following standard format: 'TITLE - DATE - HH-MM UTC'
        """

        title = ""
        throwaways = ['full', 'disk']

        # Extract the date (d), and create UTC time without the date.
        d = utc.split(" ")[0]
        utc = utc.split(" ")[1:]
        utc = ' '.join([str(t) for t in utc])

        # Take the last part of the partial path containing some title information
        title = path.split('/')[-1].split('_')
        
        # Remove all extra words that are not title and remove *.jpg last element
        title = [t for t in title if not t in throwaways][:-1]
        title = ' '.join([str(t).capitalize() for t in title]) + " - " + d + " - " + utc
        
        return title


    def create_satellite_directory(self):
        """
        Creates a high-level directory with the static HIMAWARI_8_DIRECTORY string if it does not exist.
        """

        if not os.path.exists(self.HIMAWARI_8_DIRECTORY):
            os.makedirs(self.HIMAWARI_8_DIRECTORY)