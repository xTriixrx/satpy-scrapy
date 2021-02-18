# satpy-scrapy

<p align="center">

satpy-scrapy is a modular, multithreaded, protocol based high resolution satellite image scraper which utilizes the Tor network for HTTP/HTTPS web scraping capabilities as well as some FTP support. All satellites except the ELEKTRO-L2 satellite utilize HTTP/HTTPS Tor requests while the ELEKTRO-L2 satellite provides a direct FTP server connection to download images.

The --images= argument should not be used for the ELEKTRO-L2 satellite, the --utcrange= argument should only be used for the ELEKTRO-L2 satellite and the FENGYUN-4A satellite, and the --day= argument should only be used for the ELEKTRO-L2 satellite. Here are some sample commands for this program:

 * sudo python3 satpy-scrapy.py -h
 * sudo python3 satpy-scrapy.py -d
 * sudo python3 satpy-scrapy.py -e
 * sudo python3 satpy-scrapy.py -w
 * sudo python3 satpy-scrapy.py -i
 * sudo python3 satpy-scrapy.py -k2
 * sudo python3 satpy-scrapy.py -k3
 * sudo python3 satpy-scrapy.py -m8
 * sudo python3 satpy-scrapy.py -m11
 * sudo python3 satpy-scrapy.py -f4a
 * sudo python3 satpy-scrapy.py -gk2a
 * sudo python3 satpy-scrapy.py --help
 * sudo python3 satpy-scrapy.py --filters
 * sudo python3 satpy-scrapy.py -e --images="GeoColor"
 * sudo python3 satpy-scrapy.py -k2 --utcrange="0000-2300"
 * sudo python3 satpy-scrapy.py -f4a --utcrange="0000-2300"
 * sudo python3 satpy-scrapy.py -d --images="\"Enhanced Color\""
 * sudo python3 satpy-scrapy.py -k2 --day="25" --utcrange="0000-2300"
 * sudo python3 satpy-scrapy.py -k3 --images="\"Synthesized Color\""
 * sudo python3 satpy-scrapy.py -w --images="\"Derived Motion Winds\""
 * sudo python3 satpy-scrapy.py -i --images="\"Natural Color\" \"GeoColor\""
 * sudo python3 satpy-scrapy.py -e --images=\"GeoColor \"Derived Motion Winds\""
 * sudo python3 satpy-scrapy.py -gk2a --images="\"Natural Color\" \"True Color\""

The merge-img program is a utility program which will merge together patches of a full res image together. Some satellites being queried are written to extract the full resolution patches to be merged together at a later time, rather than downloading a single, low resolution image. Some images provide the full 11008px x 11008px resolution image while others are downscaled to some other lower resolution. Here are some sample commands for this program:

 * python3 merge-img.py --destination="\"HIMAWARI-8/2021-02-08/22-30 UTC/GeoColor\"" --dimension="16"
 * python3 merge-img.py --destination="\"HIMAWARI-8/2021-02-08/22-30 UTC/RGB AirMass\"" --dimension="8"

It is highly recommended to target a single image type at a time for a given scraping run as each image requires 256 (16x16) or 64 (8x8) web scraping runs for each image patch. As the number of images increase, the risk of failure exponentially increases along with the number of web scrape requests. It can also be said that the more images scraped in a single run the longer the run will take, so if this is to be automated the chance of missing images increases. Optimally, this would benefit from a mulithreaded, multisystem environment such as a Beowulf cluster. Below here is a list of each satellite that follows this pattern of individual image patches and will need to merge the image patches together, along with the available resolution:

HIMAWARI-8:

 * Band 1 (16x16) - 11008x11008 resolution.
 * Band 2 (16x16) - 11008x11008 resolution.
 * Band 3 (16x16) - 11008x11008 resolution.
 * Band 4 (16x16) - 11008x11008 resolution.
 * Band 5 (8x8) - 5504x5504 resolution.
 * Band 6 (8x8) - 5504x5504 resolution.
 * Band 7 (8x8) - 5504x5504 resolution.
 * Band 8 (8x8) - 5504x5504 resolution.
 * Band 9 (8x8) - 5504x5504 resolution.
 * Band 10 (8x8) - 5504x5504 resolution.
 * Band 11 (8x8) - 5504x5504 resolution.
 * Band 12 (8x8) - 5504x5504 resolution.
 * Band 13 (8x8) - 5504x5504 resolution.
 * Band 14 (8x8) - 5504x5504 resolution.
 * Band 15 (8x8) - 5504x5504 resolution.
 * Band 16  (8x8) - 5504x5504 resolution.
 * GeoColor (16x16) - 11008x11008 resolution.
 * Shortwave Albedo (8x8) - 5504x5504 resolution.
 * Visible Albedo (8x8) - 5504x5504 resolution.
 * Split Window Difference (8x8) - 5504x5504 resolution.
 * Natural Color (16x16) - 11008x11008 resolution.
 * RGB AirMass (8x8) - 5504x5504 resolution.
 * Day Cloud Phase Distinction (16x16) - 11008x11008 resolution.
 * Dust (8x8) - 5504x5504 resolution.
 * Fire Temperature (8x8) - 5504x5504 resolution.
 * Natural Fire Color (16x16) - 11008x11008 resolution.
 * Ash (8x8) - 5504x5504 resolution.
 * Sulfur Dioxide (8x8) - 5504x5504 resolution.
 * Cloud-Top Height (8x8) - 5504x5504 resolution.
 * Cloud Geometric Thickness (8x8) - 5504x5504 resolution.
 * Cloud Layers (8x8) - 5504x5504 resolution.
 * Cloud Optical Thickness (8x8) - 5504x5504 resolution.
 * Cloud Effective Radius (8x8) - 5504x5504 resolution.
 * Cloud Phase (8x8) - 5504x5504 resolution.

METEOSAT-8 (42.0E) && METEOSAT-11 (0.0)

 * Band 1 (8x8) - 3712x3712 resolution.
 * Band 2 (8x8) - 3712x3712 resolution.
 * Band 3 (8x8) - 3712x3712 resolution.
 * Band 4 (8x8) - 3712x3712 resolution.
 * Band 5 (8x8) - 3712x3712 resolution.
 * Band 6 (8x8) - 3712x3712 resolution.
 * Band 7 (8x8) - 3712x3712 resolution.
 * Band 8 (8x8) - 3712x3712 resolution.
 * Band 9 (8x8) - 3712x3712 resolution.
 * Band 10 (8x8) - 3712x3712 resolution.
 * Band 11 (8x8) - 3712x3712 resolution.
 * GeoColor (8x8) - 3712x3712 resolution.
 * Natural Color (8x8) - 3712x3712 resolution.
 * RGB AirMass (8x8) - 3712x3712 resolution.
 * Day Cloud Phase Distinction (8x8) - 3712x3712 resolution.
 * Nighttime Microphysics (8x8) - 3712x3712 resolution.
 * Dust (8x8) - 3712x3712 resolution.
 * Ash (8x8) - 3712x3712 resolution.

Below is a .gif file created by ELEKTRO-L2 satellite images scraped by this program from January 26th, 2021 - January 27th, 2021.
</p>

<p align="center"> <img src="https://github.com/xTriixrx/satpy-scrapy/blob/master/imgs/elektro-l2.gif" /> </p>

<p align="center">Below is a .gif file created by EWS-G1 satellite images scraped by this program from February 16th, 2021 - February 17th, 2021.</p>

<p align="center"> <img src="https://github.com/xTriixrx/satpy-scrapy/blob/master/imgs/ews-g1.gif" /> </p>

## Tor Client Configuration

<p align="center">
The Tor client can be installed on multiple operating systems and each installation may vary. For instance to install the Tor client on Mac OS, you can use Homebrew using the 'brew install tor' command. To install the Tor client I would suggest looking up the specific instructions for your operating system. Once installed, on Linux and Mac OS the torrc configuration file should be located
at /usr/local/etc/tor/torrc. Before editing this file you should have a password hashed by tor with the following command saved: tor --hashed-password "your-pw-here". Save the output as you will need
to store this in your torrc configuration file. When you open the torrc file you will need to uncomment the following lines:
</p>

 * ControlPort 9051
 * HashedControlPassword YOUR-HASH-GOES-HERE

<p align="center">
And add the following lines at the bottom of the file if you would like to use a specific country as your end point:
</p>

 * ExitNodes {us}
 * StrictNodes 1

<p align="center">
You can test your Tor client configuration by running the tor_check.py program with your tor password by editing line 37 of the program. After you run the program you should see 2 different IP addresses which are not your own IP address. Now we just need to set up the config file and secret file containing a hashed string. This hashed string should be the hash for your tor password that you have defined for the ControlPort. To generate a hash, use the hasher.py program to produce a hash. Once a hash is produced, copy this and while as the root user create a file that should be only known to you and stored somewhere other than the satpy-scrapy directory location and paste the hash into this file. Once this file is saved, chmod this file as root into a readonly mode (400) such that only the root user can access this special file. Lastly, create a config.xml file within the satpy-scrapy directory as root and populate the fields templated in the example config.xml file. Once the config file is finished being written to, also as root chmod this file to be readonly (400) as well. Enforcing root privileges increases security of storing passwords on the file system and decentralizing the password from a single config file. It is recommended to remove the hasher.py program when finished with setting up the environment. With that taken care of you are now ready to use satpy-scrapy!
</p>

## Supported Satellites

### GOES-EAST (NOAA/GOES-16)

<p align="center">GOES-16, formerly known as GOES-R before reaching geostationary orbit, is the first of the GOES-R series of Geostationary Operational Environmental Satellite (GOES) operated by NASA and the National Oceanic and Atmospheric Administration (NOAA).</p>

<p align="center"> <img src="https://github.com/xTriixrx/satpy-scrapy/blob/master/imgs/20210231620_GOES16-ABI-FD-GEOCOLOR-10848x10848.jpg" /></p>

<p align="center"> <img src="https://github.com/xTriixrx/satpy-scrapy/blob/master/imgs/20210260420_GOES16-ABI-FD-GEOCOLOR-10848x10848.jpg" /></p>

### GOES-WEST (NOAA/GOES-17)

<p align="center">GOES-17 (formerly GOES-S) is the second of the current generation of weather satellites operated by the National Oceanic and Atmospheric Administration (NOAA).</p>

<p align="center"> <img src="https://github.com/xTriixrx/satpy-scrapy/blob/master/imgs/20210260140_GOES17-ABI-FD-GEOCOLOR-10848x10848.jpg" /></p>

<p align="center"> <img src="https://github.com/xTriixrx/satpy-scrapy/blob/master/imgs/20210300530_GOES17-ABI-FD-NightMicrophysics-10848x10848.jpg" /></p>

### EWS-G1 (GOES-13)

<p align="center">EWS-G1 (Electro-optical Infrared Weather System Geostationary)[1] is a weather satellite of the U.S. Space Force, formerly GOES-13 (also known as GOES-N before becoming operational) and part of the National Oceanic and Atmospheric Administration's Geostationary Operational Environmental Satellite system.</p>

<p align="center"> <img src="https://github.com/xTriixrx/satpy-scrapy/blob/master/imgs/ews-g1_2021047_0845_01_fd.gif" /></p>

### Elektro-L2

<p align="center">The Electro-L satellite is Russia's second high-altitude weather observatory, coming after a troubled mission launched in 1994 that never achieved all of its goals The next-generation Electro-L program faced years of delays because of interruptions in funding. The Electro-L spacecraft will function for up to 10 years, collecting weather imagery several times per hour with visible and infrared cameras.</p>

<p align="center"> <img src="https://github.com/xTriixrx/satpy-scrapy/blob/master/imgs/210126_1600_original_RGB.jpg" /></p>

### Elektro-L3

<p align="center">The third satellite in the series Elektro-L No.3, was launched from Baikonur Cosmodrome on 24 December 2019 at 12:03 UTC by a Proton-M rocket</p>

<p align="center"> <img src="https://github.com/xTriixrx/satpy-scrapy/blob/master/imgs/2102110630_e3_295.jpg" /></p>

### HIMAWARI-8

<p align="center">Himawari 8 (ひまわり8号) is a Japanese weather satellite, the 8th of the Himawari geostationary weather satellites operated by the Japan Meteorological Agency. Himawari-8 will be succeeded by Himawari-9 which is currently in standby mode, until 2022.</p>

<p align="center"> <img src="https://github.com/xTriixrx/satpy-scrapy/blob/master/imgs/full_disk_ahi_natural_color_20210126023000.jpg" /></p>

### Fengyun 4A

<p align="center">Fengyun-4 (Wind and Cloud) series is China’s second-generation geostationary meteorological satellites after Fengyun-2 satellite series.</p>

<p align="center"> <img src="https://github.com/xTriixrx/satpy-scrapy/blob/master/imgs/00.jpg" /> </p>

### GEO-KOMPSAT-2A

<p align="center">GEO-KOMPSAT 2A is a South Korean geostationary meteorological satellite developed by KARI. It is one component of the two satellite GEO-KOMPSAT 2 program.
The GEO-KOMPSAT-2 program is to develop two geostationary orbit satellites, the meteorological GEO-KOMPSAT-2A (GK2A) and the ocean monitoring GEO-KOMPSAT-2B (GK2B) sharing the same satellite bus. The lifetime of both satellites will be no less than 10 years.</p>

<p align="center"> <img src="https://github.com/xTriixrx/satpy-scrapy/blob/master/imgs/gk2a_ami_le1b_rgb-true_fd010ge_202101300350.srv.png" /></p>

### METEOSAT-8

<p align="center">Meteosat 8 is a weather satellite, also known as MSG 1. The Meteosat series are operated by EUMETSAT under the Meteosat Transition Programme (MTP) and the Meteosat Second Generation (MSG) program. Meteosat-8 is expected to run out of fuel sometime in 2020[9] and it's availability lifetime will end in 2022.</p>

<p align="center"><img src="https://github.com/xTriixrx/satpy-scrapy/blob/master/imgs/2021-02-09 10-30 UTC_m8.jpg" /></p>

<p align="center"><img src="https://github.com/xTriixrx/satpy-scrapy/blob/master/imgs/2021-02-09 00-45 UTC.jpg" /></p>

### METEOSAT-11

<p align="center">Meteosat-11 is the prime operational geostationary satellite, positioned at 0º and providing full disc imagery every 15 minutes. It also provides Search and Rescue monitoring and Data Collection Platform Relay Service.</p>

<p align="center"><img src="https://github.com/xTriixrx/satpy-scrapy/blob/master/imgs/2021-02-09 10-30 UTC_m11.jpg" /></p>

<p align="center"><img src="https://github.com/xTriixrx/satpy-scrapy/blob/master/imgs/2021-02-09 01-00 UTC.jpg" /></p>

### DSCOVR

<p align="center">The Deep Space Climate Observatory, or DSCOVR, was launched in February of 2015, and maintains the nation's real-time solar wind monitoring capabilities, which are critical to the accuracy and lead time of NOAA's space weather alerts and forecasts. Without timely and accurate warnings, space weather events—like geomagnetic storms—have the potential to disrupt nearly every major public infrastructure system on Earth, including power grids, telecommunications, aviation and GPS.

The DSCOVR mission succeeded NASA's Advanced Composition Explorer's (ACE) role in supporting solar wind alerts and warnings from the L1 orbit, which is the neutral gravity point between the Earth and Sun, approximately one million miles from Earth. L1 is a good position from which to monitor the Sun, because the constant stream of particles from the Sun (the solar wind) reaches L1 up to an hour before reaching Earth.</p>

<p align="center"><img src="https://github.com/xTriixrx/satpy-scrapy/blob/master/imgs/epic_1b_20210209150054.png" /></p>

<p align="center"><img src="https://github.com/xTriixrx/satpy-scrapy/blob/master/imgs/epic_RGB_20210208061925.png" /></p>

## Command Line Arguments

Short Arguments
   * '-h': Triggers help logging function.
   * '-d': Instantiates DSCOVR crawler to extract ever possible image for this vehicle.
   * '-e': Instantiates GOES-EAST crawler to extract every possible image for this vehicle.
   * '-w': Instantiates GOES-WEST crawler to extract every possible image for this vehicle.
   * '-i': Instantiates HIMAWARI-8 crawler to extract every possible image for this vehicle.
   * '-g1': Instantiates EWS-G1 crawler to extract every possible image for this vehicle.
   * '-k2': Instantiates ELEKTRO-L2 crawler to extract every possible image for this vehicle.
   * '-k3': Instantiates ELEKTRO-L3 crawler to extract every possible image for this vehicle.
   * '-m8': Instantiates METEOSAT-8 crawler to extract every possible image for this vehicle.
   * '-m11': Instantiates METEOSAT-11 crawler to extract every possible image for this vehicle.
   * '-f4a': Instantiates FENGYUN-4A crawler to extract ever possible image for this vehicle.
   * '-gk2a': Instantiates GEO-KOMPSAT-2A crawler to extract every possible image for this vehicle.

Long Arguments
   * '--help': Triggers help logging function.
   * '--filters': Triggers image filter options function.
   * '--images=': Accepts a set of image filters to reduce number of images extracted on Tor requests.
   * '--utcrange=': Accepts a UTC range in the format of 'NNNN-NNNN' where N is a number and the range is between 0000 and 2330. The range should only be set in half hour increments to query a set of images in the ELEKTRO-L2 FTP server or for the FENGYUN-4A crawler.
   * '--day=': Accepts a day of the current month to query for the ELEKTRO-L2 FTP server. 

## Dependencies

 * BeautifulSoup 4
 * Requests v2.24
 * Stem v1.8
 * Pytz v2020.1
 * Multitasking v0.0.9

### Future Satellite Support

 * FY-2G 1125 x 1125px images
 * INSAT-3D 827px x 887px images
 * INSAT-3DR 827px x 887px images
 * FY-2H 2000px x 1200px images (China/India region)
 * Others potentially (FY-2, Elektro-L1 (archive 2013-2016))