import model_sarang

prediction = model_sarang.make_prediction({
    'division': 'Dhaka',
    'building_type': 'Appartment',
    'building_nature': 'Residential',
    'purpose': 'Rent',
    'zone': 'Mohammadpur',
    'num_bed_rooms': 3,
    'num_bath_rooms': 3,
    'area': 1100
})

print(f"Predicted Price: {prediction}")
