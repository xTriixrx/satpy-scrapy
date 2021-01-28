import re
import os
from bs4 import BeautifulSoup 
from crawlers.satellite_crawler import SatelliteCrawler

class GOES_WEST(SatelliteCrawler):
    """
    Concrete satellite spider class for GOES_WEST (GOES-17) which extends the base class, SatelliteCrawler.
    This method of splitting spiders into separate classes will help with keeping longevity of spider
    runner classes and update issues easier that may occur during website HTML updates. This spider hierarchy
    requires using the Tor network and using the default settings (including ControlPort) to access the network.

    @author Vincent.Nigro
    @version 0.0.1
    @modified 1/24/21
    """

    GOES_WEST_DIRECTORY = 'GOES-WEST'
    GOES_WEST_URL = 'https://www.star.nesdis.noaa.gov/GOES/fulldisk.php?sat=G17'
    
    def __init__(self, url, satellite, resolution):
        """
        A concrete constructor which accepts a full base path to a URL to begin crawl, satellite name, and
        an appropriate resolution size to search for during crawl process.
        
        @param url: str - A string containing a full URL path to some website to begin web crawl.
        @param satellite: str - A string containing a representative name for the GOES-WEST satellite crawler.
        @parm resolution: int - An integer representation of a pixel resolution to search for in web crawler.
        """

        super().__init__(url, satellite)
        self.__resolution = resolution


    def get_links(self, pw):
        """
        Implemented abstract public method which performs GOES-WEST specific base page extraction and extraction
        of links from the appropriate containing objects.

        @param pw: str - A string containing the Tor password for the given system configuration.
        @return links: {} - A key-value mapping of a title key in a standard format and its appropriate image link.
        """

        links = {}
        
        page = self._extract_content(self.get_url(), pw)

        # Generate bs soup object and extract list of containers containing each set of image links
        soup = BeautifulSoup(page.text, self.SOUP_PARSER)
        summary_containers = soup.findAll(self.DIV_ELEMENT, {self.CLASS_ATTRIBUTE: self.GOES_TARGET_CLASS_VALUE})

        # Extract each URI for each image type available for px resolution
        links = self.__extract_hires_uris(summary_containers, self.__resolution)
        
        return links


    def _create_img_dir(self, title):
        """
        Protected abstract method implementation which is called during the base SatelliteCrawlers' pulldown_images
        method. This method is to generate the directory string path of where an image should be placed or already
        exists.

        @param title: str - A string containing the following standard format: 'TITLE - DATE - HH-MM UTC'
        which describes the image being queried.
        @return dir_path: str - A directory string containing the following standard format: 'GOES-WEST/DATE/HH-MM UTC/TITLE'
        where the image downloaded should be placed, or already has been placed.
        """

        dir_path = ""
        
        today = re.split(self.TITLE_DELIMITER, title)[1]
        utctime = re.split(self.TITLE_DELIMITER, title)[-1].replace(":", "-")

        dir_path = self.GOES_WEST_DIRECTORY + "/" + str(today) + "/" + utctime + "/" + title
        
        return dir_path


    def __extract_hires_uris(self, containers, res):
        """
        Private method which performs unique extraction of desired high resolution image links
        from the containers set.

        @param containers: ResultSet - A list of results each containing multiple image links of different resolutions.
        @param res: int - A desired resolution to extract the appropriate image link from each container.
        @return links: {} - A key-value mapping of a title key in a standard format and its appropriate image link.
        """

        links = {}

        for container in containers:
            a_tags = self.__extract_image_link(container, res)
            a_tag = a_tags[0]

            link = a_tag.get(self.HREF_ATTRIBUTE)
            title = a_tag.get(self.TITLE_ATTRIBUTE)

            links[title] = link

        return links


    def __extract_image_link(self, container, res):
        """
        Private method which extracts image links in a div container links to downloadable images 
        with regex containing the desired resolution of the image.

        @param container: Any - A object containing a subset of HTML markup containing many image links.
        @param res: int - An integer representation of the desired resolution.
        @return links: [] - A list which should contain a single element of the appropriate resolution image link.
        """

        links = container.findAll(href=re.compile(str(res)))
        
        return links


    def create_satellite_directory(self):
        """
        Implemented public abstract method which creates a high-level directory with the static 
        GOES_WEST_DIRECTORY string if it does not exist.
        """

        if not os.path.exists(self.GOES_WEST_DIRECTORY):
            os.makedirs(self.GOES_WEST_DIRECTORY)


    def get_resolution(self):
        """
        Public accessor method for retrieving the private member containing the configured resolution
        for the current GOES-WEST instance.
        """

        return self.__resolution