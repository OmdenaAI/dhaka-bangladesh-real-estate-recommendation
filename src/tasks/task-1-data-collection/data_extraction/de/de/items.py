
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
    parking_space = Field()
    balcony = Field()
    dining = Field()
    living = Field()
    total_floor = Field()
    size_in_katha = Field()
    view = Field()
    road_width = Field()
    land_katha = Field()

class ashSpiderItem(Item):
    # define the fields for your item here like:
    location = Field()
    price = Field()
    bedrooms = Field()
    bathrooms = Field()
    area = Field()
    ptype = Field()
    pstatus = Field()
    garage = Field()
    url = Field()
    amenities = Field()
    
    
    class RentalHomeBD(Item):
    # define the fields for your item here like:
    basic_info = Field()
    amenities = Field()
    address = Field()
    type = Field()
    title = Field()
    price_in_BDT = Field()
    details = Field()
    purpose = Field()
    page_url = Field()
    listing_url = Field()
