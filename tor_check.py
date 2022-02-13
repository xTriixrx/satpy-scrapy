import sys
import requests
from stem import Signal
from stem.control import Controller

def get_tor_session():
  """
  Creates a requests session using the standard SOCKS5 localhost ports used by Tor.

  @return session: Session - A requests.Session type containing static SOCK5 HTTP/HTTPS proxies configured 
  to default Tor output socket.
  """

  # initialize a requests Session
  session = requests.Session()
  # setting the proxy of both http & https to the localhost:9050 
  # this requires a running Tor service in your machine and listening on port 9050 (by default)
  session.proxies = {"http": "socks5://localhost:9050", "https": "socks5://localhost:9050"}
  return session


def renew_connection(pw):
  """
  Contacts the Tor network configurations' ControlPort on port 9051 to authenticate itself and
  perform a recycle of a new Tor IP address.

  @param pw: str - A string containing the Tor password for the given system configuration.
  """

  with Controller.from_port(port=9051) as c:
    c.authenticate(password=pw)
    # send NEWNYM signal to establish a new clean connection through the Tor network
    c.signal(Signal.NEWNYM)

def main():
    """
    Main program which executes the tor checking program.
    """

    print("Executing tor_check...")

    s = get_tor_session()
    page = s.get("https://api.myip.com")
    s.close()
    
    print(page.text)
    
    print('------------------------------------------')
    renew_connection('your-password-here')

    s = get_tor_session()
    page = s.get("https://api.myip.com")
    s.close()

    print(page.text)

if __name__ == '__main__':
    main()