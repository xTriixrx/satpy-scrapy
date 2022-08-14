import re
import os
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from crawlers.satellite_crawler import SatelliteCrawler

class EWS_G1(SatelliteCrawler):
    """
    Concrete satellite spider class for EWS-G1 which extends the base class, SatelliteCrawler.
    This method of splitting spiders into separate classes will help with keeping longevity of spider 
    runner classes and update issues easier that may occur during website HTML updates. This spider hierarchy
    requires using the Tor network and using the default settings (including ControlPort) to access the network.

    @author Vincent.Nigro
    @version 0.0.2
    @modified 2/12/22
    """

    VISIBLE = '_01_'
    NEAR_IR = '_02_'
    IMG_TYPE = 'fd.gif'
    WATER_VAPOR = '_03_'
    LONGWAVE_IR = '_04_'
    CO2_LONGWAVE_IR = '_06_'
    EWS_G1_FIELD = 'ews-g1_'
    VISIBLE_TITLE = 'Visible'
    NEAR_IR_TITLE = 'Near IR'
    EWS_G1_DIRECTORY = 'EWS-G1'
    EWS_G1_TIME_ZONE = 'Etc/GMT-4'
    WATER_VAPOR_TITLE = 'Water Vapor'
    LONGWAVE_IR_TITLE = 'Longwave IR'
    CO2_LONGWAVE_IR_TITLE = 'C02 Longwave IR'
    EWS_G1_URL = 'https://www.ssec.wisc.edu/data/geo/images/ews-g1/animation_images/'

    def __init__(self, url, satellite):
        """
        A concrete constructor which accepts a full base path to a URL to begin crawl, and satellite name.
        
        @param url: str - A string containing a full URL path to some website to begin web crawl.
        @param satellite: str - A string containing a representative name for the EWS-G1 satellite crawler.
        """

        super().__init__(url, satellite)


    def get_links(self, pw):
        """
        Implemented abstract public method which performs EWS-G1 page link generation based on current time.

        @param pw: str - A string containing the Tor password for the given system configuration.
        @return links: {} - A key-value mapping of a title key in a standard format and its appropriate image link.
        """

        links = {}
        
        # Get set of links available
        page = self._extract_content(self.get_url(), pw)

        soup = BeautifulSoup(page.text, self.SOUP_PARSER)
        a_elements = soup.findAll(self.A_ELEMENT, {self.HREF_ATTRIBUTE: re.compile(self.IMG_TYPE)})

        # Iterate through each a_element containing details for a given full disk image
        for a_element in a_elements:
            # Extract href property containing details
            href = a_element.get(self.HREF_ATTRIBUTE)

            # Generate link based on base_url + href
            link = self.get_url() + href

            # Generate a title based on the href details
            title = self.__generate_title(href)

            self._logger.debug("Generated link " + link + " for image " + title + ".")

            links[title] = link

        return links


    def __generate_title(self, href):
        """
        Using the href provided, performs the necessary formatting to generating the standardized title format.

        @param href: str - A string containing the julian date and image type such as ews-g1_2022042_1415_01_fd.gif
        @return title: str - A string containing the following standard format: 'TITLE - DATE - HH-MM UTC'
        """

        # Split parts of the href, should produce something such as ['ews-g1, 'YYYYJJJ', 'HHMM', 'FF', 'fd.gif']
        # Where YYYY represents the year, HH and MM represents the UTC hour and minute time respectively, 
        # JJJ represents a julian day, and FF represents an image type
        parts = href.split('_')
        
        utc = parts[2]
        img_type = parts[3]
        year = parts[1][:-3]
        julian_day = parts[1][4:]

        # Create a georgian datetime object and convert to a string formatted as YYYY-MM-DD
        date = self.__convert_julian_day_to_georgian(year, julian_day)
        date = date.strftime('%Y-%m-%d')

        title = ''
        if img_type in self.VISIBLE:
            title = self.VISIBLE_TITLE
        elif img_type in self.NEAR_IR:
            title = self.NEAR_IR_TITLE
        elif img_type in self.WATER_VAPOR:
            title = self.WATER_VAPOR_TITLE
        elif img_type in self.LONGWAVE_IR:
            title = self.LONGWAVE_IR_TITLE
        elif img_type in self.CO2_LONGWAVE_IR:
            title = self.CO2_LONGWAVE_IR_TITLE
        
        title += ' - ' + date + ' - ' + utc[:-2] +  '-' + utc[2:] + ' ' + self.UTC_STRING

        self._logger.debug("Created title for href " + href + ": " + title + ".")
        return title


    def __convert_julian_day_to_georgian(self, year, julian_day):
        """
        Converts a Julian calendar date into a Georgian calendar datetime object.

        @param year: str - A string representing the current year such as '2022'.
        @param julian_day: str - A string representing a julian day such as '042'.
        @return georgian_date: datetime - A georgian date time representing the julian day and year in YYYY-MM-DD form.
        """

        georgian_date = datetime(int(year), 1, 1)

        # Subtract by one as the conversion is off by 1
        difference = timedelta(int(julian_day) - 1)
        
        # Apply difference delta to georgian date
        georgian_date += difference

        return georgian_date


    def _create_img_dir(self, title):
        """
        Protected abstract method implementation which is called during the base SatelliteCrawlers' pulldown_images
        method. This method is to generate the directory string path of where an image should be placed or already
        exists.

        @param title: str - A string containing the following standard format: 'TITLE - DATE - HH-MM UTC'
        which describes the image being queried.
        @return dir_path: str - A directory string containing the following standard format: 'EWS-G1/DATE/HH-MM UTC/TITLE'
        where the image downloaded should be placed, or already has been placed.
        """
        
        dir_path = ''
        
        today = re.split(self.TITLE_DELIMITER, title)[1]
        utctime = re.split(self.TITLE_DELIMITER, title)[-1].replace(':', '-')

        dir_path = self.EWS_G1_DIRECTORY + os.sep + str(today) + os.sep + utctime + os.sep + title
        
        self._logger.debug("Image directory path for title " + title + ": " + dir_path + ".")

        return dir_path


    def create_satellite_directory(self):
        """
        Creates a high-level directory with the static EWS_G1_DIRECTORY string if it does not exist.
        """

        if not os.path.exists(self.EWS_G1_DIRECTORY):
            self._logger.debug("Creating directory at path: " + self.EWS_G1_DIRECTORY)
            os.makedirs(self.EWS_G1_DIRECTORY)