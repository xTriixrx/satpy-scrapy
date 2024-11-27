import sys
import shlex
import getopt
import logging
import hashlib
import multitasking
from xml.dom import minidom
from crawlers.dscovr import DSCOVR
from crawlers.ews_g2 import EWS_G2
from crawlers.goes_16 import GOES_16
from crawlers.goes_18 import GOES_18
from crawlers.insat_3d import INSAT_3D
from crawlers.insat_3dr import INSAT_3DR
from crawlers.gk_2a import GEO_KOMPSAT_2A
from crawlers.arktika_m1 import ARKTIKA_M1
from crawlers.arktika_m2 import ARKTIKA_M2
from crawlers.himawari_8 import HIMAWARI_8
from crawlers.elektro_l2 import ELEKTRO_L2
from crawlers.elektro_l3 import ELEKTRO_L3
from crawlers.elektro_l4 import ELEKTRO_L4
from crawlers.fengyun_4a import FENGYUN_4A
from crawlers.fengyun_4b import FENGYUN_4B
from crawlers.fengyun_2g import FENGYUN_2G
from crawlers.fengyun_2h import FENGYUN_2H
from crawlers.meteosat_9 import METEOSAT_9
from crawlers.meteosat_11 import METEOSAT_11

"""
Scrapes multiple different websites for the latest high resolution imagery for satellites GOES-16,
GOES-18, HIMAWARI-8, GEO-KOMPSAT-2A, FENGYUN-4A, FENGYUN-4B, FENGYUN-2G, FENGYUN-2H,
METEOSAT-9, METEOSAT-11, DSCOVR, ELEKTRO-L3, ELEKTRO-L2, ELEKTRO-L4, ARKTIKA-M1, INSAT-3D, and INSAT-3DR.

 @author Vincent Nigro
 @version 1.0.2
 @modified 11/27/24
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
    print("Version: 1.0.1")
    print("Last Modified: 8/12/22")
    print("")
    print("This program extracts the latest high resolution images from various sources using the Tor Network.")
    print("")
    print("To printout the available image filters for each satellite")
    print("\tsudo python3 satpy-scrapy.py --filters")
    print("")
    print("To extract all the latest HIMAWARI-8 images")
    print("\tsudo python3 satpy-scrapy.py -i")
    print("")
    print("To extract all the latest DSCOVR images")
    print("\tsudo python3 satpy-scrapy.py -d")
    print("")
    print("To extract all the latest ARTIKA-M1 images")
    print("\tsudo python3 satpy-scrapy.py -a1")
    print("")
    print("To extract all the latest GOES-16 images")
    print("\tsudo python3 satpy-scrapy.py -g16")
    print("")
    print("To extract all the latest GOES-18 images")
    print("\tsudo python3 satpy-scrapy.py -g18")
    print("")
    print("To extract the latest FENGYUN-4A image")
    print("\tsudo python3 satpy-scrapy.py -fy4a")
    print("")
    print("To extract the latest GK2A images")
    print("\tsudo python3 satpy-scrapy.py -gk2a")
    print("")
    print("To extract the latest METEOSAT-9 images")
    print("\tsudo python3 satpy-scrapy.py -m9")
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
    print("To extract the latest ELEKTRO-L3 image")
    print("\tsudo python3 satpy-scrapy.py -k4")
    print("")
    print("To extract the latest INSAT-3D images")
    print("\tsudo python3 satpy-scrapy.py -insat3d")
    print("")
    print("To extract the latest INSAT-3DR images")
    print("\tsudo python3 satpy-scrapy.py -insat3dr")
    print("")
    print("To extract 'Visible' FENGYUN-2H images")
    print("\tsudo python3 satpy-scrapy.py -fy2h --images=\"Visible\"")
    print("")
    print("To extract the latest ELEKTRO-L2 images within a UTC range")
    print("\tsudo python3 satpy-scrapy.py -k2 --utcrange=\"0000-2300\"")
    print("")
    print("To extract the latest ELEKTRO-L2 images within a UTC range for a day in the current month")
    print("\tsudo python3 satpy-scrapy.py -k2 --day=\"25\" --utcrange=\"0000-2300\"")
    print("")
    print("To extract the latest FENGYUN-4A images within a UTC range")
    print("\tsudo python3 satpy-scrapy.py -fy4a --utcrange=\"0000-2300\"")
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
    print("To extract the latest GeoColor GOES-18 images with 21696 resolution")
    print("\tsudo python3 satpy-scrapy.py -g18 --images=\"GeoColor\" --resolution=21696")
    print("")


def filter_logger():
    """
    A function called by handle_arguments which provides examples to stdout regarding possible image link filtering.
    """

    dscovr_filter_options = ['Natural Color', 'Enhanced Color']

    fy2g_g15_filter_options = ['Visible', 'Shortwave IR', 'Water Vapor', 'Longwave IR']

    fy2h_filter_options = ['False Color', 'Infared 1', 'Infared 2', 'Infared 3', 'Infared 4', 'Visible']

    goes_filter_options = \
    [
        'Band 1', 'Band 2', 'Band 3', 'Band 4', 'Band 5', 'Band 6', 'Band 7', 'Band 8', 'Band 9',
        'Band 10', 'Band 11', 'Band 12', 'Band 13', 'Band 14', 'Band 15', 'Band 16', 'AirMass RGB',
        'Derived Motion Winds', 'Day Cloud Phase RGB', 'Day Convection RGB', 'Dust', 'Fire Temperature', 'GeoColor',
        'Nighttime Microphysics', 'Split Window Differential', 'Sandwich RGB'
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
        'Band 1', 'Band 2', 'Band 3', 'Band 4', 'Band 5', 'Band 6', 'Band 7', 'Band 8', 'Band 9', 'Band 10', 'Band 11', 'GeoColor', 'ProxyVis',
        'Dust - DEBRA', 'Split Window Difference', 'Split Window Difference Dust', 'Split Window Difference Grayscale', 'Natural Color', 
        'RGB AirMass', 'Day Cloud Phase Distinction', 'Nighttime Microphysics', 'Dust', 'Natural Color-Fire', 'Ash'
    ]

    himawari_filter_options = \
    [
        'Band 1', 'Band 2', 'Band 3', 'Band 4', 'Band 5', 'Band 6', 'Band 7', 'Band 8', 'Band 9', 'Band 10', 'Band 11',
        'Band 12', 'Band 13', 'Band 14', 'Band 15', 'Band 16', 'GeoColor', 'Shortwave Albedo', 'Visible Albedo', 'Split Window Difference',
        'Natural Color', 'RGB AirMass', 'Day Cloud Phase Distinction', 'Dust', 'Fire Temperature', 'Natural Fire Color', 'Ash', 'Sulfur Dioxide',
        'Cloud-Top Height', 'Cloud Geometric Thickness', 'Cloud Layers', 'Cloud Optical Thickness', 'Cloud Effective Radius', 'Cloud Phase'
    ]

    insat_filter_options = \
    [
        'Infrared 10.8µm', 'Visible', 'Shortwave Infrared 1.625µm', 'Middlewave Infrared 3.9µm', 'Middlewave Infrared Temperature 3.9µm', 'Water Vapor',
        'Water Vapor Temperature', 'Infrared Temperature 10.8µm', 'Infrared 12.0µm', 'Infrared Temperature 12.0µm', 'Day Night Microphysics',
        'Outgoing Longwave Radiation', 'SST Regression', 'Land Surface Temperature', 'Upper Troposphere Humidity', 'Hydro Estimator Precipitation',
        'IMSRA (Improved)', 'Cloud Top Temperature', 'Cloud Top Pressure', 'Total Precipitable Water', 'Cloud Mask'
    ]

    arktika_m1_options = \
    [
        'Band 01', 'Band 02', 'Band 03', 'Band 04', 'Band 05', 'Band 06', 'Band 07', 'Band 08', 'Band 99', 'Band 10'
    ]

    print('Filter options for GOES-16, & GOES-18')
    print(*goes_filter_options, sep='\n')
    print('')
    print('Filter options for GEO-KOMPSAT-2A')
    print(*gk2a_filter_options, sep='\n')
    print('')
    print('Filter options for HIMAWARI-8')
    print(*himawari_filter_options, sep='\n')
    print('')
    print('Filter options for METEOSAT-9 & METEOSAT-11')
    print(*meteosat_options, sep='\n')
    print('')
    print('Filter options for DSCOVR')
    print(*dscovr_filter_options, sep='\n')
    print('')
    print('Filter options for FY2G')
    print(*fy2g_g15_filter_options, sep='\n')
    print('')
    print('Filter options for INSAT-3D and INSAT-3DR')
    print(*insat_filter_options, sep='\n')
    print('')
    print('Filter options for ARKTIKA-M1')
    print(*arktika_m1_options, sep='\n')
    print('')
    print('Filter options for FENGYUN-2H')
    print(*fy2h_filter_options, sep='\n')


def handle_arguments(argv):
    """
    Function which handles the command line arguments which had been presented during the start of the program.

    @param argv = [] - A list containing a set of arguments passed by the command line.
    @return satellite, img_types: SatelliteCrawler, [], notor: bool
    """

    day = ''
    notor = False
    img_types = []
    utc_range = ''
    resolution = ''
    arktika_pass = False
    elektro2_pass = False
    elektro3_pass = False
    elektro4_pass = False
    
    try:
        opts, args = getopt.getopt(argv, '-wehda:i:k:m:f:g:', 
            ['help', 'filters', 'day=', 'utcrange=', 'images=', 'resolution=', 'notor'])
        
        for opt, arg in opts:
            if opt == '-h' or opt == '--help':
                help_logger()
                sys.exit(0)
            elif opt == '--filters':
                filter_logger()
                sys.exit(0)
            elif opt == '--notor':
                notor = True
            elif opt == '-k':
                if arg == '2':
                    elektro2_pass = True
                if arg == '3':
                    elektro3_pass = True
                if arg == '4':
                    elektro4_pass = True
            elif opt == '-a' and (arg == '1' or arg == '2'):
                arktika_pass = True
                
        if elektro2_pass or elektro3_pass or elektro4_pass or arktika_pass:
            try:
                day = [arg for opt, arg in opts if opt == '--day'][0]
            except Exception as e:
                no_day = 'No --day parameter was given to Elektro-L2 image pull iteration.'
                logging.info(no_day)
            try:
                utc_range = [arg for opt, arg in opts if opt == '--utcrange'][0].split('-')
                if elektro2_pass:
                    utc_range = generate_utc_range_30_step(utc_range)
                elif elektro3_pass:
                    utc_range = generate_utc_range_15_step(utc_range)
                elif elektro4_pass:
                    utc_range = generate_utc_range_15_step(utc_range)
                elif arktika_pass:
                    utc_range = generate_utc_range_15_step(utc_range)
            except Exception as e:
                no_range = 'No --utcrange parameter was given to image pull iteration.'
                logging.info(no_range)

        img_types = [arg for opt, arg in opts if opt == '--images']
        
        if img_types != []:
            # Create list of each image type preserving quotes
            img_types = shlex.split(img_types[0])
        
        try:
            resolution = str([arg for opt, arg in opts if opt == '--resolution'][0])
        except Exception as e:
            no_resolution = "No resolution parameter was provided during image pull."
            resolution = '10848'
            logging.info(no_resolution)

        for opt, arg in opts:
            if opt == '-a':
                if arg == '1':
                    return ARKTIKA_M1(ARKTIKA_M1.ARKTIKA_M1_URL, ARKTIKA_M1.ARKTIKA_M1_NAME, day, utc_range), img_types, notor
                elif arg == '2':
                    return ARKTIKA_M2(ARKTIKA_M2.ARKTIKA_M2_URL, ARKTIKA_M2.ARKTIKA_M2_NAME, day, utc_range), img_types, notor
            elif opt == '-d':
                return DSCOVR(DSCOVR.DSCOVR_URL, DSCOVR.DSCOVR_NAME), img_types, notor
            elif opt == '-i':
                if arg == 'nsat3d':
                    return INSAT_3D(INSAT_3D.INSAT_3D_URL, INSAT_3D.INSAT_3D_NAME), img_types, notor
                elif arg == 'nsat3dr':
                    return INSAT_3DR(INSAT_3DR.INSAT_3DR_URL, INSAT_3DR.INSAT_3DR_NAME), img_types, notor
                elif arg == '8':
                    return HIMAWARI_8(HIMAWARI_8.HIMAWARI_8_URL, HIMAWARI_8.HIMAWARI_8_NAME), img_types, notor
            elif opt == '-k':
                if arg == '2':
                    return ELEKTRO_L2(ELEKTRO_L2.ELEKTRO_L2_URL, ELEKTRO_L2.ELEKTRO_L2_NAME, day,
                        utc_range), img_types, notor
                elif arg == '3':
                    return ELEKTRO_L3(ELEKTRO_L3.ELEKTRO_L3_URL, ELEKTRO_L3.ELEKTRO_L3_NAME, day,
                        utc_range), img_types, notor
                elif arg == '4':
                    return ELEKTRO_L4(ELEKTRO_L4.ELEKTRO_L4_URL, ELEKTRO_L4.ELEKTRO_L4_NAME, day,
                        utc_range), img_types, notor
            elif opt == '-f':
                if arg == 'y4a':
                    return FENGYUN_4A(FENGYUN_4A.FENGYUN_4A_URL, FENGYUN_4A.FENGYUN_4A_NAME), img_types, notor
                elif arg == 'y4b':
                    return FENGYUN_4B(FENGYUN_4B.FENGYUN_4B_URL, FENGYUN_4B.FENGYUN_4B_NAME), img_types, notor
                elif arg == 'y2g':
                    return FENGYUN_2G(FENGYUN_2G.FENGYUN_2G_URL, FENGYUN_2G.FENGYUN_2G_NAME), img_types, notor
                elif arg == 'y2h':
                    return FENGYUN_2H(FENGYUN_2H.FENGYUN_2H_URL, FENGYUN_2H.FENGYUN_2H_NAME), img_types, notor
            elif opt == '-g':
                if arg == 'k2a':
                    return GEO_KOMPSAT_2A(GEO_KOMPSAT_2A.GEO_KOMPSAT_2A_URL, GEO_KOMPSAT_2A.GEO_KOMPSAT_2A_NAME), img_types, notor
                elif arg == '2':
                    return EWS_G2(EWS_G2.EWS_G2_URL, EWS_G2.EWS_G2_NAME), img_types, notor
                elif arg == '16':
                    return GOES_16(GOES_16.GOES_16_URL, GOES_16.GOES_16_NAME, resolution, img_types), img_types, notor
                elif arg == '18':
                    return GOES_18(GOES_18.GOES_18_URL, GOES_18.GOES_18_NAME, resolution, img_types), img_types, notor
            elif opt == '-m':
                if arg == '9':
                    return METEOSAT_9(METEOSAT_9.METEOSAT_9_URL, METEOSAT_9.METEOSAT_9_NAME), img_types, notor
                elif arg == '11':
                    return METEOSAT_11(METEOSAT_11.METEOSAT_11_URL, METEOSAT_11.METEOSAT_11_NAME), img_types, notor
        
    except getopt.GetoptError as e:
        logging.exception(e)
        print(e)
        sys.exit(1)

    return GOES_16(GOES_16.GOES_16_URL, GOES_16.GOES_16_NAME, resolution, img_types), img_types, notor


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
    
    return tor_pw


def main(argv):
    """
    Main program which executes the anonymous extraction of GOES-16, HIMAWARI-8,
    FY-4A, GK2A, METEOSAT-9, METEOSAT-11, DSCOVR, ELEKTRO-L3, ELEKTRO-L2, ELEKTRO-L3, and ELEKTRO-L4 high resolution
    images. By default, the resolution for GOES vehicles is set to the 10848x10848 resolution, 
    FENGYUN-4A is typically just under 3k images, GK2A typically are under 1500x1500 and the HIMAWARI-8 
    images are either 11000x11000 or 5500x5500.
  
    To view configuration options, either run this program with the -h/--help flag or 
    view the help_logger() function above which describes examples and how to use this
    software.
    """
    tor_pw = ''

    satellite, img_titles, notor = handle_arguments(argv)

    if not notor:
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
                satellite.download_images(dictionary, tor_pw, notor)
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