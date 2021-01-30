class Crawler:
    """
    A bare generic base crawler class which is to be extended for each unique web scrapping campaign.
    This spider hierarchy contains the necessary constant static variables which can be accessed by each
    derived crawlers' 'self' reference.

    @author Vincent.Nigro
    @version 0.0.1
    @modified 1/29/21
    """

    # Standard crawler fields
    OK_STATUS = 200
    UTC_STRING = 'UTC'
    SOUP_PARSER = 'lxml'
    ZIP_EXTENSION = '.zip'
    TITLE_DELIMITER = ' - '

    # HTML Elements/Tags
    A_ELEMENT = 'a'
    TR_ELEMENT = 'tr'
    TD_ELEMENT = 'td'
    DIV_ELEMENT = 'div'
    IMG_ELEMENT = 'img'

    # HTML Element Attributes
    SRC_ATTRIBUTE = 'src'
    HREF_ATTRIBUTE = 'href'
    TITLE_ATTRIBUTE = 'title'
    CLASS_ATTRIBUTE = 'class'
    
    # div class value for GOES satellite imagery extraction
    GOES_TARGET_CLASS_VALUE = 'summaryContainer'

    def __init__(self):
        """
        An empty initialization function as there is nothing to be done.
        """