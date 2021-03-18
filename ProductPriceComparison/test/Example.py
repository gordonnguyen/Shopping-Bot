import bs4, requests
 
headers = {'User-Agent':'Mozilla/5.0(Macintosh;Intel Mac OS X 10_9_5)''AppleWebkit 537.36(KHTML,like Gecko) Chrome', 'Accept':'text/html,application/xhtml+xml,application/xml;'
'q=0.9,image/webp,*/*;q=0.8'}

web_response = requests.get("http://www.amazon.com/Automate-Boring-Stuff-Python-Programming/dp/1593275994/", headers=headers)
web_response.raise_for_status()
 
soup1 = bs4.BeautifulSoup(web_response.text, "html.parser")
soup2 = bs4.BeautifulSoup(soup1.prettify(), "html.parser")
 
elems = soup2.select("#buyNewSection > h5 > div > div.a-column.a-span8.a-text-right.a-span-last > div > span.a-size-medium.a-color-price.offer-price.a-text-normal")
 
price = elems[0].text.strip()
 
print("The price for the referenced item is: " + price)