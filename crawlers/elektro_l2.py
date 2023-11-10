import re
import os
import pytz
from ftplib import FTP
from datetime import datetime, timedelta
from crawlers.satellite_crawler import SatelliteCrawler

class ELEKTRO_L2(SatelliteCrawler):
    """
    Concrete satellite spider class for ELEKTRO-L2 which extends the base class, SatelliteCrawler.
    This method of splitting spiders into separate classes will help with keeping longevity of spider 
    runner classes and update issues easier that may occur during website HTML updates. This spider requires
    using FTP in order to extract the latest hi-res image for the ELEKTRO-L2 spacecraft via the ntsomz.gptl.ru
    FTP server.

    @author Vincent.Nigro
    @version 0.0.2
    @modified 10/10/23
    """
    
    HALF_HOUR_MARK = 30
    ELEKTRO_L2_FTP_PORT = 2121
    ELEKTRO_L2_USERNAME = 'electro'
    ELEKTRO_L2_PASSWORD = 'electro'
    MOSCOW_TIME_ZONE = 'Europe/Moscow'
    ELEKTRO_L2_DIRECTORY = 'ELEKTRO-L2'
    ELEKTRO_L2_URL_HOSTNAME = 'ntsomz.gptl.ru'
    ELEKTRO_L2_FTP_BASE_DIRECTORY = 'ELECTRO_L_2'
    ELEKTRO_L2_URL = 'ftp://electro:electro@ntsomz.gptl.ru:2121/ELECTRO_L_2'

    def __init__(self, url, satellite, day, utcrange):
        """
        A concrete constructor which accepts a full base path to a URL to begin crawl, satellite name, and
        an appropriate resolution size to search for during crawl process.
        
        @param url: str - A string containing a full URL path to some website to begin web crawl.
        @param satellite: str - A string containing a representative name for the ELEKTRO-L2 satellite crawler.
        """

        super().__init__(url, satellite)
        self.__day = day
        self.__utcrange = utcrange

    def get_links(self, pw):
        """
        Implemented abstract public method which performs ELEKTRO-L2 specific processing for creating the appropriate
        time information required for querying the Russian ntsomz.gptl.ru FTP server.

        @param pw: str - A string containing the Tor password for the given system configuration.
        @return links: {} - A key-value mapping of a title key in a standard format and its appropriate image link.
        """

        days = []
        links = {}

        if self.__utcrange != "" and self.__day != "":
            days.append(self.__day)
            links = self.extract_links(utc_range=self.__utcrange, days=days)
        elif self.__utcrange != "":
            links = self.extract_links(utc_range=self.__utcrange)
        elif self.__day != "":
            days.append(self.__day)
            links = self.extract_links(days)
        else:
            links = self.extract_links()

        self._logger.debug("Generated links: ")
        self._logger.debug(links)

        return links

    def extract_links(self, days=[], utc_range=[]):
        """
        Extracts and retrieves the file links for a set of days, within a utc_range. This will initiate
        the FTP connection to the ELECTRO-L2 server and begin traversing the directories for the current
        month.

        @param days: [] - A list representing a single day; if empty it means retrieve all days.
        @param utc_range: [] - A list of utc times in HHMM format to set the time range of returned links.
        @return links: {} - A key-value mapping of a title key in a standard format and its appropriate image link.
        """

        links = {}

        # Get current utc time of russia
        utctime = self.__get_russian_utc_time()
        self._logger.debug("Approximate current russian utc time is: " + utctime.strftime("%x - %X"))

        # Extract each field required for run
        year, month = self.__get_date_fields(utctime)
        self._logger.debug("Current year: " + year)
        self._logger.debug("Current month: " + month)

        # Initiate FTP connection
        with FTP() as ftp:
            ftp.connect(self.ELEKTRO_L2_URL_HOSTNAME, self.ELEKTRO_L2_FTP_PORT)
            self._logger.debug("Connecting to FTP server at: " + self.ELEKTRO_L2_URL_HOSTNAME \
                               + ":" + str(self.ELEKTRO_L2_FTP_PORT) + ".")

            ftp.login(self.ELEKTRO_L2_USERNAME, self.ELEKTRO_L2_PASSWORD)
            self._logger.debug("Logging into FTP server with credentials: " + self.ELEKTRO_L2_USERNAME \
                               + ":" + self.ELEKTRO_L2_PASSWORD + ".")
            base_dir = self.ELEKTRO_L2_FTP_BASE_DIRECTORY + '/' + year + '/' + month
            ftp.cwd(base_dir)
            self._logger.debug("Changed directory to: " + base_dir + ".")

            # If days is empty, get the list of days in the current directory
            if not days:
                days = ftp.nlst()

            # Iterate over each day and get the links for each day, aggregating them into the links map
            for day in days:
                tmp_links = self.extract_links_for_day(ftp, year, month, day, utc_range)
                self._logger.debug("Changed directory back to: " + base_dir + ".")
                links = {**tmp_links, **links}
        self._logger.debug("Closing connection to FTP server at: " + self.ELEKTRO_L2_URL_HOSTNAME \
                           + ":" + str(self.ELEKTRO_L2_FTP_PORT) + ".")

        return links

    def extract_links_for_day(self, ftp, year, month, day, utc_range=[]):
        """
        Extracts and retrieves the file links for a given day within a utc_range. If the utc_range
        is provided, each utc_time will be compared to determine whether the time is within the range.
        Otherwise, all utc_times will be retrieved with all of the files associated in the share.

        @param ftp: FTP - An FTP object to traverse the ELECTRO_L_2 FTP share.
        @param year: str - The current year.
        @param month: str - A string representing the current month.
        @param day: str - A string representing some day of the month.
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

            # If the current time is not within the utc_range, skip over it
            if utc_time not in utc_range and utc_range:
                self._logger.debug(
                    "UTC time " + utc_time[0:2] + "-" + utc_time[2:4] + " UTC is not within provided UTC range.")
                continue

            self._logger.debug("Generating titles and links for files captured for UTC Time: " + utc_time)

            # Enter the valid utc directory and get the list of all the files
            ftp.cwd(utc_time)
            self._logger.debug("Changed directory to: " + utc_time + ".")

            files = ftp.nlst()

            # For each file, generate the title and link & insert into links map
            for file in files:
                # Skip over any zip files
                if file.endswith('.zip'):
                    continue

                self._logger.debug("Generating title and link for file: " + file)

                # Get time from file and parse into datetime for better readability
                time = file.split('_')
                time = time[0] + time[1]
                self._logger.debug("Captured time value from file name: " + time)

                # Insert captured string time into datetime object with associated time format
                date = datetime.strptime(time, '%y%m%d%H%M').date()

                # Get image type in file name
                img_type = file.split('.')[0]
                img_type = img_type.split('_')[2:]
                img_type = "_".join(img_type)
                img_type = img_type.lower().replace("_", " ").title()

                if img_type.isdigit():
                    img_type = "Band " + img_type

                self._logger.debug("Generated image type of: " + img_type)

                # Create title for given file
                title = img_type + ' - ' + date.strftime('%Y-%m-%d') + \
                        ' - ' + utc_time[0:2] + '-' + utc_time[2:4] + ' UTC'

                # Create link for file
                link = (self.ELEKTRO_L2_URL + '/' + year + '/' + month + '/' + day + \
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
        difference = timedelta(hours=3)
        utctime += difference
        
        # FTP server pushes files every half hour in UTC time.
        if utctime.minute > self.HALF_HOUR_MARK:
            difference = timedelta(minutes=(utctime.minute - self.HALF_HOUR_MARK))
            utctime -= difference
        else:
            difference = timedelta(minutes=utctime.minute)
            utctime -= difference
        
        return utctime

    def __get_date_fields(self, utctime):
        """
        A private method which generates the necessary date fields required for building 
        link path and standardized title.

        @param utctime: datetime - A datetime object containing the current russian UTC time.
        @return year, month: str - Strings representing the year and month respectively.
        """

        year = utctime.strftime('%Y')  # YYYY
        month = utctime.strftime('%B')  # January

        return year, month

    def _create_img_dir(self, title):
        """
        Protected abstract method implementation which is called during the base SatelliteCrawlers' pulldown_images
        method. This method is to generate the directory string path of where an image should be placed or already
        exists.

        @param title: str - A string containing the following standard format: 'TITLE - DATE - HH-MM UTC'
        which describes the image being queried.
        @return dir_path: str - A directory string containing the following standard format: 'ELEKTRO-L2/DATE/HH-MM UTC/TITLE'
        where the image downloaded should be placed, or already has been placed.
        """

        dir_path = ""

        today = re.split(self.TITLE_DELIMITER, title)[1]
        utctime = re.split(self.TITLE_DELIMITER, title)[-1].replace(":", "-")

        dir_path = self.ELEKTRO_L2_DIRECTORY + "/" + str(today) + "/" + utctime + "/" + title
        
        self._logger.debug("Image directory path for title " + title + ": " + dir_path + ".")

        return dir_path

    def create_satellite_directory(self):
        """
        Implemented public abstract method which creates a high-level directory with the static 
        ELEKTRO_L2_DIRECTORY string if it does not exist.
        """

        if not os.path.exists(self.ELEKTRO_L2_DIRECTORY):
            self._logger.debug("Creating directory at path: " + self.ELEKTRO_L2_DIRECTORY)
            os.makedirs(self.ELEKTRO_L2_DIRECTORY)