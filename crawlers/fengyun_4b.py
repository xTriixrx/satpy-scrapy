import os
import re
from bs4 import BeautifulSoup
from crawlers.satellite_crawler import SatelliteCrawler

class FENGYUN_4B(SatelliteCrawler):
    """
    Concrete satellite spider class for FENGYUN-4B which extends the base class, SatelliteCrawler.
    This method of splitting spiders into separate classes will help with keeping longevity of spider 
    runner classes and update issues easier that may occur during website HTML updates. This spider hierarchy
    circumvents using the Tor network since the Chinese firewall blocks Tor requests.
    The FENGYUN_4B crawler does not use the Tor network but instead relys on using a VPN to perform the request,
    if you try to execute this crawler without having a VPN enabled the crawler could have your IP blocked.
    This is intentional as web scraping Chinese websites are not exactly safe, and Tor is blocked by China's
    deep packet analysis. Will continue to look for a way to make this crawler work with the Tor network.

    @author Vincent.Nigro
    @version 0.0.1
    @modified 10/11/23
    """

    FENGYUN_4B_DIRECTORY = 'FENGYUN-4B'
    FENGYUN_4B_URL = 'http://img.nsmc.org.cn/PORTAL/NSMC/XML/FY4B/'
    
    FENGYUN_4B_XML_FILES = ['FY4B_AGRI_IMG_DISK_GCLR_NOM.xml', 'FY4B_AGRI_IMG_DISK_NATR_NOM.xml', 'FY4B_AGRI_IMG_DISK_SWCI_NOM.xml']
    
    FENGYUN_4B_TITLE_MAP = {'FY4B AGRI IMG DISK GCLR NOM': 'True Color', 'FY4B AGRI IMG DISK NATR NOM': 'Natural Color',
            'FY4B AGRI IMG DISK SWCI NOM': 'Sandwich'}

    def __init__(self, url, satellite):
        """
        A concrete constructor which accepts a full base path to a URL to begin crawl, satellite name, and
        an appropriate resolution size to search for during crawl process.
        
        @param url: str - A string containing a full URL path to some website to begin web crawl.
        @param satellite: str - A string containing a representative name for the FENGYUN-4B satellite crawler.
        @param utcrange: [] - A list of utc times which increment by 15 minutes.
        """

        super().__init__(url, satellite)

    def get_links(self, pw):
        """
        Implemented abstract public method which performs FENGYUN_4B specific base page extraction and extraction
        of links from the appropriate containing objects.

        @param pw: str - A string containing the Tor password for the given system configuration.
        @return links: {} - A key-value mapping of a title key in a standard format and its appropriate image link
        """

        links = {}

        # Iterate over each XML file defining where images are located on server
        for xml_file in self.FENGYUN_4B_XML_FILES:
            # Extract xml page
            page = self._extract_content(self.get_url() + xml_file, pw, notor=True)
            soup = BeautifulSoup(page.text, self.SOUP_PARSER)
            
            # Extract all <image> elements (should be basically entire document)
            image_elements = soup.findAll(self.IMAGE_ELEMENT)

            # Iterate over each image element to start generating links
            for image_element in image_elements:
                # Extract the elements' description, and split the utc time for title
                desc = image_element.get(self.DESC_ATTRIBUTE)
                time_data = image_element.get(self.TIME_ATTRIBUTE)
                date = time_data.split(" ")[0]
                utc = time_data.split(" ")[1]
                
                # Generate title based on title map and append date and utc time 
                title = self.FENGYUN_4B_TITLE_MAP[desc]
                title += " - " + date + " - " + utc + " UTC"
                link = image_element.get(self.URL_ATTRIBUTE)
                links[title] = link

        return links

    def _create_img_dir(self, title):
        """
        Protected abstract method implementation which is called during the base SatelliteCrawlers' pulldown_images
        method. This method is to generate the directory string path of where an image should be placed or already
        exists.

        @param title: str - A string containing the following standard format: 'TITLE - DATE - HH-MM UTC'
        which describes the image being queried.
        @return dir_path: str - A directory string containing the following standard format: 'FENGYUN-4B/DATE/HH-MM UTC/TITLE'
        where the image downloaded should be placed, or already has been placed.
        """

        dir_path = ""

        today = re.split(self.TITLE_DELIMITER, title)[1]
        utctime = re.split(self.TITLE_DELIMITER, title)[-1].replace(":", "-")

        dir_path = self.FENGYUN_4B_DIRECTORY + "/" + str(today) + "/" + utctime + "/" + title
        
        return dir_path

    def create_satellite_directory(self):
        """
        Implemented public abstract method which creates a high-level directory with the static 
        FENGYUN_4B_DIRECTORY string if it does not exist.
        """
        
        if not os.path.exists(self.FENGYUN_4B_DIRECTORY):
            os.makedirs(self.FENGYUN_4B_DIRECTORY)