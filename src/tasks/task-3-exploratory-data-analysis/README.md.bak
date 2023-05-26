# Bangladesh Real-Estate Data Exploration

## Dataset

The data consists of informations regarding 33,000+ properties, including price, area, locality, city, and other property attributes.
The dataset can be found [here](https://github.com/OmdenaAI/dhaka-bangladesh-real-estate-recommendation/blob/main/src/data/Merged_Data/cleaned_merged_datasets.csv), with features described below:
* **area**: the area occupied by the property, in sqft
* **building_type**: the type of the property (shop, apartment, duplex, ...)
* **building_nature**: the nature of the property (residential, commercial)
* **image_url**: the link toward the property's image
* **num_bath_rooms**: number of available bathrooms
* **num_bed_rooms**: number of available bedrooms
* **price**: property's price
* **property_description**: property's description (contain many details)
* **property_overview**: property's overview (quick presentation)
* **property_url**: link toward the the property's publication page (the page from which the information was scrapped)
* **image_url**: the link toward the property's image
* **purpose**: Rent/Sale
* **city**: city in which the property is located
* **locality**: locality in which the property is located
* **address**: property's address
* **id**: id given to the current sample (will be usefull for the recommender engine)
* **image_url**: the link toward the property's image
* **relaxation_amenity_count**: number of relaxation amenities the property has
* **security_amenity_count**: number of security amenities the property has
* **maintenance_or_cleaning_amenity_count**: number of maintenance or cleaning amenities the property has
* **social_amenity_count**: number of social amenities in the vicinity of the property
* **expendable_amenity_count**: number of expendable amenities the property has
* **service_staff_amenity_count**: number of relaxation amenities the property has
* **unclassify_amenity_count**: number of unclassified amenities (not part of the above mentionned amenities' category) the property has
* **relaxation_amenity_count**: number of relaxation amenities the property has
* **division**: division in which the property is located; a division is a group of cities based on how near they are from each other
* **zone**: zone in which the property is located; a zone is a group of localities based on how near they are from each other


## Summary of Findings

In the exploration, we found that there was a strong relationship between prices and features such as `area`, `building_type`, and most of the `*_amenity_count`.
We also found that:
* properties density in an area is also impacting the trending prices
* the price increases exponentially with `area`, `num_bath_rooms`, and `num_bed_rooms`.
* there are amenities with little effect on the prices: `maintenance_or_cleaning_amenity_count`, `service_staff_amenity_count`
And there is a skew in our data toward "Apartment" `building_type`


## Key Insights for Presentation

-
