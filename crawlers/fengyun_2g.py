import re
import os
import pytz
from datetime import datetime, timedelta
from crawlers.satellite_crawler import SatelliteCrawler

class FENGYUN_2G(SatelliteCrawler):
    """
    Concrete satellite spider class for FY-2G which extends the base class, SatelliteCrawler.
    This method of splitting spiders into separate classes will help with keeping longevity of spider 
    runner classes and update issues easier that may occur during website HTML updates. This spider hierarchy
    requires using the Tor network and using the default settings (including ControlPort) to access the network.

    @author Vincent.Nigro
    @version 0.0.1
    @modified 2/17/21
    """

    VISIBLE = '_01_'
    IMG_TYPE = 'fd.gif'
    WATER_VAPOR = '_03_'
    LONGWAVE_IR = '_04_'
    SHORTWAVE_IR = '_02_'
    VISIBLE_TITLE = 'Visible'
    FENGYUN_2G_FIELD = 'fy2g_'
    FY_2G_TIME_ZONE = 'Asia/Jakarta'
    WATER_VAPOR_TITLE = 'Water Vapor'
    LONGWAVE_IR_TITLE = 'Longwave IR'
    SHORTWAVE_IR_TITLE = 'Shortwave IR'
    FENGYUN_2G_DIRECTORY = 'FENGYUN-2G'
    FENGYUN_2G_URL = 'https://www.ssec.wisc.edu/data/geo/images/fy2g/animation_images/'

    def __init__(self, url, satellite):
        """
        A concrete constructor which accepts a full base path to a URL to begin crawl, and satellite name.
        
        @param url: str - A string containing a full URL path to some website to begin web crawl.
        @param satellite: str - A string containing a representative name for the FY-2G satellite crawler.
        """

        super().__init__(url, satellite)


    def get_links(self, pw):
        """
        Implemented abstract public method which performs FY-2G page link generation based on current time.

        @param pw: str - A string containing the Tor password for the given system configuration.
        @return links: {} - A key-value mapping of a title key in a standard format and its appropriate image link.
        """

        links = {}

        # Get start and stop utctimes
        utctime = self.__current_utctime()
        print(utctime)
        endtime = self.__calculate_endtime(utctime)
        print(endtime)

        # Generate dictionary containing julian date and utc hour/minute as key and georgian date str as value
        times = self.__calculate_timerange(utctime, endtime)

        # Get subset of links for each image type
        vis_links = self.__generate_links_set(times, self.VISIBLE)
        sir_links = self.__generate_links_set(times, self.SHORTWAVE_IR)
        wvp_links = self.__generate_links_set(times, self.WATER_VAPOR)
        lir_links = self.__generate_links_set(times, self.LONGWAVE_IR)

        # Merge individual dictionaries into one
        links = {**vis_links, **sir_links, **wvp_links, **lir_links}

        return links


    def __calculate_timerange(self, utctime, endtime):
        """
        Creates and returns a dictionary based off of a time range spanning about a day, where each iteration 
        stores a unique julian date with the utc hour and time as the key, and the georgian date as the value.

        @param utctime: datetime - A datetime object containing the current adjusted datetime.
        @param endtime: datetime - A datetime object containing the ending adjusted datetime.
        @return times: {} - A dictionary containing a unique string composed of julian date and utctime and date as value.
        """

        times = {}

        # While utctime is still greater, create date stamps list into times array
        while utctime >= endtime: 
            tt = utctime.timetuple()
            julian_datetime = int('%d%03d' % (tt.tm_year, tt.tm_yday))
            
            date = datetime.strptime(str(julian_datetime)[2:], '%y%j').date()
            hour = utctime.strftime('%H')
            minute = utctime.strftime('%M')

            # Add key value pair to times dictionary
            times[str(julian_datetime) + '_' + hour + minute] = str(date)

            # Get current minutes and remove minutes from iter utctime
            mins = utctime.minute
            difference = timedelta(minutes = utctime.minute)
            utctime -= difference
            
            # Decrement utctime to next mark
            if mins == 0:
                difference = timedelta(hours = 1)
                utctime -= difference
                difference = timedelta(minutes = 30)
                utctime += difference
            elif mins == 30:
                difference = timedelta(minutes = 1)
                utctime += difference
        
        return times


    def __calculate_endtime(self, utctime):
        """
        Subtracts 3 days, 1 hour, and all of the minutes off of the utctime passed, based on the
        minutes of the current adjusted utctime.

        @param utctime: datetime - A datetime object containing the current adjusted datetime.
        @return endtime: datetime - A datetime object containing the ending adjusted datetime.
        """

        # Create an endtime for which a 3 full days, a single hour and the remainder of minutes is subtracted
        endtime = utctime
        mins = endtime.minute
        difference = timedelta(days = 3, hours = 1, minutes = endtime.minute)
        endtime -= difference
        
        return endtime


    def __current_utctime(self):
        """
        Returns a current utctime time based on the timezone where the FY-2G spacecraft is located. This
        time is adjusted by an hour and all current minutes to ensure the latest image is posted on the web server.

        @return utctime: datetime - A datetime object containing the current adjusted datetime.
        """
        
        # Get UTC time of around where FY-2G vehicle is located
        time_zone = pytz.timezone(self.FY_2G_TIME_ZONE)
        country_time = datetime.now(time_zone)
        utctime = country_time.utcnow()
        
        # Subtract an hour and current minutes from current time to ensure we get an image
        difference = timedelta(hours = 1, minutes = utctime.minute)
        utctime -= difference
        difference = timedelta(minutes = 1)
        utctime += difference
        
        return utctime


    def __generate_links_set(self, times, img_type):
        """
        Generates a subset of the links dictionary based off of the times dictionary and the type of image.

        @param times: {} - A dictionary containing A unique string composed of julian date and utctime and date as value.
        @param img_type: str - A unique string containing identifying information to be utilized in link building.
        @return links: {} - A dictionary containing a unique string composed of julian date and utctime and date as value.
        """

        links = {}
        
        for julian_date, date in times.items():
            title = self.__generate_title(img_type, julian_date, date)
            link = self.__generate_link(img_type, julian_date)
            
            links[title] = link
        
        return links


    def __generate_link(self, img_type, j_date):
        """
        Generates and individual URL path based on the image type and the julian date string containing the utc
        hour and time joined together such as '2021048'.
        
        @param img_type: str - A unique string containing identifying information to be utilized in link building.
        @param j_date: str - A string containing the julian date and utc hour and time such as '2021048'.
        @return link: str - A generated link to retrieve a single image for the date, and img_type provided.
        """

        link = self.get_url() + self.FENGYUN_2G_FIELD + j_date + img_type + self.IMG_TYPE
        
        return link


    def __generate_title(self, img_type, j_date, date):
        """
        Using the date fields and img_type provided, performs the necessary formatting to generating the
        standardized title format.

        @param img_type: str - A unique string containing identifying information to be utilized in link building.
        @param j_date: str - A string containing the julian date and utc hour and time such as '2021048'.
        @param date: str - A georgian calendar datetime formatted as YYYY-MM-DD.
        @return title: str - A string containing the following standard format: 'TITLE - DATE - HH-MM UTC'
        """

        utc = j_date.split('_')[1]

        title = ''
        if img_type == self.VISIBLE:
            title = self.VISIBLE_TITLE
        elif img_type == self.SHORTWAVE_IR:
            title = self.SHORTWAVE_IR_TITLE
        elif img_type == self.WATER_VAPOR:
            title = self.WATER_VAPOR_TITLE
        elif img_type == self.LONGWAVE_IR:
            title = self.LONGWAVE_IR_TITLE
        
        title += ' - ' + date + ' - ' + utc[:-2] +  '-' + utc[2:] + ' ' + self.UTC_STRING
        
        return title


    def _create_img_dir(self, title):
        """
        Protected abstract method implementation which is called during the base SatelliteCrawlers' pulldown_images
        method. This method is to generate the directory string path of where an image should be placed or already
        exists.

        @param title: str - A string containing the following standard format: 'TITLE - DATE - HH-MM UTC'
        which describes the image being queried.
        @return dir_path: str - A directory string containing the following standard format: 'FENGYUN-2G/DATE/HH-MM UTC/TITLE'
        where the image downloaded should be placed, or already has been placed.
        """
        
        dir_path = ''
        
        today = re.split(self.TITLE_DELIMITER, title)[1]
        utctime = re.split(self.TITLE_DELIMITER, title)[-1].replace(':', '-')

        dir_path = self.FENGYUN_2G_DIRECTORY + os.sep + str(today) + os.sep + utctime + os.sep + title
        
        return dir_path


    def create_satellite_directory(self):
        """
        Creates a high-level directory with the static FENGYUN_2G_DIRECTORY string if it does not exist.
        """

        if not os.path.exists(self.FENGYUN_2G_DIRECTORY):
            os.makedirs(self.FENGYUN_2G_DIRECTORY)