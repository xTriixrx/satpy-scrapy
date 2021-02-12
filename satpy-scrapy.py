import sys
import shlex
import getopt
import logging
import hashlib
import multitasking
from xml.dom import minidom
from crawlers.dscovr import DSCOVR
from crawlers.goes_16 import GOES_EAST
from crawlers.goes_17 import GOES_WEST
from crawlers.gk_2a import GEO_KOMPSAT_2A
from crawlers.himawari_8 import HIMAWARI_8
from crawlers.elektro_l2 import ELEKTRO_L2
from crawlers.elektro_l3 import ELEKTRO_L3
from crawlers.fengyun_4a import FENGYUN_4A
from crawlers.meteosat_8 import METEOSAT_8
from crawlers.meteosat_11 import METEOSAT_11

"""
Scrapes multiple different websites for the latest high resolution imagery for satellites GOES-EAST (GOES-16),
GOES-WEST (GOES-17), HIMAWARI-8, GEO-KOMPSAT-2A, FENGYUN-4A, METEOSAT-8, METEOSAT-11, DSCOVR, and ELEKTRO-L2.

 @author Vincent Nigro
 @version 0.0.1
 @modified 2/11/21
"""

ASCII = 'ascii'
READ_ONLY = 'rb'
TOR_ELEMENT = 'tor'
PW_ATTRIBUTE = 'pw'
SECRET_ELEMENT = 'secret'
CONFIG_FILE_LOC = 'config.xml'
LOCATION_ATTRIBUTE = 'location'

def generate_utc_range_30_step(utcrange):
    """
    A function which generates a list of UTC times in steps of 30 minutes, which starts at the first argument
    of the UTC range from the command line, and ends at the second argument of the UTC range from the same command line
    argument.

    @param utcrange: str - A string containing a start and stop UTC time in a range with a '-' as the delimiter.
    @return utc_range: [] An list containing an enumerated set of utc times separated by a half hour.
    """

    utc_range = []
    start = utcrange[0]
    stop = utcrange[-1]
    
    current = start
    
    while current != stop:
        utc_range.append(current)
        if current[-2:] == '00':
            current = current[:2]
            current += '30'
        else:
            hour = "{:02d}".format((int(current[:2]) + 1))
            current = '00'
            current = hour + current

    utc_range.append(current)

    return utc_range


def generate_utc_range_15_step(utcrange):
    """
    A function which generates a list of UTC times in steps of 15 minutes, which starts at the first argument
    of the UTC range from the command line, and ends at the second argument of the UTC range from the same command line
    argument.

    @param utcrange: str - A string containing a start and stop UTC time in a range with a '-' as the delimiter.
    @return utc_range: [] An list containing an enumerated set of utc times separated by a half hour.
    """

    utc_range = []
    start = utcrange[0]
    stop = utcrange[-1]
    
    current = start
    count = 0
    while current != stop:
        utc_range.append(current)
        if current[-2:] == '00':
            current = current[:2]
            current += '15'
        elif current[-2:] == '15':
            current = current[:2]
            current += '30'
        elif current[-2:] == '30':
            current = current[:2]
            current += '45'
        else:
            hour = "{:02d}".format((int(current[:2]) + 1))
            current = '00'
            current = hour + current

    utc_range.append(current)

    return utc_range


def help_logger():
    """
    A function called by handle_arguments which provides examples to stdout regarding possible commands.
    """

    print("Satellite Hi-Res IMG Scraper By Vincent Nigro")
    print("Version: 1.0.0")
    print("Last Modified: 2/11/21")
    print("")
    print("This program extracts the latest high resolution images from various sources using the Tor Network.")
    print("")
    print("To printout the available image filters for each satellite")
    print("\tsudo python3 satpy-scrapy.py --filters")
    print("")
    print("To extract all the latest GOES-EAST images")
    print("\tsudo python3 satpy-scrapy.py -e")
    print("")
    print("To extract all the latest GOES-WEST images")
    print("\tsudo python3 satpy-scrapy.py -w")
    print("")
    print("To extract all the latest HIMAWARI-8 images")
    print("\tsudo python3 satpy-scrapy.py -i")
    print("")
    print("To extract all the latest DSCOVR images")
    print("\tsudo python3 satpy-scrapy.py -d")
    print("")
    print("To extract the latest FENGYUN-4A image")
    print("\tsudo python3 satpy-scrapy.py -f4a")
    print("")
    print("To extract the latest GK2A images")
    print("\tsudo python3 satpy-scrapy.py -gk2a")
    print("")
    print("To extract the latest METEOSAT-8 images")
    print("\tsudo python3 satpy-scrapy.py -m8")
    print("")
    print("To extract the latest METEOSAT-11 images")
    print("\tsudo python3 satpy-scrapy.py -m11")
    print("")
    print("To extract the latest ELEKTRO-L2 image")
    print("\tsudo python3 satpy-scrapy.py -k2")
    print("")
    print("To extract the latest ELEKTRO-L3 image")
    print("\tsudo python3 satpy-scrapy.py -k3")
    print("")
    print("To extract the latest ELEKTRO-L2 images within a UTC range")
    print("\tsudo python3 satpy-scrapy.py -k2 --utcrange=\"0000-2300\"")
    print("")
    print("To extract the latest ELEKTRO-L2 images within a UTC range for a day in the current month")
    print("\tsudo python3 satpy-scrapy.py -k2 --day=\"25\" --utcrange=\"0000-2300\"")
    print("")
    print("To extract the latest FENGYUN-4A images within a UTC range")
    print("\tsudo python3 satpy-scrapy.py -f4a --utcrange=\"0000-2300\"")
    print("")
    print("To extract 'GeoColor' GOES-EAST image(s)")
    print("\tsudo python3 satpy-scrapy.py -e --images=\"GeoColor\"")
    print("")
    print("To extract 'Synthesized Color' ELEKTRO-L3 image(s)")
    print("\tsudo python3 satpy-scrapy.py -k3 --images=\"Synthesized Color\"")
    print("")
    print("To extract 'Derived Motion Winds' GOES-WEST image(s)")
    print("\tsudo python3 satpy-scrapy.py -w --images=\"\\\"Derived Motion Winds\\\"\"")
    print("")
    print("To extract 'Enhanced Color' DSCOVR image(s)")
    print("\tsudo python3 satpy-scrapy.py -d --images=\"\\\"Natural Color\\\"\"")
    print("")
    print("To extract 'GeoColor' and 'Derived Motion Winds' GOES-EAST images")
    print("\tsudo python3 satpy-scrapy.py -e --images=\"GeoColor \\\"Derived Motion Winds\\\"\"")
    print("")
    print("To extract 'Natural Color' and 'True Color' GK2A images")
    print("\tsudo python3 satpy-scrapy.py -gk2a --images=\"\\\"Natural Color\\\" \\\"True Color\\\"\"")
    print("")
    print("To extract 'Natural Color' and 'True Color' HIMAWARI-8 images")
    print("\tsudo python3 satpy-scrapy.py -i --images=\"\\\"Natural Color\\\" \\\"GeoColor\\\"\"")
    print("")


def filter_logger():
    """
    A function called by handle_arguments which provides examples to stdout regarding possible image link filtering.
    """

    dscovr_filter_options = ['Natural Color', 'Enhanced Color']

    goes_filter_options = \
    [
        "GeoColor (Captures GLM type too)", "GLM FED+GeoColor", "AirMass RGB", "Sandwich RGB", "Derived Motion Winds",
        "Day Cloud Phase RGB", "Nighttime Microphysics", "Band 1", "Band 2", "Band 3", "Band 4",
        "Band 5", "Band 6", "Band 7", "Band 8", "Band 9", "Band 10", "Band 11", "Band 12", "Band 13",
        "Band 14", "Band 15", "Band 16"
    ]

    gk2a_filter_options = \
    [
        'VIS 0.47µm', 'VIS 0.51µm', 'VIS 0.64µm', 'VIS 0.86µm', 'NIR 1.37µm', 'NIR 1.6µm', 'SWIR 3.8µm', 'WV 6.3µm',
        'WV 6.9µm', 'WV 7.3µm', 'IR 8.7µm', 'IR 9.6µm', 'IR 10.5µm', 'IR 11.2µm', 'IR 12.3µm', 'IR 13.3µm', 'True Color',
        'Natural Color', 'AirMass RGB', 'Dust RGB', 'Daynight RGB', 'Fog RGB', 'Storm RGB', 'Snowfog RGB', 'Cloud RGB', 
        'Ash RGB', 'Enhanced IR WV 6.3µm', 'Enhanced IR WV 6.9µm', 'Enhanced IR WV 7.3µm', 'Enhanced IR 10.5µm'
    ]
    
    meteosat_options = \
    [
        'Band 1', 'Band 2', 'Band 3', 'Band 4', 'Band 5', 'Band 6', 'Band 7', 'Band 8', 'Band 9', 'Band 10', 'Band 11', 'GeoColor',
        'Natural Color', 'RGB AirMass', 'Day Cloud Phase Distinction', 'Nighttime Microphysics', 'Dust', 'Ash'
    ]

    himawari_filter_options = \
    [
        'Band 1', 'Band 2', 'Band 3', 'Band 4', 'Band 5', 'Band 6', 'Band 7', 'Band 8', 'Band 9', 'Band 10', 'Band 11',
        'Band 12', 'Band 13', 'Band 14', 'Band 15', 'Band 16', 'GeoColor', 'Shortwave Albedo', 'Visible Albedo', 'Split Window Difference',
        'Natural Color', 'RGB AirMass', 'Day Cloud Phase Distinction', 'Dust', 'Fire Temperature', 'Natural Fire Color', 'Ash', 'Sulfur Dioxide',
        'Cloud-Top Height', 'Cloud Geometric Thickness', 'Cloud Layers', 'Cloud Optical Thickness', 'Cloud Effective Radius', 'Cloud Phase'
    ]

    print('Filter options for GOES-EAST & GOES-WEST')
    print(*goes_filter_options, sep='\n')
    print('')
    print('Filter options for GEO-KOMPSAT-2A')
    print(*gk2a_filter_options, sep='\n')
    print('')
    print('Filter options for HIMAWARI-8')
    print(*himawari_filter_options, sep='\n')
    print('')
    print('Filter options for METEOSAT-8 & METEOSAT-11')
    print(*meteosat_options, sep='\n')
    print('')
    print('Filter options for DSCOVR')
    print(*dscovr_filter_options, sep='\n')
    print('')


def handle_arguments(argv):
    """
    Function which handles the command line arguments which had been presented during the start of the program.

    @param argv = [] - A list containing a set of arguments passed by the command line.
    @return satellite, img_types: SatelliteCrawler, []
    """

    img_types = []
    utc_range = ''
    elektro_day = ''
    elektro2_pass = False
    fengyun_4a_pass = False
    
    try:
        opts, args = getopt.getopt(argv, '-wehidk:m:f:g:', 
            ['help', 'filters', 'day=', 'utcrange=', 'images='])
        
        for opt, arg in opts:
            if opt == '-h' or opt == '--help':
                help_logger()
                sys.exit(0)
            elif opt == '--filters':
                filter_logger()
                sys.exit(0)
            elif opt == '-k':
                if arg == '2':
                    elektro2_pass = True
            elif opt == '-f':
                if arg == '4a':
                    fengyun_4a_pass = True
                
        if not elektro2_pass:
            if fengyun_4a_pass:
                try:
                    utc_range = [arg for opt, arg in opts if opt == '--utcrange'][0].split('-')
                    utc_range = generate_utc_range_15_step(utc_range)
                except Exception as e:
                    no_range = 'No --utcrange parameter was given to Fengyun-4A image pull iteration.'
                    logging.info(no_range)
        else:
            try:
                elektro_day = [arg for opt, arg in opts if opt == '--day'][0]
            except Exception as e:
                no_day = 'No --day parameter was given to Elektro-L2 image pull iteration.'
                logging.info(no_day)
            try:
                utc_range = [arg for opt, arg in opts if opt == '--utcrange'][0].split('-')
                utc_range = generate_utc_range_30_step(utc_range)
            except Exception as e:
                no_range = 'No --utcrange parameter was given to Elektro-L2 image pull iteration.'
                logging.info(no_range)

        img_types = [arg for opt, arg in opts if opt == '--images']

        if img_types != []:
            # Create list of each image type preserving quotes
            img_types = shlex.split(img_types[0])

        for opt, arg in opts:
            if opt == '-d':
                return DSCOVR(DSCOVR.DSCOVR_URL, DSCOVR.DSCOVR_NAME), img_types
            elif opt == '-w':
                return GOES_WEST(GOES_WEST.GOES_WEST_URL, GOES_WEST.GOES_WEST_NAME, 10848), img_types
            elif opt == '-e':
                return GOES_EAST(GOES_EAST.GOES_EAST_URL, GOES_EAST.GOES_EAST_NAME, 10848), img_types
            elif opt == '-i':
                return HIMAWARI_8(HIMAWARI_8.HIMAWARI_8_URL, HIMAWARI_8.HIMAWARI_8_NAME), img_types
            elif opt == '-k':
                if arg == '2':
                    return ELEKTRO_L2(ELEKTRO_L2.ELEKTRO_L2_URL, ELEKTRO_L2.ELEKTRO_L2_NAME, elektro_day, 
                        utc_range), img_types
                elif arg == '3':
                    return ELEKTRO_L3(ELEKTRO_L3.ELEKTRO_L3_URL, ELEKTRO_L3.ELEKTRO_L3_NAME), img_types
            elif opt == '-f':
                if arg == '4a':
                    return FENGYUN_4A(FENGYUN_4A.FENGYUN_4A_URL, FENGYUN_4A.FENGYUN_4A_NAME, utc_range), img_types
            elif opt == '-g':
                if arg == 'k2a':
                    return GEO_KOMPSAT_2A(GEO_KOMPSAT_2A.GEO_KOMPSAT_2A_URL, GEO_KOMPSAT_2A.GEO_KOMPSAT_2A_NAME), img_types
            elif opt == '-m':
                if arg == '8':
                    return METEOSAT_8(METEOSAT_8.METEOSAT_8_URL, METEOSAT_8.METEOSAT_8_NAME), img_types
                elif arg == '11':
                    return METEOSAT_11(METEOSAT_11.METEOSAT_11_URL, METEOSAT_11.METEOSAT_11_NAME), img_types
        
    except getopt.GetoptError as e:
        logging.exception(e)
        print(e)
        sys.exit(1)

    return GOES_EAST(GOES_EAST.GOES_EAST_URL, GOES_EAST.GOES_EAST_NAME, 10848), img_types


def read_tor_secret():
    """
    This function will attempt to read a root-only accessible configuration file which contains an element named 'tor'
    with an attribute containing 'pw' which holds the value of a password. This password is read in and is checked against
    a hashed value stored in some secret file. This secret file is also root-only accessible meaning the entire satpy-scrapy
    program requires root to start such a program in order to access the configuration and secret files. This is a safer method
    than presenting the password at the command line where traffic sniffers can easily detect such a file.

    @return tor_pw: str - A plaintext string representing the password configured for the Tor clients' ControlPort. 
    """

    tor_pw = ''
    
    try:
        # Read & parse read only root configuration file
        dom = minidom.parse(CONFIG_FILE_LOC)
        tor_element = dom.getElementsByTagName(TOR_ELEMENT)
        sec_element = dom.getElementsByTagName(SECRET_ELEMENT)

        # Extract pw from secured configuration file and convert to binary
        pw = tor_element[0].attributes[PW_ATTRIBUTE].value
        pw = pw.encode(ASCII).rstrip()
        
        s_file = sec_element[0].attributes[LOCATION_ATTRIBUTE].value

        # Get hashed store in secret hold file location
        hw = ''
        with open(s_file, READ_ONLY) as f:
            hw = f.read()
            hw = hw.decode(ASCII).rstrip()
            f.close()
        
        hashed = hashlib.sha512(pw).hexdigest().rstrip()

        if hashed == hw:
            tor_pw = pw.decode(ASCII)
        else:
            err = 'Provided password in configuration file does not match secret hash.'
            logging.error(err)
            print(err)
            sys.exit(1)

    except Exception as e:
        logging.error(e)
        print(e)
        sys.exit(1)
    finally:
        return tor_pw


def main(argv):
    """
    Main program which executes the anonymous extraction of GOES-16, GOES-17, HIMAWARI-8,
    FY-4A, GK2A, METEOSAT-8, METEOSAT-11, DSCOVR, and ELEKTRO-L2 high resolution images. By default, 
    the resolution for GOES vehicles is set to the 10848x10848 resolution, FENGYUN-4A is typically 
    just under 3k images, GK2A typically are under 1500x1500 and the HIMAWARI-8 images are either 
    11000x11000 or 5500x5500.
  
    To view configuration options, either run this program with the -h/--help flag or 
    view the help_logger() function above which describes examples and how to use this
    software.
    """
    
    satellite, img_titles = handle_arguments(argv)

    tor_pw = read_tor_secret()

    if tor_pw == '':
        err = 'No password was read in from the configuration file, exiting now.'
        logging.error(err)
        print(err)
        sys.exit(1)
    
    try:
        satellite.create_satellite_directory()
        
        links = satellite.get_links(tor_pw)
        
        # If --images params were given, remove all inappropriate links that were not queried
        if img_titles != []:
            links = {title:link for (title,link) in links.items() if any(x in title for x in img_titles)}
        
        if links != {}:
            dict_list = []
            
            # Separate each key/value pair into its own dictionary
            for key, value in links.items():
                link = {}
                link[key] = value
                dict_list.append(link)
            
            # Recycle IP once before extracting image set
            if tor_pw != '':
                satellite._renew_connection(tor_pw)
                tor_pw = ''
            
            # download_images() implicitly spawns threads using @multitasking.task decorator
            for dictionary in dict_list:
                # Performs either Tor HTTP/HTTPs web scrape or FTP protocol to extract image from FTP server
                satellite.download_images(dictionary, tor_pw)
        else:
            err = "No image links were provided to be pulled down."
            logging.info(err)
            print(err)
        
        # Wait for all downloads to finish 
        multitasking.wait_for_tasks()
        
        # Perform time elapsed calculation.
        satellite.elapsed_time_procedure()
    except Exception as e:
        print(e)
    
if __name__ == "__main__":
    """
    Forces only execution by shell and passes sys.argv without program name.
    """

    main(sys.argv[1:])