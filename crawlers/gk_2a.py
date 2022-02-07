import os
import re
import sys
import pytz
from datetime import datetime, timedelta
from crawlers.satellite_crawler import SatelliteCrawler

class GEO_KOMPSAT_2A(SatelliteCrawler):
    """
    Concrete satellite spider class for GEO-KOMPSAT-2A which extends the base class, SatelliteCrawler.
    This method of splitting spiders into separate classes will help with keeping longevity of spider 
    runner classes and update issues easier that may occur during website HTML updates. This spider hierarchy
    requires using the Tor network and using the default settings (including ControlPort) to access the network.

    @author Vincent.Nigro
    @version 0.0.1
    @modified 1/29/21
    """

    SEOUL_TIME_ZONE = 'Asia/Seoul'
    GEO_KOMPSAT_2A_IMG_FOOTER = 'ge_'
    GEO_KOMPSAT_2A_DIRECTORY = 'GEO-KOMPSAT-2A'
    GEO_KOMPSAT_2A_IMG_HEADER = 'gk2a_ami_le1b_'
    GEO_KOMPSAT_2A_URL = 'http://nmsc.kma.go.kr/IMG/GK2A/AMI/PRIMARY/L1B/COMPLETE/FD/'
    GEO_KOMPSAT_2A_IMG_SET = ['vi004_fd010', 'vi005_fd010', 'vi006_fd005', 'vi008_fd010', 'nr013_fd020', 'nr016_fd020', \
        'sw038_fd020', 'wv063_fd020', 'wv069_fd020', 'wv073_fd020', 'ir087_fd020', 'ir096_fd020', 'ir105_fd020', 'ir112_fd020', \
        'ir123_fd020', 'ir133_fd020', 'rgb-true_fd010', 'rgb-natural_fd020', 'rgb-airmass_fd020', 'rgb-dust_fd020', \
        'rgb-daynight_fd020', 'rgb-fog_fd020', 'rgb-storm_fd020', 'rgb-snowfog_fd020','rgb-cloud_fd020','rgb-ash_fd020', \
        'enhc-wv063_fd020', 'enhc-wv069_fd020', 'enhc-wv073_fd020', 'enhc-color-ir105_fd020']

    def __init__(self, url, satellite):
        """
        A concrete constructor which accepts a full base path to a URL to begin crawl, satellite name, and
        an appropriate resolution size to search for during crawl process.
        
        @param url: str - A string containing a full URL path to some website to begin web crawl.
        @param satellite: str - A string containing a representative name for the GEO-KOMPSAT-2A satellite 
        crawler.
        """

        super().__init__(url, satellite)


    def get_links(self, pw):
        """
        Implemented abstract public method which performs GEO_KOMPSAT_2A specific base page extraction and extraction
        of links from the appropriate containing objects.

        @param pw: str - A string containing the Tor password for the given system configuration.
        @return links: {} - A key-value mapping of a title key in a standard format and its appropriate image link
        """

        links = {}
        
        # Gets UTC time and date as YYYY-MM-DD HH MM
        utctime = self.__generate_utctime()

        # Extract date and UTC time fields        
        time_fields = utctime.split(' ')
        date = time_fields[0]
        hour = time_fields[1]
        minute = time_fields[2]
        
        # Extract sub fields within date
        date_fields = date.split('-')
        year = date_fields[0]
        month = date_fields[1]
        day = date_fields[2]

        # Build full URL paths for each possible image type for the given time
        for image in self.GEO_KOMPSAT_2A_IMG_SET:
            relative_path = year + month + '/' + day + '/' + hour + '/' + self.GEO_KOMPSAT_2A_IMG_HEADER + \
                image + self.GEO_KOMPSAT_2A_IMG_FOOTER + year + month + day + hour + minute + '.png'
            title = self.__generate_title(image, year, month, day, hour, minute)
            links[title] = self.GEO_KOMPSAT_2A_URL + relative_path
        
        return links


    def __generate_title(self, img, year, month, day, hour, minute):
        """
        A private method which generates a standardized title format to be used as a directory to contain the
        linked image as well as other processing done by the standard pulldown procedure.

        @param year: str - A year formated as YYYY ex: 2021.
        @param month: str - Digits representing month ex: 01.
        @param day: str - A string digit representing the day ex: 25.
        @param hour: str - A string formatted as HH ex: 07.
        @param minute: str - A string formatted as MM ex: 30.
        @return title: str - A title with a standardized format such as: True Color - 30 01 2021 - 03-30 UTC
        """
        
        title = ''
        date = day + ' ' + month + ' ' + year
        utc = hour + '-' + minute + ' ' + self.UTC_STRING

        if img == 'vi004_fd010':
            title = 'VIS 0.47µm - ' + date + ' - ' + utc
        elif img == 'vi005_fd010':
            title = 'VIS 0.51µm - ' + date + ' - ' + utc
        elif img == 'vi006_fd005':
            title = 'VIS 0.64µm - ' + date + ' - ' + utc
        elif img == 'vi008_fd010':
            title = 'VIS 0.86µm - ' + date + ' - ' + utc
        elif img == 'nr013_fd020':
            title = 'NIR 1.37µm - ' + date + ' - ' + utc
        elif img == 'nr016_fd020':
            title = 'NIR 1.6µm - ' + date + ' - ' + utc
        elif img == 'sw038_fd020':
            title = 'SWIR 3.8µm - ' + date + ' - ' + utc
        elif img == 'wv063_fd020':
            title = 'WV 6.3µm - ' + date + ' - ' + utc
        elif img == 'wv069_fd020':
            title = 'WV 6.9µm - ' + date + ' - ' + utc
        elif img == 'wv073_fd020':
            title = 'WV 7.3µm - ' + date + ' - ' + utc
        elif img == 'ir087_fd020':
            title = 'IR 8.7µm - ' + date + ' - ' + utc
        elif img == 'ir096_fd020':
            title = 'IR 9.6µm - ' + date + ' - ' + utc
        elif img == 'ir105_fd020':
            title = 'IR 10.5µm - ' + date + ' - ' + utc
        elif img == 'ir112_fd020':
            title = 'IR 11.2µm - ' + date + ' - ' + utc
        elif img == 'ir123_fd020':
            title = 'IR 12.3µm - ' + date + ' - ' + utc
        elif img == 'ir133_fd020':
            title = 'IR 13.3µm - ' + date + ' - ' + utc
        elif img == 'rgb-true_fd010':
            title = 'True Color - ' + date + ' - ' + utc
        elif img == 'rgb-natural_fd020':
            title = 'Natural Color - ' + date + ' - ' + utc
        elif img == 'rgb-airmass_fd020':
            title = 'AirMass RGB - ' + date + ' - ' + utc
        elif img == 'rgb-dust_fd020':
            title = 'Dust RGB - ' + date + ' - ' + utc
        elif img == 'rgb-daynight_fd020':
            title = 'Daynight RGB - ' + date + ' - ' + utc
        elif img == 'rgb-fog_fd020':
            title = 'Fog RGB - ' + date + ' - ' + utc
        elif img == 'rgb-storm_fd020':
            title = 'Storm RGB - ' + date + ' - ' + utc
        elif img == 'rgb-snowfog_fd020':
            title = 'Snowfog RGB - ' + date + ' - ' + utc
        elif img == 'rgb-cloud_fd020':
            title = 'Cloud RGB - ' + date + ' - ' + utc
        elif img == 'rgb-ash_fd020':
            title = 'Ash RGB - ' + date + ' - ' + utc
        elif img == 'enhc-wv063_fd020':
            title = 'Enhanced IR WV 6.3µm - ' + date + ' - ' + utc
        elif img == 'enhc-wv069_fd020':
            title = 'Enhanced IR WV 6.9µm - ' + date + ' - ' + utc
        elif img == 'enhc-wv073_fd020':
            title = 'Enhanced IR WV 7.3µm - ' + date + ' - ' + utc
        elif img == 'enhc-color-ir105_fd020':
            title = 'Enhanced IR 10.5µm - ' + date + ' - ' + utc

        return title


    def __generate_utctime(self):
        """
        A private method which generates a UTC time and date based on the time currently in South Korea (Seoul). 
        Once the time is determined, 20 extra minutes are removed from the current time to ensure all links 
        will have images loaded at the proper time.

        @return utctime: str - A string of format YYYY-MM-DD HH MM where HH and MM were in UTC time.
        """

        # Get current time in SEOUL
        time_zone = pytz.timezone(self.SEOUL_TIME_ZONE)
        country_time = datetime.now(time_zone)
        utctime = country_time.utcnow()
        
        # Remove 20 minutes from current time properly dependent upon current minute tick.
        if utctime.minute >= 0 and utctime.minute <= 10:
            difference = timedelta(minutes = utctime.minute)
            utctime -= difference
            difference = timedelta(hours = 1, minutes = 20)
            utctime -= difference
        elif utctime.minute >= 10 and utctime.minute <= 19:
            difference = timedelta(minutes = utctime.minute)
            utctime -= difference
            difference = timedelta(hours = 1, minutes = 10)
            utctime -= difference
        elif utctime.minute >= 20 and utctime.minute <= 29:
            difference = timedelta(minutes = utctime.minute)
            utctime -= difference
        elif utctime.minute >= 30 and utctime.minute <= 39:
            difference = timedelta(minutes = utctime.minute)
            utctime -= difference
            difference = timedelta(minutes = 10)
            utctime += difference
        elif utctime.minute >= 40 and utctime.minute <= 49:
            difference = timedelta(minutes = utctime.minute)
            utctime -= difference
            difference = timedelta(minutes = 20)
            utctime += difference
        elif utctime.minute >= 50 and utctime.minute <= 59:
            difference = timedelta(minutes = utctime.minute)
            utctime -= difference
            difference = timedelta(minutes = 30)
            utctime += difference

        # Remove extra 10 minutes off to make sure images are there.
        if (utctime.minute == 0):
            difference = timedelta(hours = 1)
            utctime -= difference
            difference = timedelta(minutes = 50)
            utctime += difference
        else:
            difference = timedelta(minutes = 10)
            utctime -= difference
        
        # Removes fractions of second field from utctime 
        utctime = str(utctime).split('.')[0]
        
        # Creates list and removes last element containing seconds
        utctime = utctime.split(':')[:-1]
        
        # Joins list back as string separated with a space
        utctime = " ".join(utctime)
        print(utctime)
        return utctime


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

        dir_path = self.GEO_KOMPSAT_2A_DIRECTORY + "/" + str(today) + "/" + utctime + "/" + title
        
        return dir_path


    def create_satellite_directory(self):
        """
        Implemented public abstract method which creates a high-level directory with the static 
        GEO_KOMPSAT_2A_DIRECTORY string if it does not exist.
        """
        
        if not os.path.exists(self.GEO_KOMPSAT_2A_DIRECTORY):
            os.makedirs(self.GEO_KOMPSAT_2A_DIRECTORY)