import re
import os
from datetime import datetime, timedelta
from crawlers.satellite_crawler import SatelliteCrawler

class METEOSAT_11(SatelliteCrawler):
    """
    Concrete satellite spider class for METEOSAT-11 which extends the base class, SatelliteCrawler.
    This method of splitting spiders into separate classes will help with keeping longevity of spider 
    runner classes and update issues easier that may occur during website HTML updates. This spider hierarchy
    requires using the Tor network and using the default settings (including ControlPort) to access the network.

    @author Vincent.Nigro
    @version 0.0.1
    @modified 2/8/21
    """

    TIMES_3_ZOOM = '03'
    METEOSAT_11_DIRECTORY = 'METEOSAT-11'
    METEOSAT_11_BASE_FULL_DISK = 'meteosat-11---full_disk'
    METEOSAT_11_URL = 'https://rammb-slider.cira.colostate.edu/data/imagery/'

    # Dictionary containing key of image title presented in link to presentation title
    IMAGE_TITLES = {'band_01': 'Band 1', 'band_02': 'Band 2', 'band_03': 'Band 3', 'band_04': 'Band 4', 'band_05': 'Band 5', 'band_06': 'Band 6', 'band_07': 'Band 7', 
        'band_08': 'Band 8', 'band_09': 'Band 9', 'band_10': 'Band 10', 'band_11': 'Band 11', 'geocolor': 'GeoColor', 'natural_color': 'Natural Color', 'rgb_air_mass': 'RGB AirMass', 
        'jma_day_cloud_phase_distinction_rgb': 'Day Cloud Phase Distinction', 'eumetsat_nighttime_microphysics': 'Nighttime Microphysics', 'awips_dust': 'Dust', 'eumetsat_ash': 'Ash'}

    # Dictionary containing key of image title presented in link to zoom level for each image.
    IMAGE_PATHS = {'band_01': TIMES_3_ZOOM, 'band_02': TIMES_3_ZOOM, 'band_03': TIMES_3_ZOOM, 'band_04': TIMES_3_ZOOM, 'band_05': TIMES_3_ZOOM,
        'band_06': TIMES_3_ZOOM, 'band_07': TIMES_3_ZOOM, 'band_08': TIMES_3_ZOOM, 'band_09': TIMES_3_ZOOM, 'band_10': TIMES_3_ZOOM, 'band_11': TIMES_3_ZOOM,
        'geocolor': TIMES_3_ZOOM, 'natural_color': TIMES_3_ZOOM, 'rgb_air_mass': TIMES_3_ZOOM, 'jma_day_cloud_phase_distinction_rgb': TIMES_3_ZOOM, 
        'eumetsat_nighttime_microphysics': TIMES_3_ZOOM, 'awips_dust': TIMES_3_ZOOM, 'eumetsat_ash': TIMES_3_ZOOM}
    
    def __init__(self, url, satellite):
        """
        A concrete constructor which accepts a full base path to a URL to begin crawl, satellite name, and
        an appropriate resolution size to search for during crawl process.
        
        @param url: str - A string containing a full URL path to some website to begin web crawl.
        @param satellite: str - A string containing a representative name for the METEOSAT-11 satellite crawler.
        """

        super().__init__(url, satellite)


    def get_links(self, pw):
        """
        Implemented abstract public method which performs METEOSAT-11 specific base page extraction and extraction
        of links from the appropriate containing objects.

        @param pw: str - A string containing the Tor password for the given system configuration.
        @return links: {} - A key-value mapping of a title key in a standard format and its appropriate image link.
        """
        links = {}

        # Generates a UTC time an hour back from the current time
        utctime = self.__get_adjusted_utctime()

        # Removes fractions of second field from utctime 
        short_utctime = str(utctime).split('.')[0]
        
        # Creates list and removes last element containing seconds
        short_utctime = short_utctime.split(':')[:-1]
        
        # Joins list back as string separated with a space
        short_utctime = short_utctime[0] + ':' + short_utctime[1] + ' UTC'
        
        year, month, day, hour, minute = self.__get_date_fields(utctime)

        # Build date properties needed to build links
        date_link = year + month + day # 20210131
        date_time_link = date_link + hour + minute + '00' # 20210131204000

        # Generate max 8x8 images ranging from 000_000.png to 007_007.png
        my_range = []
        for i in range(0, 8):
            for j in range(0, 8):
                if i > 9 and j < 10:
                    my_range.append('0' + str(i) +  '_00' + str(j) + '.png')
                elif i < 10 and j < 10:
                    my_range.append('00' + str(i) +  '_00' + str(j) + '.png')
                elif i < 10 and j > 9:
                    my_range.append('00' + str(i) +  '_0' + str(j) + '.png')

        # Build necesary paths for each image
        for type_path, zoom in self.IMAGE_PATHS.items():
            i = 0
            j = 0
            for r in my_range:
                # If band type, images are updated hourly, otherwise every 15 minutes.
                if 'band' in type_path:
                    difference = timedelta(minutes = utctime.minute)
                    utctime -= difference
                    
                    formatted_utc = str(utctime).split('.')[0]
                    formatted_utc = formatted_utc.split(':')[:-1]
                    formatted_utc = formatted_utc[0] + ':' + formatted_utc[1] + ' UTC'
                    
                    title = self.__generate_title(type_path, formatted_utc, r)
                    hourly_datetime_link = date_link + hour + '0000'

                    links[title] = self.get_url() + date_link + '/' + self.METEOSAT_11_BASE_FULL_DISK + \
                        '/' + type_path + '/' + hourly_datetime_link + '/' + zoom + '/' + r
                else:
                    title = self.__generate_title(type_path, short_utctime, r)
                    links[title] = self.get_url() + date_link + '/' + self.METEOSAT_11_BASE_FULL_DISK + \
                        '/' + type_path + '/' + date_time_link + '/' + zoom + '/' + r
                
                i += 1

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


    def __get_adjusted_utctime(self):
        """
        Creates a UTC time that is an hour behind the current time to ensure that the images are still
        present on the web server.
        
        @return utctime: datetime - A datetime object containing the current UTC time behind by one hour.
        """
        
        time = datetime.now()
        utctime = time.utcnow()
        
        # Always take off two hours off time to ensure images will always be available.
        if utctime.minute >= 0 and utctime.minute <= 14:
            difference = timedelta(hours = 2, minutes = utctime.minute)
            utctime -= difference
        elif utctime.minute >= 15 and utctime.minute <= 29:
            difference = timedelta(hours = 2, minutes = utctime.minute)
            utctime -= difference
            difference = timedelta(minutes = 15)
            utctime += difference 
        elif utctime.minute >= 30 and utctime.minute <= 44:
            difference = timedelta(hours = 2, minutes = utctime.minute)
            utctime -= difference
            difference = timedelta(minutes = 30)
            utctime += difference
        elif utctime.minute >= 45 and utctime.minute <= 59:
            difference = timedelta(hours = 2, minutes = utctime.minute)
            utctime -= difference
            difference = timedelta(minutes = 45)
            utctime += difference
        
        return utctime


    def _create_img_dir(self, title):
        """
        Protected abstract method implementation which is called during the base SatelliteCrawlers' pulldown_images
        method. This method is to generate the directory string path of where an image should be placed or already
        exists.

        @param title: str - A string containing the following standard format: 'TITLE - DATE - HH-MM UTC'
        which describes the image being queried.
        @return dir_path: str - A directory string containing the following standard format: 'METEOSAT-11/DATE/HH-MM UTC/TITLE'
        where the image downloaded should be placed, or already has been placed.
        """

        dir_path = ""
        
        today = re.split(self.TITLE_DELIMITER, title)[1]
        utctime = re.split(self.TITLE_DELIMITER, title)[-1].replace(':', '-')

        dir_path = self.METEOSAT_11_DIRECTORY + os.sep + str(today) + os.sep + utctime + os.sep + title
        
        return dir_path


    def __generate_title(self, type_path, utc, curr_range):
        """
        Using a UTC formatted time and a relative path containing the partial title, performs the necessary 
        formatting to generate the standardized title format.

        @param utc: str - A string formatted as: '2021-01-24 21:30 UTC'.
        @param path: str - A string containing the relative path which contains some partial title.
        @return title: str - A string containing the following standard format: 'TITLE - DATE - HH-MM UTC'
        """
        
        title = ''
        my_type = self.IMAGE_TITLES[type_path]

        # Extract the date (d), and create UTC time without the date.
        d = utc.split(" ")[0]
        utc = utc.split(" ")[1:]
        utc = ' '.join([str(t) for t in utc])

        # Take the last part of the partial path containing some title information
        title = my_type + os.sep + my_type + ' ' + curr_range.split('.')[0] + " - " + d + " - " + utc
        
        return title


    def create_satellite_directory(self):
        """
        Creates a high-level directory with the static METEOSAT_11_DIRECTORY string if it does not exist.
        """

        if not os.path.exists(self.METEOSAT_11_DIRECTORY):
            os.makedirs(self.METEOSAT_11_DIRECTORY)