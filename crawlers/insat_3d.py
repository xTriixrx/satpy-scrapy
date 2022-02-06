import re
import os
import pytz
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from crawlers.satellite_crawler import SatelliteCrawler

class INSAT_3D(SatelliteCrawler):
    """
    Concrete satellite spider class for INSAT-3D which extends the base class, SatelliteCrawler.
    This method of splitting spiders into separate classes will help with keeping longevity of spider 
    runner classes and update issues easier that may occur during website HTML updates. This spider hierarchy
    requires using the Tor network and using the default settings (including ControlPort) to access the network.

    @author Vincent.Nigro
    @version 0.0.1
    @modified 2/5/22
    """

    GMT_TIME_ZONE = 'Etc/GMT'
    INSAT_3D_DIRECTORY = 'INSAT-3D'
    INSAT_3D_REGEX = '(L1B_STD|L2B)'
    INSAT_3D_BASE_URL = 'https://mosdac.gov.in'
    INSAT_3D_URL = 'https://mosdac.gov.in/data/weather.do?mode=diplay3DImage'

    def __init__(self, url, satellite):
        """
        A concrete constructor which accepts a full base path to a URL to begin crawl, satellite name, and
        an appropriate resolution size to search for during crawl process.
        
        @param url: str - A string containing a full URL path to some website to begin web crawl.
        @param satellite: str - A string containing a representative name for the INSAT-3D satellite crawler.
        """

        super().__init__(url, satellite)
    
    def get_links(self, pw):
        """
        Implemented abstract public method which performs INSAT-3D specific base page extraction and extraction
        of links from the appropriate containing objects.

        @param pw: str - A string containing the Tor password for the given system configuration.
        @return links: {} - A key-value mapping of a title key in a standard format and its appropriate image link.
        """
        links = {}

        # Get an adjusted GMT time that is about a half hour behind the current
        gmt_time = self.__get_adjusted_gmttime()
        date_fields = self.__get_date_fields(gmt_time)

        # Extract the web page with the set of full disk links & titles
        page = self._extract_content(self.get_url(), pw)
        
        soup = BeautifulSoup(page.text, self.SOUP_PARSER)

        # Get every <a> element that has an href that matches the classes' regex, then keep only even numbered links as the
        # captured <a> elements are doubled, the first in each pair contains a title within the elements' text
        a_elements = soup.findAll(self.A_ELEMENT, {self.HREF_ATTRIBUTE: re.compile(self.INSAT_3D_REGEX)})[::2]

        # Iterate over each <a> element, extract the href link, append to the base Mosdac gov link, get the image type for the title & add to links
        for a_element in a_elements:
            link = self.INSAT_3D_BASE_URL + a_element.get(self.HREF_ATTRIBUTE)
            image_type = a_element.text.strip()
            title = self.__generate_title(image_type, date_fields)
            links[title] = link
        
        return links


    def __get_date_fields(self, utctime):
        """
        A private method which generates the necessary date fields required for building 
        link path and standardized title.

        @param utctime: datetime - A datetime object containing the current russian UTC time.
        @return day, month, year, hour, minute
        """

        year = utctime.strftime('%Y') # YYYY
        month= utctime.strftime('%m') # 01
        day = utctime.strftime('%d') # 26
        hour = utctime.strftime('%H') # 03
        minute = utctime.strftime('%M') # 30

        return year, month, day, hour, minute


    def __get_adjusted_gmttime(self):
        """
        Creates a GMT time that is an hour behind the current time to estimate the image that is stored on the
        Mosdac gov site; further time analysis would have to be extrapolated from the actual image once it is processed
        as the Mosdac gov site does not include timestamps along with the images currently.
        
        @return gmt_time: datetime - A datetime object containing the current GMT time behind by a half hour.
        """
        
        time = datetime.now()
        utctime = time.utcnow()
        utctime -= timedelta(hours = 1)
        
        # Always take off a half hour off time
        if utctime.minute >= 0 and utctime.minute <= 30:
            difference = timedelta(minutes = utctime.minute)
            utctime -= difference
            difference = timedelta(minutes = 00)
            utctime += difference
        elif utctime.minute > 30 and utctime.minute <= 59:
            difference = timedelta(minutes = utctime.minute)
            utctime -= difference
            difference = timedelta(minutes = 30)
            utctime += difference
        
        # Returns a GMT timezone based timestamp which is represented by the Mosdac imagery jpg's
        return utctime.replace(tzinfo=pytz.timezone(self.GMT_TIME_ZONE))


    def _create_img_dir(self, title):
        """
        Protected abstract method implementation which is called during the base SatelliteCrawlers' pulldown_images
        method. This method is to generate the directory string path of where an image should be placed or already
        exists.

        @param title: str - A string containing the following standard format: 'TITLE - DATE - HH-MM GMT'
        which describes the image being queried.
        @return dir_path: str - A directory string containing the following standard format: 'INSAT-3D/DATE/HH-MM GMT/TITLE'
        where the image downloaded should be placed, or already has been placed.
        """

        dir_path = ""
        
        today = re.split(self.TITLE_DELIMITER, title)[1]
        time = re.split(self.TITLE_DELIMITER, title)[-1].replace(':', '-')

        dir_path = self.INSAT_3D_DIRECTORY + os.sep + str(today) + os.sep + time + os.sep + title
        
        return dir_path


    def __generate_title(self, my_type, date_fields):
        """
        Using a GMT formatted datetime and a relative path containing the partial title, performs the necessary 
        formatting to generate the standardized title format.

        @param my_type: str - A string containing type of the image.
        @param date_fields: [] - A list containing a set of fields for the date and time of the image.
        @return title: str - A string containing the following standard format: 'TITLE - DATE - HH-MM GMT'
        """
        
        title = ''
        date = date_fields[0] + '-' + date_fields[1] + '-' + date_fields[2] # YYYY-MM-DD
        time = date_fields[3] + '-' + date_fields[4] + ' GMT' # HH-MM GMT

        title += my_type + ' - ' + date + ' - ' + time
        
        return title


    def create_satellite_directory(self):
        """
        Creates a high-level directory with the static INSAT_3D_DIRECTORY string if it does not exist.
        """

        if not os.path.exists(self.INSAT_3D_DIRECTORY):
            os.makedirs(self.INSAT_3D_DIRECTORY)