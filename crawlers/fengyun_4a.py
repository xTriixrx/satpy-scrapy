import os
import re
from bs4 import BeautifulSoup
from crawlers.satellite_crawler import SatelliteCrawler

class FENGYUN_4A(SatelliteCrawler):
    """
    Concrete satellite spider class for FENGYUN-4A which extends the base class, SatelliteCrawler.
    This method of splitting spiders into separate classes will help with keeping longevity of spider 
    runner classes and update issues easier that may occur during website HTML updates. This spider hierarchy
    requires using the Tor network and using the default settings (including ControlPort) to access the network.
    The FENGYUN_4A crawler does not use the Tor network but instead relys on using a VPN to perform the request,
    if you try to execute this crawler without having a VPN enabled the crawler will encounter long blocking periods
    as well as max retries exceptions. This is intentional as web scraping Chinese websites are not exactly safe, and
    Tor is blocked by China's deep packet analysis. Will continue to look for a way to make this crawler work with the
    Tor network.

    @author Vincent.Nigro
    @version 0.0.2
    @modified 2/13/22
    """

    FENGYUN_4A_DIRECTORY = 'FENGYUN-4A'
    FENGYUN_4A_URL = 'http://img.nsmc.org.cn/PORTAL/NSMC/XML/FY4A/'
    
    FENGYUN_4A_XML_FILES = ['FY4A_AGRI_IMG_DISK_MTCC_NOM.xml', 'FY4A_AGRI_IMG_DISK_GRA_NOM_C001.xml', 'FY4A_AGRI_IMG_DISK_GRA_NOM_C002.xml',
    'FY4A_AGRI_IMG_DISK_GRA_NOM_C003.xml','FY4A_AGRI_IMG_DISK_GRA_NOM_C004.xml', 'FY4A_AGRI_IMG_DISK_GRA_NOM_C005.xml', 'FY4A_AGRI_IMG_DISK_GRA_NOM_C006.xml',
    'FY4A_AGRI_IMG_DISK_GRA_NOM_C007.xml', 'FY4A_AGRI_IMG_DISK_GRA_NOM_C008.xml', 'FY4A_AGRI_IMG_DISK_GRA_NOM_C009.xml', 'FY4A_AGRI_IMG_DISK_COL_NOM_C009.xml',
    'FY4A_AGRI_IMG_DISK_GRA_NOM_C010.xml', 'FY4A_AGRI_IMG_DISK_COL_NOM_C010.xml', 'FY4A_AGRI_IMG_DISK_GRA_NOM_C011.xml', 'FY4A_AGRI_IMG_DISK_COL_NOM_C011.xml',
    'FY4A_AGRI_IMG_DISK_GRA_NOM_C012.xml', 'FY4A_AGRI_IMG_DISK_COL_NOM_C012.xml', 'FY4A_AGRI_IMG_DISK_GRA_NOM_C013.xml', 'FY4A_AGRI_IMG_DISK_COL_NOM_C013.xml',
    'FY4A_AGRI_IMG_DISK_GRA_NOM_C014.xml', 'FY4A_AGRI_IMG_DISK_COL_NOM_C014.xml']
    
    FENGYUN_4A_TITLE_MAP = {'FY4A AGRI IMG DISK MTCC NOM': 'Visible', 'FY4A AGRI IMG DISK GRA NOM C001': 'Band 1', 'FY4A AGRI IMG DISK GRA NOM C002': 'Band 2',
    'FY4A AGRI IMG DISK GRA NOM C003': 'Band 3', 'FY4A AGRI IMG DISK GRA NOM C004': 'Band 4', 'FY4A AGRI IMG DISK GRA NOM C005': 'Band 5', 
    'FY4A AGRI IMG DISK GRA NOM C006': 'Band 6', 'FY4A AGRI IMG DISK GRA NOM C007': 'Band 7', 'FY4A AGRI IMG DISK GRA NOM C008': 'Band 8', 
    'FY4A AGRI IMG DISK GRA NOM C009': 'Band 9', 'FY4A AGRI IMG DISK COL NOM C009': 'Band 9 Enhanced', 'FY4A AGRI IMG DISK GRA NOM C010': 'Band 10', 
    'FY4A AGRI IMG DISK COL NOM C010': 'Band 10 Enhanced', 'FY4A AGRI IMG DISK GRA NOM C011': 'Band 11', 'FY4A AGRI IMG DISK COL NOM C011': 'Band 11 Enhanced',
    'FY4A AGRI IMG DISK GRA NOM C012': 'Band 12', 'FY4A AGRI IMG DISK COL NOM C012': 'Band 12 Enhanced', 'FY4A AGRI IMG DISK GRA NOM C013': 'Band 13', 
    'FY4A AGRI IMG DISK COL NOM C013': 'Band 13 Enhanced', 'FY4A AGRI IMG DISK GRA NOM C014': 'Band 14', 'FY4A AGRI IMG DISK COL NOM C014': 'Band 14 Enhanced'}

    def __init__(self, url, satellite):
        """
        A concrete constructor which accepts a full base path to a URL to begin crawl, satellite name, and
        an appropriate resolution size to search for during crawl process.
        
        @param url: str - A string containing a full URL path to some website to begin web crawl.
        @param satellite: str - A string containing a representative name for the FENGYUN-4A satellite crawler.
        @param utcrange: [] - A list of utc times which increment by 15 minutes.
        """

        super().__init__(url, satellite)


    def get_links(self, pw):
        """
        Implemented abstract public method which performs FENGYUN_4A specific base page extraction and extraction
        of links from the appropriate containing objects.

        @param pw: str - A string containing the Tor password for the given system configuration.
        @return links: {} - A key-value mapping of a title key in a standard format and its appropriate image link
        """

        links = {}

        # Iterate over each XML file defining where images are located on server
        for xml_file in self.FENGYUN_4A_XML_FILES:
            # Extract xml page
            page = self._extract_content(self.get_url() + xml_file, pw)
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
                title = self.FENGYUN_4A_TITLE_MAP[desc]
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
        @return dir_path: str - A directory string containing the following standard format: 'FENGYUN-4A/DATE/HH-MM UTC/TITLE'
        where the image downloaded should be placed, or already has been placed.
        """

        dir_path = ""

        today = re.split(self.TITLE_DELIMITER, title)[1]
        utctime = re.split(self.TITLE_DELIMITER, title)[-1].replace(":", "-")

        dir_path = self.FENGYUN_4A_DIRECTORY + "/" + str(today) + "/" + utctime + "/" + title
        
        return dir_path


    def create_satellite_directory(self):
        """
        Implemented public abstract method which creates a high-level directory with the static 
        FENGYUN_4A_DIRECTORY string if it does not exist.
        """
        
        if not os.path.exists(self.FENGYUN_4A_DIRECTORY):
            os.makedirs(self.FENGYUN_4A_DIRECTORY)    