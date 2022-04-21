from bs4 import BeautifulSoup
import requests

#helper functions for site specific urls and part names
def encode_spaces(url : str) -> str:
    """Takes a string and returns it with whitespaces encoded with %20 for use in url"""
    return url.replace(' ', '%20')

def full_url(url: str) -> str:
    """Returns full functional url from href"""
    base_url = "https://www.urparts.com/"
    return base_url + encode_spaces(url)

def split_part_name(part_name: str) -> dict:
    """Takes full part name and returns a tuple of part number and part description"""
    part_number = ''
    part_desc = ''
    if '-' in part_name:
        partitioned_name = part_name.strip().rpartition('-')
        part_number,part_descr = partitioned_name[0], partitioned_name[2]
    else:
        part_number, part_descr = part_name, part_name
        
    return part_number.strip(),part_descr.strip()    

"""
Below are functuons defined to parse different levels of each catalogue heirarchy: 
manufacturer, category, model, section(optional) 
"""

def page_soup(url:str) -> BeautifulSoup:
    """Creates a BeautifulSoup object from url using desired parser features"""
    return BeautifulSoup(requests.get(url).content, features="html.parser") 

def parse_div(catalogue_level: str,soup:BeautifulSoup ,div_class: str) -> dict:
    """Takes a page soup and parses a div with given div_class. Returns a dict of name of catalogue level and relative reference"""
    container = soup.find("div", class_ = div_class)
    if container:
        return  [{catalogue_level:item.text.strip(), 'href':item['href']} for item in container.find_all('a')]
    else:
        return None

def scrape_model(model: dict, manufacturer: str, category: str, soup: BeautifulSoup) -> list:
    """Takes a dictionary of model,  with its name and href, manufacturer name and category name and the soup of manufacturer page and returns a list of dictionaries of each part on model page
    containing manufacurer, category, model, part number, part description and its url"""
    model_parts  = parse_div("part_name", soup,"c_container allparts")
    if not model_parts:
        return []
    for part in model_parts:
        part['manufacturer'] = manufacturer
        part['category'] = category
        part['model'] = model['model']
        part['part_number'], part['part_descr'] = split_part_name(part['part_name'])
        part['url'] = full_url(part['href'])
        part.pop('part_name', None)
        part.pop('href', None)
    return model_parts
    

def scrape_sections(sections:list, model: dict, manufacturer:str, category:str) -> list:
    """Takes a list of section of dctionaries from the model if they are present and scrapes each individual model"""
    section_parts =[]
    for section in sections:
        model_soup = page_soup(full_url(section['href']))
        section_parts = section_parts + scrape_model(model, manufacturer, category, model_soup)
    return section_parts


def build_manufacturers_catalogue(url: str) -> list:
    """Builds a list of dictionaries containing manufacurers, their sections and models"""
    manufacturers = []
    catalogue_soup = page_soup(url)
    manufacturers = parse_div("manufacturer", catalogue_soup,"c_container allmakes")
    for manufacturer in manufacturers:
        manufacturer_soup = page_soup(full_url(manufacturer['href']))
        manufacturer['categories'] = parse_div("category", manufacturer_soup,"c_container allmakes allcategories")
    for manufacturer in manufacturers :
        if 'categories' in manufacturer:
            for category in manufacturer['categories']:
                category_soup = page_soup(full_url(category['href']))
                category['models'] = parse_div("model", category_soup,"c_container allmodels")
        else:
            continue
    return manufacturers

def scrape_manufacturer_parts(manufacturer:dict) -> list:
    """Takes a dict contianing manufacturer name, its href and its categories and models and builds a list of parts for each model"""
    manufacturer_parts = []
    if 'categories' in manufacturer:
        for category in manufacturer['categories']:
            if category['models'] != None:
                for model in category['models']:
                    model_soup = page_soup(full_url(model['href']))
                    model_sections= parse_div("model_section", model_soup,"c_container modelSections") 
                    model_parts = []
                    if not model_sections:
                        model_parts = scrape_model(model,  manufacturer['manufacturer'], category['category'],model_soup )                         
                    else:                          
                        model_parts = scrape_sections(model_sections, model,  manufacturer['manufacturer'], category['category'])
                    manufacturer_parts  = manufacturer_parts  + model_parts
            else:
                continue
    return manufacturer_parts
 

if __name__ == '__main__':
    pass