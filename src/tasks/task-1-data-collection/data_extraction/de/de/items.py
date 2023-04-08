
from scrapy.item import Item, Field

class BpPropertyItem(Item):
    # define the fields for your item here like:
    price = Field()
    location = Field()
    num_bed_rooms = Field()
    num_bath_rooms = Field()
    area = Field()
    building_type = Field()
    purpose = Field()
    amenities = Field()
    property_url= Field()

class PBazarItem(Item):

    property_type = Field()
    price_per_month = Field()
    price_per_sft = Field()
    price = Field()
    location = Field()
    area_sft = Field()
    attach_bathrooms = Field()
    common_bathrooms = Field()
    bedrooms = Field()
    floor = Field()
    floor_type = Field()
    parking = Field()
    total_floor = Field()
    size_in_katha = Field()
    view = Field()
    road_width = Field()