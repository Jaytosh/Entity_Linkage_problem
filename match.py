import json
import io
def readproducts( path ):
    with open( path ) as product_list:
        content = product_list.readlines()
    products = []
    counter  = 0
    for line in content:
        product = json.loads( line )
        product["position"] = counter                       #give a key to every entity
        product["listing"]  = []                            
        products.append( product )
        counter = counter + 1
    return products
def product_by_manufacturer( products ):                    # store by manufacturer
    product_by_manufacturer = {}
    for product in products:
        if product[ "manufacturer" ] in product_by_manufacturer.keys():
            product_by_manufacturer[ product[ "manufacturer" ] ].append( product )
        else:
            product_by_manufacturer[ product[ "manufacturer" ] ] = []
            product_by_manufacturer[ product[ "manufacturer" ] ].append( product )
    return product_by_manufacturer
def man_to_man( product_manufacturers, listing_manufacturers ):
    man_to_man = {}
    for listing_manufacturer in listing_manufacturers:
        for product_manufacturer in product_manufacturers:
            if product_manufacturer.lower() in listing_manufacturer.lower():
                man_to_man[ listing_manufacturer ] = product_manufacturer       # same as camera mnufacturer
                continue
        if listing_manufacturer not in man_to_man.keys():
            man_to_man[ listing_manufacturer ] = "None"         # not name of any camera manufacturer
    return man_to_man
products = readproducts( "products.txt" )                       # parse products
listings = readproducts( "listings.txt" )                       # parse listings
prod_man = product_by_manufacturer( products )                  
list_man = product_by_manufacturer( listings )
man_to_man = man_to_man( prod_man, list_man )                   # get listing manufaturer to product manufacturer links
for listing in listings:                        #as listing will be more frequently added
    target = man_to_man[ listing[ "manufacturer" ] ]                #check if manufacturer is the manufacturer of camera also
    if target != "None" :                                           
        search_space = prod_man[ target ]                           # search space reduced
    else:
        search_space = products
    title = listing[ "title" ]
    if target != "None" :
        for product in search_space:
            if product["model"] in title :                          # only check for title
                product["listing"].append( listing["position"] )
    else:
        for product in search_space:
            if product["model"] in title and product["manufacturer"] in title:
                if "family" in product.keys():
                    if product["family"] in title:                  # if family exist check for it also
                        product["listing"].append( listing["position"] )
                else:
                    product["listing"].append( listing["position"] )
Result = []
for product in products:
    Temp = {}
    Temp["product_name"] = product["product_name"]
    Temp["listings"] = []
    for position in product["listing"]:
        Temp["listings"].append(listings[ position ] )
    Result.append( Temp )
import io, json
with io.open('result.txt', 'w', encoding='utf-8') as f:
    for res in Result:
        f.write(unicode(json.dumps(res, ensure_ascii=False)+"\n"))
                               
                               
    

