# satpy-scrapy

<p align="center">

satpy-scraper is a modular, protocol based high resolution satellite image scraper which utilizes the Tor network for HTTP/HTTPS web scraping capabilities as well as some FTP support. All satellites except the ELEKTRO-L2 satellite utilize HTTP/HTTPS Tor requests while the ELEKTRO-L2 satellite provides a direct FTP server connection to download images.

The --images= and --tor-password= arguments should not be used for the ELEKTRO-L2 satellite and the --day= and --utcrange= arguments should only be used for the ELEKTRO-L2 satellite. Here are some sample commands for this program:

 * python3 satpy-scrapy.py -e --tor-password="password"
 * python3 satpy-scrapy.py -w --tor-password="password"
 * python3 satpy-scrapy.py -m --tor-password="password"
 * python3 satpy-scrapy.py -k --utcrange="0000-2300"
 * python3 satpy-scrapy.py -k --day="25" --utcrange="0000-2300"
 * python3 satpy-scrapy.py -e --images="GeoColor" --tor-password="password"
 * python3 satpy-scrapy.py -w --images="\"Derived Motion Winds\"" --tor-password="password"
 * python3 satpy-scrapy.py -e --images=\"GeoColor \"Derived Motion Winds\"" --tor-password="password"
 * python3 satpy-scrapy.py -m --images="\"Natural Color\" \"GeoColor\"" --tor-password="password"

Below is a .gif file created by ELEKTRO-L2 satellite images scraped by this program from January 26th - January 27th.

</p>

<p align="center"> <img src="https://github.com/xTriixrx/satpy-scrapy/blob/master/imgs/elektro-l2.gif" /> </p>

## Tor Client Configuration

<p align="center">
The Tor client can be installed on multiple operating systems and each installation may vary. For instance to install the Tor client on Mac OS, you can use Homebrew using the 'brew install tor' command. To install the Tor client I would suggest looking up the specific instructions for your operating system. Once installed, on Linux and Mac OS the torrc configuration file should be located
at /usr/local/etc/tor/torrc. Before editing this file you should have a password hashed by tor with the following command saved: tor --hashed-password "your-pw-here". Save the output as you will need
to store this in your torrc configuration file. When you open the torrc file you will need to uncomment the following lines:
 * ControlPort 9051
 * HashedControlPassword YOUR-HASH-GOES-HERE

And add the following lines at the bottom of the file if you would like to use a specific country as your end point:
 * ExitNodes {us}
 * StrictNodes 1

You can test your Tor client configuration by running the tor_check.py program with your tor password by editing line 37 of the program. After you run the program you should see 2 different IP addresses which are not your own IP address. With that taken care of you are now ready to use satpy-scrapy!
</p>

## Supported Satellites

### GOES-EAST (NOAA/GOES-16)

<p align="center">GOES-16, formerly known as GOES-R before reaching geostationary orbit, is the first of the GOES-R series of Geostationary Operational Environmental Satellite (GOES) operated by NASA and the National Oceanic and Atmospheric Administration (NOAA).</p>

<p align="center"> <img src="https://github.com/xTriixrx/satpy-scrapy/blob/master/imgs/20210231620_GOES16-ABI-FD-GEOCOLOR-10848x10848.jpg" /> </p>

<p align="center"> <img src="https://github.com/xTriixrx/satpy-scrapy/blob/master/imgs/20210260420_GOES16-ABI-FD-GEOCOLOR-10848x10848.jpg" /> </p>

### GOES-WEST (NOAA/GOES-17)

<p align="center">GOES-17 (formerly GOES-S) is the second of the current generation of weather satellites operated by the National Oceanic and Atmospheric Administration (NOAA).</p>

<p align="center"> <img src="https://github.com/xTriixrx/satpy-scrapy/blob/master/imgs/20210260140_GOES17-ABI-FD-GEOCOLOR-10848x10848.jpg" /> </p>

### Elektro-L2

<p align="center">The Electro-L satellite is Russia's second high-altitude weather observatory, coming after a troubled mission launched in 1994 that never achieved all of its goals The next-generation Electro-L program faced years of delays because of interruptions in funding. The Electro-L spacecraft will function for up to 10 years, collecting weather imagery several times per hour with visible and infrared cameras.</p>

<p align="center"> <img src="https://github.com/xTriixrx/satpy-scrapy/blob/master/imgs/210126_1600_original_RGB.jpg" /> </p>

### HIMAWARI-8

<p align="center">Himawari 8 (ひまわり8号) is a Japanese weather satellite, the 8th of the Himawari geostationary weather satellites operated by the Japan Meteorological Agency. Himawari-8 will be succeeded by Himawari-9 which is currently in standby mode, until 2022.</p>

<p align="center"> <img src="https://github.com/xTriixrx/satpy-scrapy/blob/master/imgs/full_disk_ahi_natural_color_20210126023000.jpg" /> </p>

## Command Line Arguments

Short Arguments
   * '-h': Triggers help logging function.
   * '-e': Instantiates GOES-EAST crawler to extract every possible image for this vehicle.
   * '-w': Instantiates GOES-WEST crawler to extract every possible image for this vehicle.
   * '-m': Instantiates HIMAWARI-8 crawler to extract every possible image for this vehicle.
   * '-k': Instantiates ELEKTRO-L2 crawler to extract every possible image for this vehicle.

Long Arguments
   * '--help': Triggers help logging function.
   * '--filters': Triggers image filter options function.
   * '--tor-password=': Sets the users tor password to extract images for non FTP server based vehicles.
   * '--images=': Accepts a set of image filters to reduce number of images extracted on Tor requests.
   * '--utcrange=': Accepts a UTC range in the format of 'NNNN-NNNN' where N is a number and the range is between 0000 and 2330. The range should only be set in half hour increments to query a set of images in the ELEKTRO-L2 FTP server.
   * '--day=': Accepts a day of the current month to query for the ELEKTRO-L2 FTP server. 

## Dependencies

<p align="center">
 * BeautifulSoup 4
 * Requests v2.24
 * Stem v1.8
 * Pytz v2020.1
</p>

### Future Satellite Support

 * METEOSAT-8 (41.5 degree) 3K images
 * METEOSAT-10 (0 degree) 3K images
 * DISCOVR 2048px x 2048px images
 * GEO-KOMPSAT-2A 600px x 600px images
 * INSAT-3D 827px x 887px images
 * INSAT-3DR 827px x 887px images
 * Others potentially (FY-2/FY-4, Elektro-L1 (archive))