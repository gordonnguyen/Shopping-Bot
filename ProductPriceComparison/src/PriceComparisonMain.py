from getEbayPrice import getProductPrice
import openpyxl



def main():
    watchlist_workbook = openpyxl.load_workbook('ProductWatchList.xlsx')
    sheet = watchlist_workbook.get_sheet_by_name('Sheet1')
    price_list = []
    name_list = []
    price_list, name_list = getNameandPrice(sheet)


    # Convert this:
    #save_price_and_name(product_price, product_name, sheet, watchlist_workbook)

def getNameandPrice(sheet):
    price_list = []
    name_list = []

    # Convert to list (multiple products)
    for i in sheet:
        price_list, name_list = getProductPrice(sheet.cell(row,col).value)
        #product_price, product_name = getProductPrice(sheet['F2'].value)
        
    print('The product_price of \"'+product_name+'\" on Ebay is',product_price)


def save_price_and_name(product_price, product_name, sheet, watchlist_workbook):
    sheet['A2'].value = product_name
    sheet['B2'].value = product_price
    watchlist_workbook.save('NewWatchList.xlsx')

main()
