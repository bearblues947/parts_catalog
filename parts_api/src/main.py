from unittest import result
from fastapi import FastAPI, Query
from app.src.models import Part
from mongoengine import connect
from mongoengine.queryset.visitor import Q
import json


description = """
UrParts API allows you to search a scraped version of parts catalogue from urparts.com
"""

tags_metadata = [
    {
        "name": "parts",
        "description": "Sarch parts. You can cross-reference part details using the original catalogue.",
        "externalDocs": {
            "description": "Parts original catalogue",
            "url": "https://www.urparts.com/index.cfm/page/catalogue",
        },
    },
]


app = FastAPI( title="UrPartsAPI",
    description=description,
    version="0.0.1",
    contact={
    "name": "Nik G",
    "email": "nicknsg@outlook.com"
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    }, 
    openapi_tags=tags_metadata
)

connect(db = "parts_db", host="db", port = 27017)

@app.get('/')
def home():
    return "Welcome To UrPartsAPI"

@app.get("/parts",  tags =['parts']) 
async def get_parts_sample(limit:int = 2) -> dict:
    parts = json.loads(Part.objects()[:limit].to_json())
    return {'parts': parts} 

@app.get("/search_model_parts",  tags =['parts'])
def search_model_parts(manufacturer:str, category:str, model:str, part_number: str = Query(None))  -> dict:
    result_set =Part.objects.filter(manufacturer__icontains= manufacturer,
                                             category__icontains= category,
                                             model__icontains= model) 
    if part_number:
        result_set = result_set.filter(part_number= part_number)
    return {"parts": json.loads(result_set.to_json()) }

@app.get("/search_parts",  tags =['parts'])
def search_parts(part_number:str, part_descr: str = Query(None))  -> dict:
    if part_descr: 
        parts = json.loads(Part.objects.filter(part_number__icontains= part_number, part_descr__icontains= part_descr) .to_json())
    else:
       parts = json.loads(Part.objects.filter(part_number__icontains= part_number).to_json())                 
    return {"parts": parts }

@app.get("/parts_count", tags =['parts'])
def parts_count() ->int :
    return Part.objects.count()