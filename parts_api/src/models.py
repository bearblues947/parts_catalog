from mongoengine import Document, StringField

class Part(Document):
    manufacturer = StringField()
    category = StringField()
    model = StringField()
    part_number = StringField()
    part_descr = StringField()
    url = StringField()
