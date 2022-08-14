import re
import os
import pytz
from ftplib import FTP
from googletrans import Translator
from datetime import datetime, timedelta
from crawlers.satellite_crawler import SatelliteCrawler

class ARKTIKA_M1(SatelliteCrawler):
    """
    Concrete satellite spider class for ARKTIKA_M1 which extends the base class, SatelliteCrawler.
    This method of splitting spiders into separate classes will help with keeping longevity of spider 
    runner classes and update issues easier that may occur during website HTML updates. This spider requires
    using FTP in order to extract the latest hi-res image for the ARKTIKA_M1 spacecraft via the ntsomz.gptl.ru
    FTP server.

    @author Vincent.Nigro
    @version 0.0.2
    @modified 8/12/22
    """
    
    HALF_HOUR_MARK = 30
    FILE_PREFIX = 'V1_3720_'
    ARKTIKA_M1_FTP_PORT = 2121
    ARKTIKA_M1_USERNAME = 'electro'
    ARKTIKA_M1_PASSWORD = 'electro'
    MOSCOW_TIME_ZONE = 'Europe/Moscow'
    ARKTIKA_M1_DIRECTORY = 'ARKTIKA-M1'
    ARKTIKA_M1_URL_HOSTNAME = 'ntsomz.gptl.ru'
    ARKTIKA_M1_FTP_BASE_DIRECTORY = 'ARKTIKA_M_1'
    ARKTIKA_M1_URL = 'ftp://electro:electro@ntsomz.gptl.ru:2121/ARKTIKA_M_1'
    ARKTIKA_M1_PREFIXES = ['Band 1', 'Band 2', 'Band 3', 'Band 4', 'Band 5', 'Band 6', 
    'Band 7', 'Band 8', 'Band 9', 'Band 10']

    def __init__(self, url, satellite, day, utcrange):
        """
        A concrete constructor which accepts a full base path to a URL to begin crawl, satellite name, and
        an appropriate resolution size to search for during crawl process.
        
        @param url: str - A string containing a full URL path to some website to begin web crawl.
        @param satellite: str - A string containing a representative name for the ARKTIKA-M1 satellite crawler.
        """

        super().__init__(url, satellite)
        self.__day = day
        self.__utcrange = utcrange
        self.__translator = Translator()


    def get_links(self, pw):
        """
        Implemented abstract public method which performs ARKTIKA-M1 specific processing for creating the appropriate
        time information required for querying the Russian ntsomz.gptl.ru FTP server.

        @param pw: str - A string containing the Tor password for the given system configuration.
        @return links: {} - A key-value mapping of a title key in a standard format and its appropriate image link.
        """

        days = []
        links = {}
        
        # Get current utc time of russia
        utctime = self.__get_russian_utc_time()
        self._logger.debug("Approximate current russian utc time is: " + utctime.strftime("%x - %X"))
        
        # Extract each field required for run
        year, month = self.__get_date_fields(utctime)

        # Translate month from english to russian
        translated_month = self.__translator.translate(month, src="en", dest="ru")
        translated_month = translated_month.text
        self._logger.debug('Translated english month ' + month + ' to russian month ' + translated_month + '.')
        
        if self.__utcrange != '' and self.__day != '':
            days.append(self.__day)
            links = self.extract_links(year, translated_month, days, self.__utcrange)
        elif self.__utcrange != '':
            links = self.extract_links(year, translated_month, utc_range=self.__utcrange)
        elif self.__day != '':
            days.append(self.__day)
            links = self.extract_links(year, translated_month, days)
        else:
            links = self.extract_links(year, translated_month)

        return links
    
    
    def extract_links(self, year, translated_month, days=[], utc_range=[]):
        """
        Extracts and retrieves the file links for a set of days, within a utc_range. This will initiate
        the FTP connection to the ARKTIKA_M1 server and begin traversing the directories for the current
        month.

        @param year: str - The current year.
        @param translated_month: str - A string in Russian representing the current month.
        @param days: [] - A list representing a single day; if empty it means retrieve all days.
        @param utc_range: [] - A list of utc times in HHMM format to set the time range of returned links.
        @return links: {} - A key-value mapping of a title key in a standard format and its appropriate image link.
        """
        
        links = {}

        # Initiate FTP connection
        with FTP() as ftp:
            ftp.connect(self.ARKTIKA_M1_URL_HOSTNAME, self.ARKTIKA_M1_FTP_PORT)
            self._logger.debug("Connecting to FTP server at: " + self.ARKTIKA_M1_URL_HOSTNAME \
                + ":" + str(self.ARKTIKA_M1_FTP_PORT) + ".")
            
            ftp.login(self.ARKTIKA_M1_USERNAME, self.ARKTIKA_M1_PASSWORD)
            self._logger.debug("Logging into FTP server with credentials: " + self.ARKTIKA_M1_USERNAME \
                + ":" + self.ARKTIKA_M1_PASSWORD + ".")

            base_dir = self.ARKTIKA_M1_FTP_BASE_DIRECTORY + '/' + year + '/' + translated_month
            ftp.cwd(base_dir)
            self._logger.debug("Changed directory to: " + base_dir + ".")

            # If days is empty, get the list of days in the current directory
            if not days:
                days = ftp.nlst()
            
            # Iterate over each day and get the links for each day, aggregating them into the links map
            for day in days:
                tmp_links = self.extract_links_for_day(ftp, year, translated_month, day, utc_range)
                self._logger.debug("Changed directory back to: " + base_dir + ".")
                links = {**tmp_links, **links}
        self._logger.debug("Closing connection to FTP server at: " + self.ARKTIKA_M1_URL_HOSTNAME \
                + ":" + str(self.ARKTIKA_M1_FTP_PORT) + ".")

        return links


    def extract_links_for_day(self, ftp, year, translated_month, day, utc_range=[]):
        """
        Extracts and retrieves the file links for a given day within a utc_range. If the utc_range
        is provided, each utc_time will be compared to determine whether the time is within the range.
        Otherwise, all utc_times will be retrieved with all of the files associated in the share.

        @param ftp: FTP - An FTP object to traverse the ARKTIKA_M1 FTP share.
        @param year: str - The current year.
        @param translated_month: str - A string in Russian representing the current month.
        @param days: str - A string representing some day of the month. 
        @param utc_range: [] - A list of utc times in HHMM format to set the time range of returned links.
        @return links: {} - A key-value mapping of a title key in a standard format and its appropriate image link.
        """

        links = {}
        
        # Enter the valid day directory and get the list of all the utc_times available
        ftp.cwd(day)
        self._logger.debug("Changed directory to: " + day + ".")
        utc_times = ftp.nlst()
        
        # For each utc_time if its within range get the files & create links
        for utc_time in utc_times:
            files = []
            time_map = utc_time.split('.')
            curr_time = time_map[0] + time_map[1]
            
            # If the current time is not within the utc_range, skip over it
            if curr_time not in utc_range and utc_range:
                self._logger.debug("UTC time " + time_map[0] + "-" + time_map[1] + " UTC is not within provided UTC range.")
                continue

            # Enter the valid utc directory and get the list of all the files
            ftp.cwd(utc_time)
            self._logger.debug("Changed directory to: " + utc_time + ".")

            files = ftp.nlst()
            
            # For each file, generate the title and link & insert into links map
            for file in files:
                # Get time from file and parse into datetime for better readability
                time = file.split('_')[2]
                fmt = '%Y%m%d%H%M%S'
                date = datetime.strptime(time, fmt).date()
                
                # Create title for given file
                title = 'Band ' + file.split('.')[0][-2:] + ' - ' + date.strftime('%Y-%m-%d') + \
                    ' - ' + time_map[0] + '-' + time_map[1] + ' UTC'
                
                # Create latin-1 decoded link for file
                link = (self.ARKTIKA_M1_URL + '/' + year + '/' + translated_month + '/' + day + \
                    '/' + utc_time + '/' + file)
                
                self._logger.debug("Scraped link " + link + " for image " + title + ".")

                # Insert title and link into links map
                links[title] = link
            # Navigate back one directory
            ftp.cwd('..')
            self._logger.debug("Changed directory back to: " + day + ".")
        # Navigate back one directory
        ftp.cwd('..')

        return links


    def __get_russian_utc_time(self):
        """
        A private method which generates the UTC datetime object which is 3 hours ahead of typical UTC time.
        The UTC datetime object will either be set at the 30 minute mark or the 00 minute mark dependent upon
        the current time. The ARKTIKA-M1 FTP server uploads images in half hourish intervals.

        @return utctime: datetime - A datetime object containing russian UTC time.
        """

        # Get current time in MOSCOW
        time_zone = pytz.timezone(self.MOSCOW_TIME_ZONE)
        country_time = datetime.now(time_zone)
        utctime = country_time.utcnow()
        
        # Russia operates +3 hours ahead of UTC time.
        difference = timedelta(hours = 3)
        utctime += difference
        
        # FTP server pushes files every half hourish in UTC time.
        if utctime.minute > self.HALF_HOUR_MARK:
            difference = timedelta(minutes = (utctime.minute - self.HALF_HOUR_MARK))
            utctime -= difference
        else:
            difference = timedelta(minutes = utctime.minute)
            utctime -= difference
        
        return utctime


    def __get_date_fields(self, utctime):
        """
        A private method which generates the necessary date fields required for building 
        link path and standardized title.

        @param utctime: datetime - A datetime object containing the current russian UTC time.
        @return year, month: str - Strings representing the year and month respectively.
        """

        year = utctime.strftime('%Y') # YYYY
        month = utctime.strftime('%B') # January
        
        return year, month


    def _create_img_dir(self, title):
        """
        Protected abstract method implementation which is called during the base SatelliteCrawlers' pulldown_images
        method. This method is to generate the directory string path of where an image should be placed or already
        exists.

        @param title: str - A string containing the following standard format: 'TITLE - DATE - HH-MM UTC'
        which describes the image being queried.
        @return dir_path: str - A directory string containing the following standard format: 'ARKTIKA-M1/DATE/HH-MM UTC/TITLE'
        where the image downloaded should be placed, or already has been placed.
        """

        dir_path = ""

        today = re.split(self.TITLE_DELIMITER, title)[1]
        utctime = re.split(self.TITLE_DELIMITER, title)[-1].replace(":", "-")

        dir_path = self.ARKTIKA_M1_DIRECTORY + "/" + str(today) + "/" + utctime + "/" + title
        
        self._logger.debug("Image directory path for title " + title + ": " + dir_path + ".")

        return dir_path


    def create_satellite_directory(self):
        """
        Implemented public abstract method which creates a high-level directory with the static 
        ARKTIKA_M1_DIRECTORY string if it does not exist.
        """

        if not os.path.exists(self.ARKTIKA_M1_DIRECTORY):
            self._logger.debug("Creating directory at path: " + self.ARKTIKA_M1_DIRECTORY)
            os.makedirs(self.ARKTIKA_M1_DIRECTORY)