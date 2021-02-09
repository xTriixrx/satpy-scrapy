# satpy-scrapy

<p align="center">

satpy-scrapy is a modular, multithreaded, protocol based high resolution satellite image scraper which utilizes the Tor network for HTTP/HTTPS web scraping capabilities as well as some FTP support. All satellites except the ELEKTRO-L2 satellite utilize HTTP/HTTPS Tor requests while the ELEKTRO-L2 satellite provides a direct FTP server connection to download images.

The --images= and --tor-password= arguments should not be used for the ELEKTRO-L2 satellite, the --utcrange= argument should only be used for the ELEKTRO-L2 satellite and the FENGYUN-4A satellite, and the --day= argument should only be used for the ELEKTRO-L2 satellite. Here are some sample commands for this program:

 * python3 satpy-scrapy.py -h
 * python3 satpy-scrapy.py --help
 * python3 satpy-scrapy.py --filters
 * python3 satpy-scrapy.py -k --utcrange="0000-2300"
 * python3 satpy-scrapy.py -e --tor-password="password"
 * python3 satpy-scrapy.py -w --tor-password="password"
 * python3 satpy-scrapy.py -i --tor-password="password"
 * python3 satpy-scrapy.py -m8 --tor-password="password"
 * python3 satpy-scrapy.py -f4a --tor-password="password"
 * python3 satpy-scrapy.py -gk2a --tor-password="password"
 * python3 satpy-scrapy.py -k --day="25" --utcrange="0000-2300"
 * python3 satpy-scrapy.py -e --images="GeoColor" --tor-password="password"
 * python3 satpy-scrapy.py -f4a --utcrange="0000-2300" --tor-password="password"
 * python3 satpy-scrapy.py -w --images="\"Derived Motion Winds\"" --tor-password="password"
 * python3 satpy-scrapy.py -gk2a --images="\"Natural Color\" \"True Color\"" --tor-password="password"
 * python3 satpy-scrapy.py -e --images=\"GeoColor \"Derived Motion Winds\"" --tor-password="password"
 * python3 satpy-scrapy.py -i --images="\"Natural Color\" \"GeoColor\"" --tor-password="password"

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

METEOSAT-8 (42.0E)

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
You can test your Tor client configuration by running the tor_check.py program with your tor password by editing line 37 of the program. After you run the program you should see 2 different IP addresses which are not your own IP address. With that taken care of you are now ready to use satpy-scrapy!
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

### Elektro-L2

<p align="center">The Electro-L satellite is Russia's second high-altitude weather observatory, coming after a troubled mission launched in 1994 that never achieved all of its goals The next-generation Electro-L program faced years of delays because of interruptions in funding. The Electro-L spacecraft will function for up to 10 years, collecting weather imagery several times per hour with visible and infrared cameras.</p>

<p align="center"> <img src="https://github.com/xTriixrx/satpy-scrapy/blob/master/imgs/210126_1600_original_RGB.jpg" /></p>

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

<p align="center"><img src="https://github.com/xTriixrx/satpy-scrapy/blob/master/imgs/2021-02-09 00-45 UTC.jpg" /></p>

## Command Line Arguments

Short Arguments
   * '-h': Triggers help logging function.
   * '-e': Instantiates GOES-EAST crawler to extract every possible image for this vehicle.
   * '-w': Instantiates GOES-WEST crawler to extract every possible image for this vehicle.
   * '-i': Instantiates HIMAWARI-8 crawler to extract every possible image for this vehicle.
   * '-k': Instantiates ELEKTRO-L2 crawler to extract every possible image for this vehicle.
   * '-m8': Instantiates METEOSAT-8 crawler to extract every possible image for this vehicle.
   * '-f4a': Instantiates FENGYUN-4A crawler to extract ever possible image for this vehicle.
   * '-gk2a': Instantiates GEO-KOMPSAT-2A crawler to extract every possible image for this vehicle.

Long Arguments
   * '--help': Triggers help logging function.
   * '--filters': Triggers image filter options function.
   * '--tor-password=': Sets the users tor password to extract images for non FTP server based vehicles.
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

 * METEOSAT-11 (0 degree) 3K images
 * DISCOVR 2048px x 2048px images
 * INSAT-3D 827px x 887px images
 * INSAT-3DR 827px x 887px images
 * Others potentially (FY-2, Elektro-L1 (archive))