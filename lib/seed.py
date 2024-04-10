from bs4 import BeautifulSoup
from urllib.request import Request, urlopen

# Send a GET request to the URL
response = Request('https://www.autoevolution.com/cars/', headers={'User-agent': 'Mozilla/5.0'})
webpage = urlopen(response).read()
print(webpage)


