import pymongo
import parts_scraper_tools as pst
import logging

"""This scraper saves all individual parts from urparts.com catalogue"""

CATALOGUE_URL = "https://www.urparts.com/index.cfm/page/catalogue"


logging.basicConfig(filename='scraper.log',
                    filemode='w',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.INFO)


def main():
    manufacturers = pst.build_manufacturers_catalogue(CATALOGUE_URL)
    mongo_client = pymongo.MongoClient("mongodb://db:27017/")
    target_db = mongo_client["parts_db"]
    target_col = target_db["part"]
    target_col.drop()
    for manufacturer in manufacturers:
        logging.info(f"Processing manufacturer: {manufacturer['manufacturer']}")        
        manufacturer_parts = pst.scrape_manufacturer_parts(manufacturer)
        if manufacturer_parts:
            target_col.insert_many(manufacturer_parts)
        logging.info(f"Saved {len(manufacturer_parts)} parts from {manufacturer['manufacturer']}")


    


if __name__ == '__main__':
    main()