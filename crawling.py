import requests
import json
from bs4 import BeautifulSoup as bs

url3= "https://oldschool.runescape.wiki"
url = "https://oldschool.runescape.wiki/w/"
url2= "https://oldschool.runescape.wiki/w/Category:"

def get_sub_categories(soup,subcategories_links): #1 finds sub-categories links
    data = soup.find("div",id= "mw-subcategories")
    data2 = data.find("div",class_="mw-content-ltr")
    data3 = data2.find_all("ul")
    for ul in data3:
        lis = ul.find_all("li")
        for li in lis:
            subcategories_links.append(li.find("a")["href"])
    #print(subcategories_links)

    return subcategories_links

def add_subcategories_items(url3,subcategories_links,values): #2 add to values items using the subcategories links
    new_sub_links = []
    for link in subcategories_links[:1]:
        res = requests.get(url3+link)
        soup = bs(res.content,"html.parser")
        tags=soup.find(text='Subcategories')
        data = soup.find("div",class_= "mw-content-ltr")
        data2 = data.find_all("ul")
        if(tags=="Subcategories"):
            new_sub_links = get_sub_categories(soup,new_sub_links)
            #print(new_sub_links)
            values = add_subcategories_items(url3,new_sub_links,values)
            
        for ul in data2:
            lis = ul.find_all("li")
            for li in lis:
                values.append(li.find("a").text.strip())
    #print(values)
    
    return values

def add_rest_items(values,key): #3 finding the rest of the items in the first page
    res =requests.get(url2 + key)
    soup = bs(res.content,"html.parser")
    div3 = soup.find('div',id ="mw-pages")
    div3_groups = div3.find_all('div',class_="mw-category-group")
    for group3 in div3_groups:
        ul = group3.find('ul')
        lis = ul.find_all("li")
        for li in lis:
            values.append(li.find("a").text.strip())
    #print(values)
    return values

def check_next_page(soup,values): #4 checks for next page and adding items to value
    tag = soup.find(text='next page')
    if(tag=="next page"):
        div = soup.find('div',id ="mw-pages")
        page = div.find("a")["href"]
        res= requests.get(url3+page)
        data=bs(res.content,"html.parser")
        div_groups = data.find_all('div',class_="mw-category-group")
        for group3 in div_groups:
            ul = group3.find('ul')
            lis = ul.find_all("li")
            for li in lis:
                values.append(li.find("a").text.strip())
    return values
        
def get_all_normal_items(): 
    normal_items = []
    
    with open('osrs_all_Items.json', 'r') as f:
        all_items_names = json.loads(f.read())

    keys = list(all_items_names.keys())

    for i in keys:
        try:
            if(all_items_names[f'{i}']['type'] == 'normal'):
                normal_items += [all_items_names[f'{i}']['name']]
        except:
            continue
    
    get_items_info(normal_items)
    
def get_items_info(normal_items):
    counter = 0
    f = open ("output.csv","w")
    f.write("Released,Members,Quest item,Tradeable,Equipable,Stackable,Options,Destory,Examine,Value,High alch,Low alch,Weight,Price,Buy limit,Daily volume,Category\n")
    for name in normal_items[:50]:
        keys = []
        values = []
        item_data = {}

        res = requests.get(url + name)
        soup = bs(res.content, "html.parser")

        table = soup.find('table',{'class':'infobox-item'})
        table_body = table.find('tbody')
        rows = table_body.find_all('tr')

        dict_items = dict()
        
        for row in rows:

            children = row.findChildren(recursive=False)
            if len(children) == 2:
                keys = [x.getText() for x in row.find_all('th')]
                values = [x.getText() for x in row.find_all('td')]

                for key,value in zip(keys,values):
                    dict_items[key] = value

        counter=counter+1
        with open('keys.json','r') as w:
            item_data = json.load(w)

        for i,key in enumerate(dict_items):
            item_data[key] = dict_items[key].replace(',','')

        f.write(f'{item_data["Released"]},{item_data["Members"]},{item_data["Quest item"]},{item_data["Tradeable"]},{item_data["Equipable"]},{item_data["Stackable"]},{item_data["Options"]},{item_data["Destroy"]},{item_data["Examine"]},{item_data["Value"]},{item_data["High alch"]},{item_data["Low alch"]},{item_data["Weight"]},{item_data["Exchange"]},{item_data["Buy limit"]},{item_data["Daily volume"]},{None}\n')
    f.close()
    #print(counter)
    #print(item_data)

def categorizing_item():
    keys = [ "Armour","Construction","Crafting items","Farming","Firemaking","Fishing",
    "Fletching","Food","Hunter","Mining","Prayer items","Runecraft","Smithing","Runes","Weapons","Woodcutting" ]
    values = []
    subcategories_links = []
    categories = {}

    for key in keys[6:7]:
        res =requests.get(url2 + key)
        soup = bs(res.content,"html.parser")
        tags = soup.find(text='Subcategories')      
        if(tags=="Subcategories"):
            subcategories_links= get_sub_categories(soup,subcategories_links)
    
        values = add_subcategories_items(url3,subcategories_links,values)
        values = add_rest_items(values,key)
        values = check_next_page(soup,values)
    
    print(values)


#categorizing_item()
get_all_normal_items()












        



        




        

#get_all_normal_items()
