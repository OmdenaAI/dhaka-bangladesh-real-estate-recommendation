
def is_relaxation_amenity(amenity:str)->bool:
    """
        Tell whether the parameter is a relaxation amenity or not. 
    """
    amenities=["sauna","swimming pool","gymnasium","steam room","jacuzzi",
               "fitness center","steam room","barbeque area"]
    return amenity.replace("_"," ").replace("-"," ").lower() in amenities



def is_security_amenity(amenity:str)->bool:
    """
        Tell whether the parameter is a security amenity or not.
    """
    amenities=["emergency exit", "fire alarm", "fire extinguisher", "cctv", "security guard",
               "emergency stairs","cctv security","security staff",
               "reception","reception desk and lobby","intercom",]
    return amenity.replace("_"," ").replace("-"," ").lower() in amenities

def is_maintenance_or_cleaning_amenity(amenity:str)->bool:
    """
        Tell whether the parameter is a maintenance or cleaning amenity or not.
    """
    amenities=["maintenance staff", "cleaning services", "waste disposal"]
    return amenity.replace("_"," ").replace("-"," ").lower() in amenities

def is_social_amenity(amenity:str)->bool:
    """
        Tell whether the parameter is a social amenity or not.
    """
    amenities=["community center","lawn or garden","prayer room","facilities for disabled",
               "conference room","landscape garden", "business center"]
    return amenity.replace("_"," ").replace("-"," ").lower() in amenities

def is_expendable_amenity(amenity:str)->bool:
    """
        Tell whether the parameter is an expendable amenity or not.
    """
    amenities=["storage areas","24 hours concierge","lobby in building","service elevators","double glazed windows",
               "rooftop garden"]
    return amenity.replace("_"," ").replace("-"," ").lower() in amenities

def is_service_staff_amenity(amenity:str)->bool:
    """
        Tell whether the parameter is an service staff amenity or not.
    """
    amenities=["driver room","servant room","staff toilet","guard room"]
    return amenity.replace("_"," ").replace("-"," ").lower() in amenities

def is_unclassify_amenity(amenity:str)->bool:
    """
        Tell whether the parameter is an unclassify amenity or not.
    """
    amenities=["flooring","view","floor level","atm facility","freehold","furnished",
               "central heating","first aid medical center","day care center","shared kitchen",
               "cafeteria or canteen","laundry facility","wasa","electricity","child allowed",
               "pet allowed","safety grill","govt gas","hot water","floor number","available for amenity",
               "furnished status","advance deposit","drawing room","floor type","dining room","kitchen","negotiable",
               "service charge","property condition","living room","air conditioning"]
    return amenity.replace("_"," ").replace("-"," ").lower() in amenities


