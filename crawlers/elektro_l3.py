import re
import os
from bs4 import BeautifulSoup
from crawlers.satellite_crawler import SatelliteCrawler

class ELEKTRO_L3(SatelliteCrawler):
    """
    Concrete satellite spider class for ELEKTRO-L3 which extends the base class, SatelliteCrawler.
    This method of splitting spiders into separate classes will help with keeping longevity of spider 
    runner classes and update issues easier that may occur during website HTML updates. This spider hierarchy
    requires using the Tor network and using the default settings (including ControlPort) to access the network.

    @author Vincent.Nigro
    @version 0.0.1
    @modified 2/11/21
    """
    
    BAND_1 = '296'
    BAND_9 = '297'
    TD_CLASS_VALUE = 'b5'
    HTTP_HEADER = 'http://'
    SYNTHESIZED_COLOR = '295'
    ELEKTRO_L3_DIRECTORY = 'ELEKTRO-L3'
    IMAGE_SET = [SYNTHESIZED_COLOR, BAND_1, BAND_9]
    ELEKTRO_L3_URL = 'http://planet.iitp.ru/index.php?lang=en&page_type=oper_prod&page=product&prod='

    def __init__(self, url, satellite):
        """
        A concrete constructor which accepts a full base path to a URL to begin crawl, satellite name, and
        an appropriate resolution size to search for during crawl process.
        
        @param url: str - A string containing a full URL path to some website to begin web crawl.
        @param satellite: str - A string containing a representative name for the ELEKTRO-L3 satellite crawler.
        """

        super().__init__(url, satellite)


    def get_links(self, pw):
        """
        Implemented abstract public method which performs ELEKTRO-L-2 specific processing for creating the appropriate
        time information required for querying the configured base url.

        @param pw: str - A string containing the Tor password for the given system configuration.
        @return links: {} - A key-value mapping of a title key in a standard format and its appropriate image link.
        """

        links = {}

        # For each image type defined in class create set of links and populate into links dictionary
        for image_type in self.IMAGE_SET:
            # Extract base page for current image type to get image links
            page = self._extract_content(self.get_url() + image_type, pw)

            # Create bs soup object and extract containers holding high resolution image links and dates
            soup = BeautifulSoup(page.text, self.SOUP_PARSER)
            td_containers = soup.findAll(self.TD_ELEMENT, {self.CLASS_ATTRIBUTE: self.TD_CLASS_VALUE})

            # For each container extract date/utc time of image as well as image link        
            for container in td_containers:
                c = container.text.strip()
                # Keep first 2 elements containing date and time
                date_fields = re.compile("\s").split(c)[:2]
                
                title = self.__generate_title(image_type, date_fields)
                
                a_tag = container.findAll(href=re.compile(self.HTTP_HEADER))[0]
                link = a_tag.get(self.HREF_ATTRIBUTE)
                
                links[title] = link

        return links


    def __generate_title(self, image_type, date_fields):
        """
        A private method which generates a standardized title format to be used as a directory to contain the
        linked image as well as other processing done by the standard pulldown procedure.

        @param image_type: str - A string containing some key which represents the type of image link being generated.
        @param date_fields: [] - A list containing a date and a utc time formatted as YYYY-MM-DD and HH:MM:SS respectively.
        @return title: str - A title with a standardized format such as: Synthesized Color - 2021-02-11 - 03-30 UTC
        """

        title = ''
        utc_fields = date_fields[1].split(':')
        hour = utc_fields[0]
        minutes = utc_fields[1]

        if image_type == self.SYNTHESIZED_COLOR:
            title = 'Synthesized Color - '
        elif image_type == self.BAND_1:
            title = 'Band 1 - '
        elif image_type == self.BAND_9:
            title = 'Band 9 - '
        title += date_fields[0] + ' - ' + hour + '-' + minutes + ' ' + self.UTC_STRING
        
        return title


    def _create_img_dir(self, title):
        """
        Protected abstract method implementation which is called during the base SatelliteCrawlers' pulldown_images
        method. This method is to generate the directory string path of where an image should be placed or already
        exists.

        @param title: str - A string containing the following standard format: 'TITLE - DATE - HH-MM UTC'
        which describes the image being queried.
        @return dir_path: str - A directory string containing the following standard format: 'ELEKTRO-L3/DATE/HH-MM UTC/TITLE'
        where the image downloaded should be placed, or already has been placed.
        """

        dir_path = ""

        today = re.split(self.TITLE_DELIMITER, title)[1]
        utctime = re.split(self.TITLE_DELIMITER, title)[-1].replace(":", "-")

        dir_path = self.ELEKTRO_L3_DIRECTORY + "/" + str(today) + "/" + utctime + "/" + title
        
        return dir_path


    def create_satellite_directory(self):
        """
        Implemented public abstract method which creates a high-level directory with the static 
        ELEKTRO_L2_DIRECTORY string if it does not exist.
        """

        if not os.path.exists(self.ELEKTRO_L3_DIRECTORY):
            os.makedirs(self.ELEKTRO_L3_DIRECTORY)