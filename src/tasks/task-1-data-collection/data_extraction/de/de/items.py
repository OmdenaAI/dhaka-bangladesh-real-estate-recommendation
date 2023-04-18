
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
    property_description = Field()
    property_overview = Field()
    commercial_type = Field()
    image_url = Field()

class PBazarItem(Item):

    property_type = Field()
    price_per_month = Field()
    price_per_sft = Field()
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
    road_width_ft = Field()
    garage_number = Field()
    property_url = Field()
    price = Field()

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
    num_bed =Field()
    num_bath=Field()
    area = Field()
    amenities = Field()
    address = Field()
    building_type = Field()
    title = Field()
    price_in_BDT = Field()
    details = Field()
    purpose = Field()
    listing_url = Field() 

class iqibdPropsItem(Item):
    # define the fields for your item here like:
    # name = Field()
    property_link = Field()
    price = Field()
    location = Field()
    num_bed_rooms = Field()
    num_bath_rooms = Field()
    area = Field()
    building_type = Field()
    floor=Field()
    land_size=Field()
    garage = Field()
    year_built= Field()
    status = Field()
    num_balcony = Field()
    interior = Field()
    unit = Field()
    wifi = Field()
    parking = Field()
    security = Field()
    elevator = Field()
    emergency_stairs = Field()

    generator = Field()
    tv_cable = Field()
    government_gas = Field()
    cctv= Field()
    reception= Field()
    swimming_pool= Field()
    balcony = Field()
    garden = Field()
    fitness_center=Field()
    air_conditioning=Field()
    central_heating = Field()
    pets_allow = Field()
    servant_room = Field()


class ToleterItem(Item):
     

    # define the fields for your item here like:

     
    PropertyType = Field()
    Amenities = Field()
    MainFeatures = Field()
    Bedroom=Field()
    Bathroom=Field()
    Status=Field()
    #  PropertySize = Field()
    #  Floors = Field()
    Location = Field()
    PricePerMonth =Field()
    Description = Field()
    NearByLocation= Field()
    url=Field()


class BdstallItem(Item):
    # define the fields for your item here like:
    PropertyType = Field()
    Size = Field()
    Amenities = Field()
    Bathroom=Field()
    Status=Field()
    Bed = Field()
    PricePerMonth =Field()
    Description = Field()
    Location= Field()
    url=Field()
