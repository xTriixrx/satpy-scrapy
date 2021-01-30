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

    @author Vincent.Nigro
    @version 0.0.1
    @modified 1/29/21
    """

    FENGYUN_4A_DIRECTORY = 'FENGYUN-4A'
    FENGYUN_4A_URL = 'https://www.qweather.com/en/satellite/fengyun4-asia-tc.html'

    def __init__(self, url, satellite, utcrange):
        """
        A concrete constructor which accepts a full base path to a URL to begin crawl, satellite name, and
        an appropriate resolution size to search for during crawl process.
        
        @param url: str - A string containing a full URL path to some website to begin web crawl.
        @param satellite: str - A string containing a representative name for the FENGYUN-4A satellite crawler.
        @param utcrange: [] - A list of utc times which increment by 15 minutes.
        """

        super().__init__(url, satellite)
        self.__utcrange = utcrange


    def get_links(self, pw):
        """
        Implemented abstract public method which performs FENGYUN_4A specific base page extraction and extraction
        of links from the appropriate containing objects.

        @param pw: str - A string containing the Tor password for the given system configuration.
        @return links: {} - A key-value mapping of a title key in a standard format and its appropriate image link
        """

        links = {}
        
        page = self._extract_content(self.get_url(), pw)
        
        soup = BeautifulSoup(page.text, self.SOUP_PARSER)
        image_links = soup.findAll(self.IMG_ELEMENT)
        
        # Extract only <img> containers with path 'satellite' in src string.
        image_links = [link for link in image_links if 'satellite' in str(link)]
        image_links = self.__extract_src_links(image_links)

        # If utcrange was provided
        if self.__utcrange != '':
            # Get each image from earliest to latest image.
            links = self.__populate_link_range(image_links)
        else:
            # Reverse list to ascending order and get latest image
            image_links.sort(reverse=True)
            links[self.__generate_title(image_links[0])] = image_links[0]

        return links


    def __populate_link_range(self, image_links):
        """
        A private method which receives a list of full URL paths to a set of images and will
        check if the link is within the set UTC range. If it is, the URL is placed into the 
        links dictionary with the appropriate standardized title, otherwise it is left out.

        @param image_links: [] - A list of full URL paths to each respective image.
        @return links: {} - A key-value mapping of a title key in a standard format and its appropriate image link.
        """

        links = {}

        for image_link in image_links:
            link_parts = image_link.split('/')
            link_parts.reverse()
            utctime = link_parts[1] + link_parts[0].split('.')[0]
            
            # If built utctime is within the range list.
            if utctime in self.__utcrange:
                title = self.__generate_title(image_link)
                links[title] = image_link
        
        return links


    def __extract_src_links(self, image_containers):
        """
        A private method which receives a set of <img> containers which contain src attributes
        holding the image links needed to be extracted. Each containers' src attribute is extracted
        into a list and returned to the caller.

        @param image_containers: [] - A list of <img> containers to be extracted.
        @return src_links: [] - A list of full URL paths to their respective images.
        """
        
        src_links = []

        for image_container in image_containers:
            src_links.append(image_container[self.SRC_ATTRIBUTE])
        
        # Remove 'latest' labeled image link
        return src_links[1:]


    def __generate_title(self, link):
        """
        A private method which generates a standardized title format to be used as a directory to contain the
        linked image as well as other processing done by the standard pulldown procedure.

        @param link: str - A full URL link to an image containing values to be used in the title.
        @return title: str - A title with a standardized format such as: 'True Color - 29-01-2021 - 23-00 UTC'
        """
        
        link_parts = link.split('/')
        link_parts.reverse()

        title = 'True Color - ' + link_parts[2] + '-' + link_parts[3] + '-' + link_parts[4] + \
            ' - ' + link_parts[1] + '-' + link_parts[0].split('.')[0] + ' ' + self.UTC_STRING
        
        return title


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