import re
import os
from time import mktime, gmtime
from datetime import datetime, timedelta
from crawlers.satellite_crawler import SatelliteCrawler

class INSAT_3DR(SatelliteCrawler):
    """
    Concrete satellite spider class for INSAT-3DR which extends the base class, SatelliteCrawler.
    This method of splitting spiders into separate classes will help with keeping longevity of spider 
    runner classes and update issues easier that may occur during website HTML updates. This spider hierarchy
    requires using the Tor network and using the default settings (including ControlPort) to access the network.

    @author Vincent.Nigro
    @version 0.0.2
    @modified 8/21/22
    """

    INSAT_3DR_IMG = '3RIMG'
    GMT_TIME_ZONE = 'Etc/GMT'
    INSAT_3DR_DIRECTORY = 'INSAT-3DR'
    GMT_PRINT_FORMAT = '%Y-%m-%d %H:%M GMT'
    INSAT_3DR_URL = 'http://satellite.imd.gov.in/ImageArchive/3RIMG'
    IMAGE_PATHS = {'Infrared 10.8µm': 'L1B_STD_IR1_V01R00', 'Visible': 'L1B_STD_VIS_V01R00',
    'Shortwave Infrared 1.625µm': 'L1B_STD_SWIR_V01R00', 'Middlewave Infrared 3.9µm': 'L1B_STD_MIR_V01R00',
    'Middlewave Infrared Temperature 3.9µm': 'L1B_STD_MIR_TEMP_V01R00', 'Water Vapor': 'L1B_STD_WV_V01R00',
    'Water Vapor Temperature': 'L1B_STD_WV_TEMP_V01R00', 'Infrared Temperature 10.8µm': 'L1B_STD_IR1_TEMP_V01R00',
    'Infrared 12.0µm': 'L1B_STD_IR2_V01R00', 'Infrared Temperature 12.0µm': 'L1B_STD_IR2_TEMP_V01R00',
    'Day Night Microphysics': 'L1B_STD_MP_V01R00', 'Outgoing Longwave Radiation': 'L2B_OLR_V01R00',
    'SST Regression': 'L2B_SST_REG_V02R00', 'Land Surface Temperature': 'L2B_LST_V01R00',
    'Upper Troposphere Humidity': 'L2B_UTH_V01R00', 'Hydro Estimator Precipitation': 'L2B_HEM_V01R00',
    'IMSRA (Improved)': 'L2B_IMC_V01R00', 'Cloud Top Temperature': 'L2B_CTT_V01R00', 'Cloud Top Pressure': 'L2B_CTP_V01R00',
    'Total Precipitable Water': 'L2B_TPW_V01R00', 'Cloud Mask': 'L2B_CMK_V01R00'}

    def __init__(self, url, satellite):
        """
        A concrete constructor which accepts a full base path to a URL to begin crawl, satellite name, and
        an appropriate resolution size to search for during crawl process.
        
        @param url: str - A string containing a full URL path to some website to begin web crawl.
        @param satellite: str - A string containing a representative name for the INSAT-3DR satellite crawler.
        """

        super().__init__(url, satellite)
    
    def get_links(self, pw):
        """
        Implemented abstract public method which performs INSAT-3DR specific base page extraction and extraction
        of links from the appropriate containing objects.

        @param pw: str - A string containing the Tor password for the given system configuration.
        @return links: {} - A key-value mapping of a title key in a standard format and its appropriate image link.
        """
        links = {}

        # Get an adjusted GMT time that is about 1 hour behind the current
        max_gmt_time = self.__get_adjusted_gmttime()
        min_gmt_time = max_gmt_time
        min_gmt_time -= timedelta(hours = 12)

        self._logger.debug("Max GMT Time: " + max_gmt_time.strftime(self.GMT_PRINT_FORMAT))
        self._logger.debug("Min GMT Time: " + min_gmt_time.strftime(self.GMT_PRINT_FORMAT))

        while min_gmt_time < max_gmt_time:
            # Get tuple of date fields needed for generating links
            date_fields = self.__get_date_fields(min_gmt_time)
            
            # Create link for each image type for current min gmt time
            for type, sublink in self.IMAGE_PATHS.items():
                title = self.__generate_title(type, date_fields)
                links[title] = self.get_url() + '/' + date_fields[0] + '/' + date_fields[1].upper() + '/' + \
                    self.INSAT_3DR_IMG + '_' + date_fields[2] + date_fields[1].upper() + date_fields[0] + '_' + \
                    date_fields[3] + date_fields[4] + '_' + sublink + '.jpg'
            
            # Add 30 minutes to min time
            min_gmt_time += timedelta(minutes = 30)

        return links


    def __get_date_fields(self, utctime):
        """
        A private method which generates the necessary date fields required for building 
        link path and standardized title.

        @param utctime: datetime - A datetime object containing the current russian UTC time.
        @return day, month, year, hour, minute
        """

        year = utctime.strftime('%Y') # YYYY
        month = utctime.strftime('%b') # Aug
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
        
        gmt_time = datetime.fromtimestamp(mktime(gmtime()))
        gmt_time -= timedelta(hours = 1, minutes = gmt_time.minute)

        if gmt_time.minute >= 0 and gmt_time.minute <= 15 or \
            gmt_time.minute >= 15 and gmt_time.minute <= 45:    
            gmt_time += timedelta(minutes = 15)
        elif gmt_time.minute > 45 and gmt_time.minute <= 59:
            gmt_time += timedelta(minutes = 45)
        
        # Returns a GMT timezone based timestamp which is represented by the Mosdac imagery jpg's
        return gmt_time


    def _create_img_dir(self, title):
        """
        Protected abstract method implementation which is called during the base SatelliteCrawlers' pulldown_images
        method. This method is to generate the directory string path of where an image should be placed or already
        exists.

        @param title: str - A string containing the following standard format: 'TITLE - DATE - HH-MM GMT'
        which describes the image being queried.
        @return dir_path: str - A directory string containing the following standard format: 'INSAT-3DR/DATE/HH-MM GMT/TITLE'
        where the image downloaded should be placed, or already has been placed.
        """

        dir_path = ""
        
        today = re.split(self.TITLE_DELIMITER, title)[1]
        time = re.split(self.TITLE_DELIMITER, title)[-1].replace(':', '-')

        dir_path = self.INSAT_3DR_DIRECTORY + os.sep + str(today) + os.sep + time + os.sep + title
        
        self._logger.debug("Image directory path for title " + title + ": " + dir_path + ".")

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

        self._logger.debug("Generated title \"" + title + "\" with parameters: " + my_type + ", " + str(date_fields) + ".")
        
        return title


    def create_satellite_directory(self):
        """
        Creates a high-level directory with the static INSAT_3DR_DIRECTORY string if it does not exist.
        """

        if not os.path.exists(self.INSAT_3DR_DIRECTORY):
            self._logger.debug("Creating directory at path: " + self.INSAT_3DR_DIRECTORY)
            os.makedirs(self.INSAT_3DR_DIRECTORY)