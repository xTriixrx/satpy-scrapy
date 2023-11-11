# satpy-scrapy

<p align="center">

satpy-scrapy is a modular, multithreaded, protocol based high resolution satellite image scraper which utilizes the Tor network for HTTP/HTTPS web scraping capabilities as well as some FTP support. All satellites except the ELEKTRO-L2, ELEKTRO-L3, ELEKTRO-L4, ARKTIKA-M1, FY-4A, and FY-2H satellites utilize HTTP/HTTPS Tor requests. The ELEKTRO-L2, ELEKTRO-L3, ELEKTRO-L4, and ARKTIKA-M1 satellites provide a direct FTP server connection to download images while the FY-4A, FY-4B, and FY-2H satellites use a --notor flag to circumvent the Tor Network due to China's network blocking Tor requests. It is highly recommended to use a VPN while scraping images for FY-4A, FY-4B, and FY-2H, otherwise your personal IP will be exposed during the web scrape run and could be banned.

The --utcrange=/--day= arguments should only be used for the ELEKTRO-L2, ELEKTRO-L3, ELEKTRO-L4, and the ARKTIKA-M1 satellites. Here are some sample commands for this program:

 * sudo python3 satpy-scrapy.py -h
 * sudo python3 satpy-scrapy.py --help
 * sudo python3 satpy-scrapy.py --filters
 * sudo python3 satpy-scrapy.py -g16 --images="GeoColor"
 * sudo python3 satpy-scrapy.py -k2 --utcrange="0000-2300"
 * sudo python3 satpy-scrapy.py -a1 --utcrange="0000-2300"
 * sudo python3 satpy-scrapy.py -fy4a --images="Visible" --notor
 * sudo python3 satpy-scrapy.py -d --images="\\\"Enhanced Color\\\""
 * sudo python3 satpy-scrapy.py -a1 --day="25" --utcrange="0000-2300"
 * sudo python3 satpy-scrapy.py -k2 --day="25" --utcrange="0000-2300"
 * sudo python3 satpy-scrapy.py -gk2a --images="\\\"Natural Color\\\" \\\"True Color\\\""

The merge-img program is a utility program which will merge together patches of a full res image together. Some satellites being queried are written to extract the full resolution patches to be merged together at a later time, rather than downloading a single, low resolution image. Some images provide the full 11008px x 11008px resolution image while others are downscaled to some other lower resolution. Here are some sample commands for this program:

 * python3 merge-img.py --destination="\\\"HIMAWARI-8/2021-02-08/22-30 UTC/GeoColor\\\"" --dimension="16"
 * python3 merge-img.py --destination="\\\"HIMAWARI-8/2021-02-08/22-30 UTC/RGB AirMass\\\"" --dimension="8"

It is highly recommended to target a single image type at a time for a given scraping run as each image requires 256 (16x16) or 64 (8x8) web scraping runs for each image patch. Please be mindful of your scraping.

Below are some .gif's created by a few of the satellites that are supported by satpy-scrapy:
</p>

<p align="center"> <img src="https://github.com/xTriixrx/satpy-scrapy/blob/master/imgs/elektro-l2.gif" /> </p>

<p align="center">Created by EWS-G1 satellite images scraped by this program from February 16th, 2021 - February 17th, 2021.</p>

<p align="center"> <img src="https://github.com/xTriixrx/satpy-scrapy/blob/master/imgs/ews-g1.gif" /> </p>

<p align="center">Created by FY-4A satellite images scraped by this program from February 12th, 2022 - February 13th, 2022.</p>

<p align="center"> <img src="https://github.com/xTriixrx/satpy-scrapy/blob/master/imgs/FY4A_20220212160000_20220212161459_TO_20220213160000_20220213161459.gif" /> </p>

<p align="center">Created by ARKTIKA-M1 satellite images scraped by this program from February 12th, 2022 - February 13th, 2022. The composite color mapping was created by blending the first 3 bands (1-BLUE, 2-RED, 3-GREEN) into a false color composite. For more information on how to do this a quick tutorial with GIMP can be found here: <a href="https://remoteastrophotography.com/2020/03/using-gimp-to-combine-three-mono-images-into-one-rgb">Using GIMP to Combine Three Mono Images Into One RGB</a>
</p>

<p align="center"> <img src="https://github.com/xTriixrx/satpy-scrapy/blob/master/imgs/ARKTIKA-M1-20220211024502121945.gif" /> </p>

## Tor Client Configuration

<p align="center">
The Tor client can be installed on multiple operating systems and each installation may vary. For instance to install the Tor client on Mac OS, you can use Homebrew using the 'brew install tor' command. To install the Tor client I would suggest looking up the specific instructions for your operating system. Once installed, on Linux and Mac OS the torrc configuration file should be located
at /etc/tor/torrc. Before editing this file you should have a password hashed by tor with the following command saved: tor --hash-password "your-pw-here". Save the output as you will need
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
Perform the following commands to enable the tor service and restart the tor service after configuration. 
</p>

```Bash
sudo systemctl enable tor
sudo systemctl restart tor
```

<p align="center">
Perform the following to install all requirements for satpy-scrapy.
</p>

```Bash
python3 -m pip install -r requirements.txt
```

<p align="center">
You can test your Tor client configuration by running the tor_check.py program with your tor password by editing line 37 of the program. After you run the program you should see 2 different IP addresses which are not your own IP address. 

We just need to set up the config file and secret file containing a hashed string. This hashed string should be the hash for your tor password that you have defined for the ControlPort.

To generate a hash, use the hasher.py program to produce a hash. Once a hash is produced, copy this and while as the root user create a file that should be only known to you and stored somewhere other than the satpy-scrapy directory location and paste the hash into this file. Once this file is saved, chmod this file as root into a readonly mode (400) such that only the root user can access this special file.

Lastly, create a config.xml file within the satpy-scrapy directory as root and populate the fields templated in the example config.xml file. Once the config file is finished being written to, also as root chmod this file to be readonly (400) as well. With that taken care of you are now ready to use satpy-scrapy!
</p>

## Supported Satellites

<details><summary></summary>

### GOES-16

<p align="center">GOES-16, formerly known as GOES-R before reaching geostationary orbit, is the first of the GOES-R series of Geostationary Operational Environmental Satellite (GOES) operated by NASA and the National Oceanic and Atmospheric Administration (NOAA).</p>
<details>
<summary></summary>
<p align="center"> <img src="https://github.com/xTriixrx/satpy-scrapy/blob/master/imgs/20210231620_GOES16-ABI-FD-GEOCOLOR-10848x10848.jpg" /></p>

<p align="center"> <img src="https://github.com/xTriixrx/satpy-scrapy/blob/master/imgs/20210260420_GOES16-ABI-FD-GEOCOLOR-10848x10848.jpg" /></p>
</details>

### GOES-18

<p align="center">GOES-18 (formerly GOES-T) is the third of the "GOES-R Series", the current generation of weather satellites operated by the National Oceanic and Atmospheric Administration (NOAA).</p>
<details>
<summary></summary>
<p align="center"> <img src="https://github.com/xTriixrx/satpy-scrapy/blob/master/imgs/20222270200_GOES18-ABI-FD-GEOCOLOR-1808x1808.jpg" /></p>
</details>

### ARKTIKA-M1

<p align="center">Arktika-M (Russian Арктика-М) is a Russian multipurpose satellite constellation under construction. The main task of Arktika-M is weather observation in the northern part of Russian territory; in addition, the satellites are to be used there as data relays and for emergency communication. Other applications are the observation of space weather, the earth's magnetic field and the ionosphere. The first satellite in the constellation - Arktika-M1 - was launched on the 28th. February 2021 with a Soyuz 2.1b/Fregat rocket from Baikonur Cosmodrome. Another four satellites are to follow by 2025.</p>
<details>
<summary></summary>
<p align="center"> <img src="https://github.com/xTriixrx/satpy-scrapy/blob/master/imgs/V1_3720_20220217143000_RGB.jpg" /></p>
</details>

### ELEKTRO-L2

<p align="center">The Electro-L satellite is Russia's second high-altitude weather observatory, coming after a troubled mission launched in 1994 that never achieved all of its goals The next-generation Electro-L program faced years of delays because of interruptions in funding. The Electro-L spacecraft will function for up to 10 years, collecting weather imagery several times per hour with visible and infrared cameras.</p>
<details>
<summary></summary>
<p align="center"> <img src="https://github.com/xTriixrx/satpy-scrapy/blob/master/imgs/210126_1600_original_RGB.jpg" /></p>
</details>

### ELEKTRO-L3

<p align="center">The third satellite in the series Elektro-L No.3, was launched from Baikonur Cosmodrome on 24 December 2019 at 12:03 UTC by a Proton-M rocket.</p>
<details>
<summary></summary>
<p align="center"> <img src="https://github.com/xTriixrx/satpy-scrapy/blob/master/imgs/2102110630_e3_295.jpg" /></p>
</details>

### ELEKTRO-L4

<p align="center">The fourth satellite in the series Elektro-L No.4, was launched from Baikonur Cosmodrome on 5 February 2023 at 9:12 UTC by a Proton-M rocket.</p>
<details>
<summary></summary>
<p align="center"> <img src="https://github.com/xTriixrx/satpy-scrapy/blob/master/imgs/EL4-231110_0500_RGB.jpg" /></p>
</details>

### HIMAWARI-8

<p align="center">Himawari 8 (ひまわり8号) is a Japanese weather satellite, the 8th of the Himawari geostationary weather satellites operated by the Japan Meteorological Agency. Himawari-8 will be succeeded by Himawari-9 which is currently in standby mode, until 2022.</p>
<details>
<summary></summary>
<p align="center"> <img src="https://github.com/xTriixrx/satpy-scrapy/blob/master/imgs/full_disk_ahi_natural_color_20210126023000.jpg" /></p>
</details>

### FY-4A

<p align="center">FY-4 (Wind and Cloud) series is China’s second-generation geostationary meteorological satellites after FY-2 satellite series. FY-4A is the first installment of the FY-4 family and was launched on December 10th, 2016.</p>
<details>
<summary></summary>
<p align="center"> <img src="https://github.com/xTriixrx/satpy-scrapy/blob/master/imgs/FY4A-_AGRI--_N_DISK_1047E_L1C_MTCC_MULT_NOM_20220210050000_20220210051459_1000M_V0001.jpeg" /> </p>
</details>

### FY-4B

<p align="center">FY-4 (Wind and Cloud) series is China’s second-generation geostationary meteorological satellites after FY-2 satellite series. FY-4B is the second installment of the FY-4 family and was launched on June 2nd, 2021.</p>
<details>
<summary></summary>
<p align="center"> <img src="" /> </p>
</details>

### FY-2G

<p align="center">FY 2G is a meteorological satellites to provide warnings of weather fronts and tropical cyclones across Asia. FY 2G will take over for the FY 2E weather observatory at 105 degrees east longitude. China's fleet of FY 2 spacecraft have a similar mission to NOAA's GOES weather satellites in geostationary orbit.</p>
<details>
<summary></summary>
<p align="center"> <img src="https://github.com/xTriixrx/satpy-scrapy/blob/master/imgs/fy2g_2021048_0530_01_fd.gif" /> </p>
</details>

### FY-2H

<p align="center">FY-2H is the eighth and final of the FY-2 series of spin-stabilized weather satellites for geostationary orbit, development of which began in the 1980s under CASC. The satellite is equipped with a Stretched Visible and Infrared Spin Scan Radiometer (S-VISSR) for multi-purpose weather satellite imagery, a Space Environment Monitor (SEM), a Solar X-ray Monitor (SXM) and Data Collection Service (DCS).</p>
<details>
<summary></summary>
<p align="center"> <img src="https://github.com/xTriixrx/satpy-scrapy/blob/master/imgs/FY2H_GLB_VIS_GRA_1KM_20220221_0700.jpg" /> </p>
</details>

### GK-2A

<p align="center">GK-2A is a South Korean geostationary meteorological satellite developed by KARI. It is one component of the two satellite GK 2 program.
The GK-2 program is to develop two geostationary orbit satellites, the meteorological GK-2A (GEO-KOMPSAT-2A) and the ocean monitoring GK-2B (GEO-KOMPSAT-2B) sharing the same satellite bus. The lifetime of both satellites will be no less than 10 years.</p>
<details>
<summary></summary>
<p align="center"> <img src="https://github.com/xTriixrx/satpy-scrapy/blob/master/imgs/gk2a_ami_le1b_rgb-true_fd010ge_202101300350.srv.png" /></p>
</details>

### METEOSAT-9 (IODC)

<p align="center">Meteosat 9 is a weather satellite, also known as MSG-2. The Meteosat series are operated by EUMETSAT under the Meteosat Transition Programme (MTP) and the Meteosat Second Generation (MSG) program. Meteosat-9 took over as prime IODC spacecraft on June 1st, 2022; replacing Meteosat 8.</p>
<details>
<summary></summary>
<p align="center"><img src="https://github.com/xTriixrx/satpy-scrapy/blob/master/imgs/METEOSAT-9-2022-08-16%2023-00%20UTC.jpg" /></p>
</details>

### METEOSAT-11 (PRIME)

<p align="center">Meteosat-11 is the prime operational geostationary satellite, positioned at 0º and providing full disc imagery every 15 minutes. It also provides Search and Rescue monitoring and Data Collection Platform Relay Service.</p>
<details>
<summary></summary>
<p align="center"><img src="https://github.com/xTriixrx/satpy-scrapy/blob/master/imgs/2021-02-09 10-30 UTC_m11.jpg" /></p>

<p align="center"><img src="https://github.com/xTriixrx/satpy-scrapy/blob/master/imgs/2021-02-09 01-00 UTC.jpg" /></p>
</details>

### DSCOVR

<p align="center">The Deep Space Climate Observatory, or DSCOVR, was launched in February of 2015, and maintains the nation's real-time solar wind monitoring capabilities, which are critical to the accuracy and lead time of NOAA's space weather alerts and forecasts. Without timely and accurate warnings, space weather events—like geomagnetic storms—have the potential to disrupt nearly every major public infrastructure system on Earth, including power grids, telecommunications, aviation and GPS.

The DSCOVR mission succeeded NASA's Advanced Composition Explorer's (ACE) role in supporting solar wind alerts and warnings from the L1 orbit, which is the neutral gravity point between the Earth and Sun, approximately one million miles from Earth. L1 is a good position from which to monitor the Sun, because the constant stream of particles from the Sun (the solar wind) reaches L1 up to an hour before reaching Earth.</p>
<details>
<summary></summary>
<p align="center"><img src="https://github.com/xTriixrx/satpy-scrapy/blob/master/imgs/epic_1b_20210209150054.png" /></p>

<p align="center"><img src="https://github.com/xTriixrx/satpy-scrapy/blob/master/imgs/epic_RGB_20210208061925.png" /></p>
</details>

### INSAT-3D

<p align="center">INSAT-3D is a meteorological, data relay and satellite aided search and rescue satellite developed by the Indian Space Research Organisation and was launched successfully on 26 July 2013 using an Ariane 5 ECA launch vehicle from French Guiana. The satellite has many new technology elements like star sensor, micro stepping Solar Array Drive Assembly (SADA) to reduce the spacecraft disturbances and Bus Management Unit (BMU) for control and telecom and telemetry function. It also incorporates new features of bi-annual rotation and Image and Mirror motion compensations for improved performance of the meteorological payloads.</p>
<details>
<summary></summary>
<p align="center"> <img src="https://github.com/xTriixrx/satpy-scrapy/blob/master/imgs/Image3d%3Fimagename%3D3DIMG*_L1B_STD_VIS.jpg" /></p>
</details>

### INSAT-3DR

<p align="center">INSAT-3DR is an Indian weather satellite built by the Indian Space Research Organization and operated by the Indian National Satellite System. It will provide meteorological services to India using a 6-channel imager and a 19-channel sounder, as well as search and rescue information and message relay for terrestrial data collection platforms. The satellite was launched on 8 September 2016, and is a follow-up to INSAT-3D.</p>
<details>
<summary></summary>
<p align="center"> <img src="https://github.com/xTriixrx/satpy-scrapy/blob/master/imgs/Image3d%3Fimagename3r%3D3RIMG*_L1B_STD_VIS.jpg" /></p>
</details>

</details>
<br/>

## Argument Table
<details><summary></summary>

|Satellite|Short-Arg|Long-Args|Supported Image Names|Supported Resolutions|
|---|---|---|---|---|
|**DSCOVR**|-d|--images|'Natural Color'<br/>'Enhanced Color'|2048x2048|
|**GOES-16**<br/>**GOES-18**|-g16<br/>-g18|--images<br/>--resolution|'Band 1' (22k)<br/>'Band 2' (22k)<br/>'Band 3' (22k)<br/>'Band 4'<br/>'Band 5' (22k)<br/>'Band 6'<br/>'Band 7'<br/>'Band 8'<br/>'Band 9'<br/>'Band 10'<br/>'Band 11'<br/>'Band 12'<br/>'Band 13'<br/>'Band 14'<br/>'Band 15'<br/>'Band 16'<br/>'AirMass RGB' (22k)<br/>'Derived Motion Winds'<br/>'Day Cloud Phase RGB' (22k)<br/>'Day Convection RGB' (22k)<br/>'Dust' (22k)<br/>'Fire Temperature' (22k)<br/>'GeoColor' (22k)<br/>'Nighttime Microphysics' (22k)<br/>'Split Window Differential'<br/>'Sandwich RGB' (22k)|339x339<br/>678x678<br/>1808x1808<br/>5424x5424<br/>10848x10848<br/>21696x21696 (partial)|
|**HIMAWARI-8**|--i8|--images|'Band 1' (11k)<br/>'Band 2' (11k)<br/>'Band 3' (11k)<br/>'Band 4' (11k)<br/>'Band 5'<br/>'Band 6'<br/>'Band 7'<br/>'Band 8'<br/>'Band 9'<br/>'Band 10'<br/>'Band 11'<br/>'Band 12'<br/>'Band 13'<br/>'Band 14'<br/>'Band 15'<br/>'Band 16'<br/>'GeoColor' (11k)<br/>'Shortwave Albedo'<br/>'Visible Albedo'<br/>'Split Window Difference'<br/>'Natural Color' (11k)<br/>'RGB AirMass'<br/>'Day Cloud Phase Distinction' (11k)<br/>'Dust'<br/>'Fire Temperature'<br/>'Natural Fire Color' (11k)<br/>'Ash'<br/>'Sulfur Dioxide'<br/>'Cloud-Top Height'<br/>'Cloud Geometric Thickness'<br/>'Cloud Layers'<br/>'Cloud Optical Thickness'<br/>'Cloud Effective Radius'<br/>'Cloud Phase'|5504x5504<br/>11008x11008|
|**ELEKTRO-L2**<br/>**ELEKTRO-L3**|-k2<br/>-k3|--images<br/>--day<br/>--utcrange|'Band 1'<br/>'Band 2'<br/>'Band 3'<br/>'Band 4'<br/>'Band 5'<br/>'Band 6'<br/>'Band 7'<br/>'Band 8'<br/>'Band 9'<br/>'Band 10'<br/>'Rgb'<br/>'Rgb Vis'<br/>'Rgb Vis Ir'<br/>'Original Rgb'<br/>'Original Rgb Vis'<br/>'Original Rgb Vis Ir'<br/>|1080x1080<br/>11136x11136|
|**ELEKTRO-L4**|-k4|--images<br/>--day<br/>--utcrange|'Rgb'<br/>'Rgb Vis Ir'<br/>'Original Rgb'<br/>'Original Rgb Vis Ir'|1080x1080<br/>11136x11136|
|**FY-2G**|-fy2g|--images|Visible'<br/>'Water Vapor'<br/>'Longwave IR'<br/>'Shortwave IR'|1125x1125|
|**FY-2H**|-fy2h|--images<br/>--notor (mandatory)|'False Color'<br/>'Infared 1'<br/>'Infared 2'<br/>'Infared 3'<br/>'Infared 4'<br/>'Visible'|2288x2288<br/>9152x9152 (Visible)|
|**FY-4A**|-fy4a|--images<br/>--notor (mandatory)|'Visible' (11k)<br/>'Band 1' (11k)<br/>'Band 2' (11k)<br/>'Band 3' (11k)<br/>'Band 4'<br/>'Band 5'<br/>'Band 6'<br/>'Band 7'<br/>'Band 8'<br/>'Band 9'<br/>'Band 9 Enhanced'<br/>'Band 10'<br/>'Band 10 Enhanced'<br/>'Band 11'<br/>'Band 11 Enhanced'<br/>'Band 12'<br/>'Band 12 Enhanced'<br/>'Band 13'<br/>'Band 13 Enhanced'<br/>'Band 14'<br/>'Band 14 Enhanced'<br/>|2748x2748<br/>5496x5496<br/>10992x10992<br/>21984x21984|
|**FY-4B**|-fy4b|--images<br/>--notor (mandatory)|'True Color'<br/>'Natural Color'<br/>'Sandwich'|2248x2978<br/>10992x11912<br/>21984x23824|
|**METEOSAT-9**<br/>**METEOSAT-11**|-m9<br/>-m11|--images|'Band 1'<br/>'Band 2'<br/>'Band 3'<br/>'Band 4'<br/>'Band 5'<br/>'Band 6'<br/>'Band 7'<br/>'Band 8'<br/>'Band 9'<br/>'Band 10'<br/>'Band 11'<br/>'GeoColor'<br/>'ProxyVis'<br/>'Dust - DEBRA'<br/>'Split Window Difference'<br/>'Split Window Difference Dust'<br/>'Split Window Difference Grayscale'<br/>'Natural Color'<br/>'RGB AirMass'<br/>'Day Cloud Phase Distinction'<br/>'Nighttime Microphysics'<br/>'Dust'<br/>'Natural Color-Fire'<br/>'Ash'<br/>|3712x3712|
|**ARKTIKA-M1**|-a1|--images<br/>--day<br/>--utcrange|'Rgb Vis'<br/>'Rgb Vis Ir'<br/>'Original Rgb Vis'<br/>'Original Rgb Vis Ir'<br/>|1080x1080<br/>11136x11136|
|**GK-2A**|-gk2a|--images|'VIS 0.47µm'<br/>'VIS 0.51µm'<br/>'VIS 0.64µm' (22k)<br/>'VIS 0.86µm'<br/>'NIR 1.37µm'<br/>'NIR 1.6µm'<br/>'SWIR 3.8µm'<br/>'WV 6.3µm'<br/>'WV 6.9µm'<br/>'WV 7.3µm'<br/>'IR 8.7µm'<br/>'IR 9.6µm'<br/>'IR 10.5µm'<br/>'IR 11.2µm'<br/>'IR 12.3µm'<br/>'IR 13.3µm'<br/>'True Color'<br/>'Natural Color'<br/>'AirMass RGB'<br/>'Dust RGB'<br/>'Daynight RGB'<br/>'Fog RGB'<br/>'Storm RGB'<br/>'Snowfog RGB'<br/>'Cloud RGB'<br/>'Ash RGB'<br/>'Enhanced IR WV 6.3µm'<br/>'Enhanced IR WV 6.9µm'<br/>'Enhanced IR WV 7.3µm'<br/>'Enhanced IR 10.5µm'|5500x5637<br/>11000x11275 (partial)<br/>22000x22550(partial)|
|**INSAT-3D**<br/>**INSAT-3DR**|-insat3d|--images|'Infrared 10.8µm'<br/>'Visible'<br/>'Shortwave Infrared 1.625µm'<br/>'Middlewave Infrared 3.9µm'<br/>'Middlewave Infrared Temperature 3.9µm'<br/>'Water Vapor'<br/>'Water Vapor Temperature'<br/>'Infrared Temperature 10.8µm'<br/>'Infrared 12.0µm'<br/>'Infrared Temperature 12.0µm'<br/>'Day Night Microphysics'<br/>'Outgoing Longwave Radiation'<br/>'SST Regression'<br/>'Land Surface Temperature'<br/>'Upper Troposphere Humidity'<br/>'Hydro Estimator Precipitation'<br/>'IMSRA (Improved)'<br/>'Cloud Top Temperature'<br/>'Cloud Top Pressure'<br/>'Total Precipitable Water'<br/>'Cloud Mask'<br/>|1260x1410|
</details>
<br/>

### Additional Command Line Argument Info

Short Arguments
   * '-h': Triggers help logging function.

Long Arguments
   * '--help': Triggers help logging function.
   * '--filters': Triggers image filter options function.
   * '--images=': Accepts a set of image filters to reduce number of images extracted on Tor requests.
   * '--resolution=': Accepts some resolution such as '10848 or 678', currently only used by GOES-16 and GOES-18 scrapers.
   * '--notor': A way to circumvent the Tor network for certain vehicles. The only vehicles supported are FENGYUN-2H, FENGYUN-4A, and FENGYUN-4B. Using this feature implies that you have a VPN setup.
   * '--utcrange=': Accepts a UTC range in the format of 'NNNN-NNNN' where N is a number and the range is between 0000 and 2330. The range should only be set in half hour increments to query a set of images in the ELEKTRO-L2 FTP server. Also is supported by the ELEKTRO-L3, ELEKTRO-L4, & ARKTIKA-M1 crawler in half hour increments.
   * '--day=': Accepts a day in the format of 'NN' where N is a number and the range is between 01-31. The day is used to query the provided day of the current month for the ELEKTRO-L2, ELEKTRO-L3, ELEKTRO-L4, or ARKTIKA-M1 FTP server.

### Future Satellite Support

 * Others potentially (FY-2, Elektro-L1 (FTP archive 2013-2016), Historical Archive at https://www.ncdc.noaa.gov/gibbs/)
 * Future satellites (HIMAWARI-9, ARKTIKA-M2, FY-4C, GK-2B)


## Retired Satellites

<details><summary></summary>

### EWS-G1 (GOES-13)

<p align="center">EWS-G1 (Electro-optical Infrared Weather System Geostationary) is a weather satellite of the U.S. Space Force, formerly GOES-13 (also known as GOES-N before becoming operational) and part of the National Oceanic and Atmospheric Administration's Geostationary Operational Environmental Satellite system. EWS-G1 was placed into a graveyard orbit around October 31st 2023.</p>
<details>
<summary></summary>
<p align="center"> <img src="https://github.com/xTriixrx/satpy-scrapy/blob/master/imgs/ews-g1_2021047_0845_01_fd.gif" /></p>
</details>

### GOES-17

<p align="center">GOES-17 (formerly GOES-S) is the second of the current generation of weather satellites operated by the National Oceanic and Atmospheric Administration (NOAA). Due to a cooling problem with the satellite's main imager, GOES-17 entered early retirement and was placed in on-orbit storage on January 4th 2023.</p>
<details>
<summary></summary>
<p align="center"> <img src="https://github.com/xTriixrx/satpy-scrapy/blob/master/imgs/20210260140_GOES17-ABI-FD-GEOCOLOR-10848x10848.jpg" /></p>

<p align="center"> <img src="https://github.com/xTriixrx/satpy-scrapy/blob/master/imgs/20210300530_GOES17-ABI-FD-NightMicrophysics-10848x10848.jpg" /></p>
</details>

### GOES-15

<p align="center">GOES-15, previously known as GOES-P, is an American weather satellite, which forms part of the Geostationary Operational Environmental Satellite (GOES) system operated by the U.S. National Oceanic and Atmospheric Administration. The spacecraft was constructed by Boeing, and is the last of three GOES satellites to be based on the BSS-601 bus. It was launched in 2010, while the other BSS-601 GOES satellites -- GOES-13 and GOES-14—were launched in May 2006 and June 2009 respectively. It was the sixteenth GOES satellite to be launched. On March 2, 2020, GOES-15 was deactivated and moved to a storage orbit, with plans to re-activate it in August 2020 to back up GOES-17 operations due to a known flaw causing many sensors to become unreliable at night during certain times of the year. As of August 10th 2022, the GOES-15 IMAGER subsystem has been turned off and has been placed back into On-Orbit Storage. GOES-18 will now operate in tandum with GOES-17.</p>
<details>
<summary></summary>
<p align="center"> <img src="https://github.com/xTriixrx/satpy-scrapy/blob/master/imgs/goes-15_2021048_2100_01_fd.gif" /></p>
</details>

### METEOSAT-8

<p align="center">Meteosat 8 is a weather satellite, also known as MSG-1. The Meteosat series are operated by EUMETSAT under the Meteosat Transition Programme (MTP) and the Meteosat Second Generation (MSG) program. Meteosat-8 is expected to run out of fuel sometime in 2020 and it's availability lifetime will end in 2022. As of June 2022, METEOSAT-8 has been decommissioned and placed into a "graveyard orbit".</p>
<details>
<summary></summary>
<p align="center"><img src="https://github.com/xTriixrx/satpy-scrapy/blob/master/imgs/2021-02-09 10-30 UTC_m8.jpg" /></p>

<p align="center"><img src="https://github.com/xTriixrx/satpy-scrapy/blob/master/imgs/2021-02-09 00-45 UTC.jpg" /></p>
</details>
</details>
<br/>
