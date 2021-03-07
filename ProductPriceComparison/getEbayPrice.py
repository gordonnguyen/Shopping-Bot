import bs4, requests, openpyxl

HEADERS = ({'User-Agent':
            'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
            'Accept-Language': 'en-US, en;q=0.5'})

EBAY_URL = "https://www.ebay.com/"
EBAY_PRICE_HTML_SELECTOR = ('#prcIsum', '#mm-saleDscPrc', '#prcIsum_bidPrice')
EBAY_NAME_HTML_SELECTOR = '#itemTitle'

STAPLE_URL = 'staples.com'
STAPLE_PRICE_HTML_SELECTOR = ('#priceInfoContainer > div > div.price-info__final_price')
STAPLE_NAME_HTML_SELECTOR = '#product_title'


def getProductPrice(product_url):
    res = requests.get(product_url, HEADERS)
    res.raise_for_status()
    print('Connection Status:',res.status_code)
    soup = bs4.BeautifulSoup(res.text, "html.parser")
    
    if EBAY_URL in product_url:
        product_name = soup.select(EBAY_NAME_HTML_SELECTOR)
        product_price = getPricefromHTML(soup, EBAY_PRICE_HTML_SELECTOR)
        '''
        for selector in EBAY_PRICE_HTML_SELECTOR:
            product_price = soup.select(selector)
            if product_price != '':
                break
        '''
        #if product_price == []:
        #    product_price = 'No product_price available'
        print(product_price)
        print(product_name[0].text.replace('Details about', '').strip())

        return product_price[0].text.strip(), product_name[0].text.replace('Details about', '').strip()
        #return product_price[0].text.strip(), product_name[0].text.replace('Details about', '').strip() 
    elif STAPLE_URL in product_url:
        product_name = soup.select(STAPLE_NAME_HTML_SELECTOR)
        product_price = getPricefromHTML(soup, STAPLE_PRICE_HTML_SELECTOR)
        return product_price[0].text.strip(' $'), product_name[0].text.strip()


def getPricefromHTML(soup, PRICE_HTML_SELECTOR):
    for selector in PRICE_HTML_SELECTOR:
        product_price = soup.select(selector)
        if product_price != '':
            return product_price

'''
    if product_price == []:
        product_price = soup.select('#mm-saleDscPrc')

    elif 'camelcamelcamel.com' in product_url:
        product_price = soup.select('#content > div:nth-child(2) > div.column.column-block.small-12.medium-3.medium-text-right > div:nth-child(1) > div.column.small-8.medium-12 > p > span > span')
        return product_price
'''


#product_url = input("Enter Drop\'s product URL: ")

#if product_url == '':
#    product_url = input(pyperclip.paste)

#product_price = getProductPrice(product_url)
#print('The product_price on Ebay is',product_price)