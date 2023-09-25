import requests

# this code is supposed to scrape yohnanof
# application/json; charset=utf-8

url = 'https://shop.hazi-hinam.co.il/proxy/api/item/getItemsPromoted?SortBy=-1'
url2 = 'https://shop.hazi-hinam.co.il/proxy/api/item/getItemsBySubCategory?Id=11252&IsDescending=false&SortBy=-1&filter%5BFILTER_Mivza%5D=false'
cookies = {'H_UUID' : '483abd3f-ec02-48c6-ad0f-b5fd7143213b; ai_user=2fxD6fFPu/0y1PgG/BtCdg|2023-09-23T11:47:40.879Z; H_Authentication=%7B%22access_token%22%3A%226DD8544D62F50E54EC61EFCA1A63177861566534603666CD1D66DF61985A9E29%22%2C%22expires_in%22%3A172800.0%2C%22error%22%3Anull%7D; HR=98900A52AF43FD54066E46625FCFFCF507539EE78F90C18B6DA5E28AD3A9CFFC; _ga=GA1.3.751488461.1695469661; ai_session=tsEu4EoCfKqvOaPFH8jv7E|1695640805067|1695640805067; _gid=GA1.3.919359160.1695640830; _gat_UA-73663136-1=1; _ga_DWQR296QD4=GS1.3.1695640830.2.0.1695640830.60.0.0; _ga_NC6GJM5Y37=GS1.1.1695640804.2.1.1695640836.28.0.0'}

headers = {'Content-type': 'application/json'}
r = requests.get(url2, headers=headers, cookies=cookies)
print(r.json())