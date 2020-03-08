# Tor Request

Tor proxy support for python requests.

## Dependencies
pip install pysocks  
pip install requests

**OR**: pip install -r requirements.txt

## Usage

```python
# Import TorRequest class
from TorRequest import TorRequest

# Call TorRequest with path to Tor executable
t = TorRequest('<full_path_to>/tor.exe') # Windows
t = TorRequest('/usr/local/bin/tor') # Mac OS X (default path)
t = TorRequest('/usr/sbin/tor') # Linux (default path)

# Send optional, comma-separated HTTP headers
headers = {'User-Agent': 'Mozilla/5.0'}
t = TorRequest('<path>', headers)

# Get status (true: connected, false: not connected)
t.status()

# Get Tor ip address
t.ipAddr()

# Get requests session object with binded Tor circuit
t.session()

# Get website content with anonymized request
t.get('https://gitlab.com/') # Returns HTML content
t.get('https://gitlab.com/', True) # Returns response object (contains HTTP status code, text, ...)

# Example: print HTTP status code
print(t.get('https://gitlab.com/', True).status_code)

# Send anonymized POST request to website (e.g. login credentials)
t.post('<url>', {'username': 'foo', 'password': 'bar'}) # Returns HTML content
t.post('<url>', {'key': 'value'}, True) # Returns response object
```

## Tor executable
### Windows
* Download Tor Browser Bundle from the [official website](https://www.torproject.org/de/download/) and install it
* Tor executable is placed inside <tbb_installation_path>\Browser\TorBrowser\Tor\tor.exe
* If you don't want to install the whole Tor Browser Bundle, you can also download just the [Tor source code](https://www.torproject.org/de/download/tor/)

### Mac OS X

* Install Tor using Homebrew via terminal: brew install tor
* Find installation path: which tor
* By default, installation path is /usr/local/bin/tor

### Linux

* Install Tor via terminal: apt install tor -y
* Find installation path: which tor
* By default, installation path is /usr/sbin/tor

### Warning
> For both Mac and Linux it's possible, to use that Tor executable that comes with the Tor Browser Bundle. I still recommend to use the Tor source code installed via terminal (for reason, see Troubleshooting section).

## Troubleshooting

>**Exception "SyntaxError (unicode error)" thrown**  
Use forward slashes for path string or mark this string as raw string (e.g. r'C:\Users\...\tor.exe'). You can also use double backslashes.

>**Error message "Missing dependencies for SOCKS support".**  
(Re-)install PySocks module.

>**Exception "SOCKSHTTPSConnectionPool" thrown.**  
This exception gets thrown, if you're using the Tor executable out of the Tor Browser Bundle in Linux while running the Browser itself. Use the Tor installation under /usr/sbin/tor to avoid this error.