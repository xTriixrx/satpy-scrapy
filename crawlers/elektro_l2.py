import re
import os
import pytz
import logging
from datetime import datetime, timedelta
from crawlers.satellite_crawler import SatelliteCrawler

class ELEKTRO_L2(SatelliteCrawler):
    """
    Concrete satellite spider class for ELEKTRO-L-2 which extends the base class, SatelliteCrawler.
    This method of splitting spiders into separate classes will help with keeping longevity of spider 
    runner classes and update issues easier that may occur during website HTML updates. This spider requires
    using FTP in order to extract the latest hi-res image for the ELEKTRO-L-2 spacecraft via the ntsomz.gptl.ru
    FTP server.

    @author Vincent.Nigro
    @version 0.0.1
    @modified 1/27/21
    """
    
    HALF_HOUR_MARK = 30
    JPG_NAME = 'original_RGB.jpg'
    MOSCOW_TIME_ZONE = 'Europe/Moscow'
    ELEKTRO_L2_DIRECTORY = 'ELEKTRO-L2'
    ELEKTRO_L2_URL = 'ftp://electro:electro@ntsomz.gptl.ru:2121/ELECTRO_L_2/'

    def __init__(self, url, satellite, day, utcrange):
        """
        A concrete constructor which accepts a full base path to a URL to begin crawl, satellite name, and
        an appropriate resolution size to search for during crawl process.
        
        @param url: str - A string containing a full URL path to some website to begin web crawl.
        @param satellite: str - A string containing a representative name for the HIMAWARI-8 satellite crawler.
        """

        super().__init__(url, satellite)
        self.__day = day
        self.__utcrange = utcrange


    def get_links(self, pw):
        """
        Implemented abstract public method which performs ELEKTRO-L-2 specific processing for creating the appropriate
        time information required for querying the Russian ntsomz.gptl.ru FTP server.

        @param pw: str - A string containing the Tor password for the given system configuration.
        @return links: {} - A key-value mapping of a title key in a standard format and its appropriate image link.
        """

        links = {}
        
        if self.__utcrange != '' or self.__day != '':
            links = self.__populate_ftp_link_range()
        else:
            # Get rounded utc time and full country time of russia
            utctime, country_time = self.__get_russian_utc_time()
            
            # Extract each field required for building title, filename, and relative_path 
            day, month, month_digits, year, utc = self.__get_date_fields(utctime)
            
            title, path = self.__generate_properties(day, month, month_digits, year, utc)
            
            logging.info(country_time.strftime("Current Date in Moscow, Russia is %d-%m-%y and the time is %H:%M:%S"))
            
            links[title] = self.get_url() + path

        return links
  

    def __populate_ftp_link_range(self):
        """
        Private method which populates the links dictionary based on the configured properties set by
        the constructor. Each setting will always generate the current Russian time properties and override
        the necessary ones that need to be overwritten with command line options (ones passed by constructor).

        @return links: {} - A key-value mapping of a title key in a standard format and its appropriate image link.
        """

        links = {}

        # Get rounded utc time and full country time of russia
        utctime, country_time = self.__get_russian_utc_time()
        
        logging.info(country_time.strftime("Current Date in Moscow, Russia is %d-%m-%y and the time is %H:%M:%S"))

        # Extract each field required for building title, filename, and relative_path 
        day, month, month_digits, year, utc = self.__get_date_fields(utctime)

        if self.__utcrange != '' and self.__day != '':
            for utc in self.__utcrange:
                title, path = self.__generate_properties(self.__day, month, month_digits, year, utc)
                links[title] = self.get_url() + path
        elif self.__utcrange != '':
            for utc in self.__utcrange:
                title, path = self.__generate_properties(day, month, month_digits, year, utc)
                links[title] = self.get_url() + path
        elif self.__day != '':
            title, path = self.__generate_properties(self.__day, month, month_digits, year, utc)
            links[title] = self.get_url() + path
        
        return links


    def __generate_properties(self, day, month, month_digits, year, utc):
        """
        A private method which returns the title and sub-path to the image located on the FTP hostname.

        @param day: str - A string digit representing the day ex: 25.
        @param month: str - A capitalized month ex: January.
        @param month_digits: str - A string containing 2 digits representing the month ex: 01.
        @param year: str - A year formated as YYYY ex: 2021.
        @param utc: str - A UTC formatted as XXXX ex: 0030 for 00:30 UTC.
        @return title, path: str, str - The standardized title and relative path.
        """

        # Original RGB - 26 Jan 2021 - 03-30 UTC
        title = self.__generate_title(day, month, year, utc)
        
        #YYMMDD_UTC_original_RGB.jpg
        filename = self.__generate_filename(day, month_digits, year, utc)

        # YYY/Jan/DD/UTC/img_name
        path = self.__generate_path(day, month, year, utc, filename)

        return title, path


    def __generate_title(self, day, month, year, utc):
        """
        A private method which generates a standardized title format to be used as a directory to contain the
        linked image as well as other processing done by the standard pulldown procedure.

        @param day: str - A string digit representing the day ex: 25.
        @param month: str - A capitalized month ex: January.
        @param year: str - A year formated as YYYY ex: 2021.
        @param utc: str - A UTC formatted as XXXX ex: 0030 for 00:30 UTC.
        @return title: str - A title with a standardized format such as: Original RGB - 26 Jan 2021 - 03-30 UTC
        """

        title = 'Original RGB - ' + day + ' ' + month[:3] + ' ' + \
                year + ' - ' + utc[:2] + '-' + utc[-2:] + ' ' + self.UTC_STRING
        
        return title


    def __generate_path(self, day, month, year, utc, filename):
        """
        A private method which generates a relative path on the FTP server to be concatenated 
        to the base url hostname.
        
        @param day: str - A string digit representing the day ex: 25.
        @param month: str - A capitalized month ex: January.
        @param year: str - A year formated as YYYY ex: 2021.
        @param utc: str - A UTC formatted as XXXX ex: 0030 for 00:30 UTC.
        @param filename: str - The filename of current link gen iteration with format: YYMMDD_UTC_original_RGB.jpg
        @return path: str - A relative path on the FTP server to be concatenated with base url hostname.
        """

        path = year + '/' + month + '/' + day + '/' + utc + '/' + filename

        return path


    def __generate_filename(self, day, month_digits, year, utc):
        """
        A private method which returns the filename being queried for the current iteration of link generation.

        @param day: str - A string digit representing the day ex: 25.
        @param month_digits: str - A string containing 2 digits representing the month ex: 01.
        @param year: str - A year formated as YYYY ex: 2021.
        @param utc: str - A UTC formatted as XXXX ex: 0030 for 00:30 UTC.
        @return filename: str - The filename of current link gen iteration with format: #YYMMDD_UTC_original_RGB.jpg
        """

        filename = year[-2:] + month_digits + day + '_' + utc + '_' + self.JPG_NAME

        return filename


    def __get_russian_utc_time(self):
        """
        A private method which generates the UTC datetime object which is 3 hours ahead of typical UTC time
        and a full russian datetime object with the current time in Moscow. The UTC datetime object will either be set
        at the 30 minute mark or the 00 minute mark dependent upon the current time. The ELEKTRO-L2 FTP server uploads
        images in half hour intervals.

        @return utctime, country_time: datetime, datetime - A datetime object containing russian UTC time and full time.
        """

        # Get current time in MOSCOW
        time_zone = pytz.timezone(self.MOSCOW_TIME_ZONE)
        country_time = datetime.now(time_zone)
        utctime = country_time.utcnow()
        
        # Russia operates +3 hours ahead of UTC time.
        difference = timedelta(hours = 3)
        utctime += difference
        
        # FTP server pushes files every half hour in UTC time.
        if utctime.minute > self.HALF_HOUR_MARK:
            difference = timedelta(minutes = (utctime.minute - self.HALF_HOUR_MARK))
            utctime -= difference
        else:
            difference = timedelta(minutes = utctime.minute)
            utctime -= difference
        
        return utctime, country_time


    def __get_date_fields(self, utctime):
        """
        A private method which generates the necessary date fields required for building 
        link path and standardized title.

        @param utctime: datetime - A datetime object containing the current russian UTC time.
        @return day, month, month_digits, year, utc
        """

        year = utctime.strftime('%Y') # YYYY
        month = utctime.strftime('%B') # January
        month_digits = utctime.strftime('%m') # 01
        day = utctime.strftime('%d') # 26
        utc = utctime.strftime('%H') + utctime.strftime('%M') # 0330 -> 03:30 UTC

        return day, month, month_digits, year, utc


    def _create_img_dir(self, title):
        """
        Protected abstract method implementation which is called during the base SatelliteCrawlers' pulldown_images
        method. This method is to generate the directory string path of where an image should be placed or already
        exists.

        @param title: str - A string containing the following standard format: 'TITLE - DATE - HH-MM UTC'
        which describes the image being queried.
        @return dir_path: str - A directory string containing the following standard format: 'ELEKTRO-L/DATE/HH-MM UTC/TITLE'
        where the image downloaded should be placed, or already has been placed.
        """

        dir_path = ""

        today = re.split(self.TITLE_DELIMITER, title)[1]
        utctime = re.split(self.TITLE_DELIMITER, title)[-1].replace(":", "-")

        dir_path = self.ELEKTRO_L2_DIRECTORY + "/" + str(today) + "/" + utctime + "/" + title
        
        return dir_path


    def create_satellite_directory(self):
        """
        Implemented public abstract method which creates a high-level directory with the static 
        ELEKTRO_L2_DIRECTORY string if it does not exist.
        """

        if not os.path.exists(self.ELEKTRO_L2_DIRECTORY):
            os.makedirs(self.ELEKTRO_L2_DIRECTORY)


    def _create_img_dir(self, title):
        """
        Protected abstract method implementation which is called during get_links ELEKTRO-L-2 implementation
        as it utilizes a FTP server to pull down the latest spacecrafts' images.

        @param title: str - A string containing the following standard format: 'TITLE - DATE - HH-MM UTC'
        which describes the image being queried.
        @return dir_path: str - A directory string containing the following standard format: 'ELEKTRO-L-2/DATE/HH-MM UTC/TITLE'
        where the image downloaded should be placed, or already has been placed.
        """

        dir_path = ""

        today = re.split(self.TITLE_DELIMITER, title)[1]
        utctime = re.split(self.TITLE_DELIMITER, title)[-1].replace(":", "-")

        dir_path = self.ELEKTRO_L2_DIRECTORY + "/" + str(today) + "/" + utctime + "/" + title
        
        return dir_path