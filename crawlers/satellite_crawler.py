import os
import sys
import time
import signal
import shutil
import logging
import zipfile
import requests
import multitasking
from stem import Signal
from datetime import date
from datetime import datetime
from contextlib import closing
import urllib.request as request
from stem.control import Controller
from stem.util.log import get_logger
from crawlers.crawler import Crawler

class SatelliteCrawler(Crawler):
    """
    Generic base satellite spider class which is to be extended for each unique web scrapping campaign.
    This method of splitting spiders into separate classes will help with keeping longevity of spider 
    runner classes and update issues easier that may occur during website HTML updates. This spider hierarchy
    requires using the Tor network and using the default settings (including ControlPort) to access the network.

    @author Vincent.Nigro
    @version 0.0.1
    @modified 2/21/22
    """
    
    # Supported satellite names
    DSCOVR_NAME = 'DSCOVR'
    EWS_G1_NAME = 'EWS-G1'
    GOES_15_NAME = 'GOES-15'
    GOES_16_NAME = 'GOES-16'
    INSAT_3D_NAME = 'INSAT-3D'
    INSAT_3DR_NAME = 'INSAT-3DR'
    GOES_WEST_NAME = 'GOES-WEST'
    ARKTIKA_M1_NAME = 'ARKTIKA-M1'
    HIMAWARI_8_NAME = 'HIMAWARI-8'
    ELEKTRO_L2_NAME = 'ELEKTRO-L2'
    ELEKTRO_L3_NAME = 'ELEKTRO-L3'
    FENGYUN_2G_NAME = 'FENGYUN-2G'
    FENGYUN_2H_NAME = 'FENGYUN-2H'
    FENGYUN_4A_NAME = 'FENGYUN-4A'
    METEOSAT_8_NAME = 'METEOSAT-8'
    METEOSAT_11_NAME = 'METEOSAT-11'
    GEO_KOMPSAT_2A_NAME = 'GEO-KOMPSAT-2A'
    
    # kill all tasks on ctrl-c
    signal.signal(signal.SIGINT, multitasking.killall)

    def __init__(self, url, satellite):
        """
        Abstract constructor which accepts a full base path to a URL to begin crawl and a satellite name.
        
        @param url: str - A string containing a full URL path to some website to begin web crawl.
        @param satellite: str - A string containing a representative name for the concrete satellite crawler.
        """

        self.__url = url
        self.__start = time.time()
        self.__satellite = satellite

        # Initialize logging for starting up satellite crawler
        self._initialize_logging()


    @multitasking.task
    def download_images(self, links, pw):
        """
        A generic function which accepts a dictionary of links where each entry is a key-value mapping of 
        a standardized title as the key, and a link containing the high resolution image that needs to be
        downloaded. The title is formatted as the following: 'TITLE - DATE - HH-MM UTC'. Each web crawler
        must ensure the title key is in the above format as the appropriate directories are made based off
        of that assumption. Each link to an image will be downloaded if not already done and will be stored
        in an appropriate file system hierarchy. If the crawler is for ELEKTRON-L2 spacecraft, the download 
        is done via the FTP protocol where all other spacecraft are performed with HTTP/HTTPS web crawling via
        the Tor client network.

        @param links: {} - A key-value mapping of a title key in a standard format and its appropriate image link
        @param pw: str - A string containing the Tor password for the given system configuration.
        """

        # For each link, extract and name img dir as title
        for title, link in links.items():
            starting_info = 'Thread ' + title + ' has started download...'
            print(starting_info)
            logging.info(starting_info)
            
            failed_download = False

            # Create file name derived from link path
            filename = link.split("/")[-1]

            #Create path SAT_DIRECTORY/DD MMM YYYY/HH-MM/title to contain filename
            dir_path = self._create_img_dir(title)

            # Only request image page if needs to be downloaded
            if not self._image_exists(title):
                # Check if path exists prior to attempting to create path
                if not os.path.exists(dir_path):
                    logging.info("Creating directory path " + dir_path + ".")
                    os.makedirs(dir_path)

                # Create full relative path including file name
                path = os.path.join(dir_path, filename)

                if (self.get_satellite_name() == self.ELEKTRO_L2_NAME) or \
                (self.get_satellite_name() == self.ARKTIKA_M1_NAME): # FTP Download
                    try:
                        with closing(request.urlopen(link)) as r:
                            with open(path, 'wb') as f:
                                shutil.copyfileobj(r, f)
                    except Exception as e:
                        logging.error(e)
                        print(e)
                        sys.exit(1)
                else: # HTTP/HTTPS download
                    # Create new tor session to extract page
                    page = self._extract_content(link, pw, True)
                    
                    # proceed processing if image page was extracted
                    if (page.status_code == self.OK_STATUS):
                        # Set decode_content to True, otherwise image file size will be 0.
                        page.raw.decode_content = True

                        # download file to path      
                        with open(path,'wb') as f:
                            logging.info("Downloading " + title + "...")
                            shutil.copyfileobj(page.raw, f)
                            f.close()
                
                        # if file is zipped, unzip and remove zip file
                        if (self.ZIP_EXTENSION in filename):
                            try:
                                with zipfile.ZipFile(path, 'r') as ref:
                                    logging.info("Downloaded file was zipped, extracting to " + dir_path + ".")
                                    ref.extractall(dir_path)
                                    ref.close()
                        
                                logging.info("Removing zipped file located at " + path + ".")
                                os.remove(path)
                            except Exception as e:
                                print(e)
                                logging.error(e)
                                failed_download = True
                    else:
                        failed_download_log = title + " failed to download."
                        logging.info(failed_download_log)
                        print(failed_download_log)
                
                if not failed_download:
                    downloaded_log = title + " has downloaded."
                    logging.info(downloaded_log)
                    print(downloaded_log)
            else:
                already_downloaded_log = "An image for " + title + " has already been downloaded."
                logging.info(already_downloaded_log)
                print(already_downloaded_log)


    def _extract_content(self, link, pw='', streaming=False):
        """
        A generic page extraction function utilizing the Tor session and recycling the current IP
        to another once the GET request has been fufilled and returned.

        @param link: str - A string containing a URL to some HTML page.
        @param pw: str - A string containing the Tor password for the given system configuration.
        @param streaming: bool - Defaults to false, set to True when dealing with a binary file like an image.
        @return page: Response - Returns a requests.Response object
        """

        page = None

        # Create new tor session to extract page
        s = self._get_tor_session()
        
        # Extract html archive page
        logging.info("Extracting page content at link: " + link)
        if streaming:
            page = s.get(link, stream=streaming)
        else:
            page = s.get(link)
        s.close()

        if pw != '':
            # Generate a new Tor IP
            self._renew_connection(pw)

        return page


    def _get_tor_session(self):
        """
        Creates a requests session using the standard SOCKS5 localhost ports used by Tor.

        @return session: Session - A requests.Session type containing static SOCK5 HTTP/HTTPS proxies configured 
        to default Tor output socket.
        """

        logging.info("Creating new tor session for satellite " + self.__satellite)
        
        # initialize a requests Session
        session = requests.Session()
        
        # setting the proxy of both http & https to the localhost:9050 
        # this requires a running Tor service in your machine and listening on port 9050 (by default)
        session.proxies = {"http": "socks5://localhost:9050", "https": "socks5://localhost:9050"}
        
        return session


    def _renew_connection(self, pw):
        """
        Contacts the Tor network configurations' ControlPort on port 9051 to authenticate itself and
        perform a recycle of a new Tor IP address.

        @param pw: str - A string containing the Tor password for the given system configuration.
        """

        with Controller.from_port(port=9051) as c:
            # Authenticates access to Tor ControlPort. 
            c.authenticate(password=pw)
            
            # send NEWNYM signal to establish a new clean connection through the Tor network
            c.signal(Signal.NEWNYM)
            
            generated_ip_log = 'Generated new tor IP...'
            logging.info(generated_ip_log)
            print(generated_ip_log)


    def _image_exists(self, title):
        """
        A protected member function for querying whether or not an image has already been downloaded based
        off of the current file system hierarchy.

        @param title: str - A string containing the following standard format: 'TITLE - DATE - HH-MM UTC'
        which describes the image being queried.
        """

        dir_path = self._create_img_dir(title)

        # If path exists and the directory is not empty, then the image exists
        if os.path.exists(dir_path) and os.listdir(dir_path) != []:
            return True
        return False


    def elapsed_time_procedure(self):
        """
        Generic public method which calculates the elapsed time of the specific satellite crawler and
        logs the information to both the log file and console. 
        """
        
        end = time.time()
        hours, rem = divmod(end - self.__start, 3600)
        minutes, seconds = divmod(rem, 60)
        elapsed_log = "The elapsed time was {:0>2} hours, {:0>2} minutes, and {:05.2f} seconds.".format(int(hours), int(minutes), seconds)
        
        logging.info(elapsed_log)
        print(elapsed_log)
        logging.debug("Pass has ended.")
        logging.debug("---------------------------------------------")


    def _initialize_logging(self):
        """
        Generic protected method which initializes logging for a generic concrete satellite crawler during instantiation.
        """
        
        logpath = "logs/"
        logfile = "SAT-" + self.__satellite + "-CRAWL-" + str(date.today()) + ".txt"

        # Turn off STEM logging
        logger = get_logger()
        logger.propagate = False

        if not os.path.exists(logpath):
            os.makedirs(logpath)
        
        # Initialize root logging
        logging.basicConfig(filename=logpath + logfile, level=logging.DEBUG, \
        format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')  
        logging.debug("Satellite " + self.__satellite + " crawl has initialized.")


    def _julian_to_date(self, jdate):
        """
        Converts a julian date string to a date object that can be converted to other formats.
         
        @param jdate: str - A string in the format of YYYYJJJ to be converted to a datetime object. Ex: 2022224
        """

        fmt = '%Y%j'
        date = datetime.strptime(jdate, fmt).date()

        return date


    def get_url(self):
        """
        Generic public accessor method which will return the name of the satellite configured for the given base url.
        """

        return self.__url


    def get_satellite_name(self):
        """
        Generic public accessor method which will return the name of the satellite configured for the given instance.
        """

        return self.__satellite


    def get_links(self, pw):
        """
        Abstract public method to be implemented by concrete satellite crawlers.
        """

        raise NotImplementedError("Subclass must implement abstract method.")


    def create_satellite_directory(self):
        """
        Abstract public method to be implemented by concrete satellite crawlers.
        """

        raise NotImplementedError("Subclass must implement abstract method.")


    def _create_img_dir(self, title):
        """
        Abstract protected method to be implemented by concrete satellite crawlers.
        """

        raise NotImplementedError("Subclass must implement abstract method.")