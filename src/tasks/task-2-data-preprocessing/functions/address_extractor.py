"""
 The functions below are developed by @Shariar Hossain Omee

 get_detailed_address() :
    - Take a full address as input
    - Split the address into City, Area, Address
    - Return a dictionary containing City, Area (a.k.a. "Locality"), Address as keys

"""


def get_detailed_address(address):
    try:
        address = address.title()
        address_dict = {"city": "", "area": "", "address": ""}
        splitted_address = address.split(',')

        for i in reversed(splitted_address):
            if get_city_name(i.strip().replace('.', '')):
                address_dict["city"] = i.strip().replace('.', '')
                splitted_address.remove(i)
            elif get_area_name(i.strip().replace('.', '')):
                address_dict["area"] = i.strip().replace('.', '')
                splitted_address.remove(i)

        address_dict["address"] = ','.join(splitted_address)

        return address_dict

    except:
        return {"city": "", "area": "", "address": address}


def get_city_name(name):
    cities = ['Dhaka', 'Chattogram', 'Narayanganj City', 'Gazipur', 'Sylhet']

    try:
        cities.index(name)
        return True

    except:
        return False


def get_area_name(name):
    areas = ['10 No. North Kattali Ward', '11 No. South Kattali Ward', '15 No. Bagmoniram Ward',
             '16 No. Chawk Bazaar Ward', '22 No. Enayet Bazaar Ward', '29 No. West Madarbari Ward',
             '30 No. East Madarbari Ward', '31 No. Alkoron Ward', '32 No. Andarkilla Ward',
             '33 No. Firingee Bazaar Ward', '36 Goshail Danga Ward', '4 No Chandgaon Ward',
             '7 No. West Sholoshohor Ward', '9 No. North Pahartali Ward', 'Adabor', 'Aftab Nagar', 'Agargaon',
             'Ambarkhana', 'Badda', 'Bakalia', 'Banani', 'Banani Dohs', 'Banasree', 'Banglamotors', 'Bangshal',
             'Baridhara', 'Baridhara Dohs', 'Bashabo', 'Bashundhara R-A', 'Bayazid', 'Cantonment', 'Chandra',
             'Dakshin Khan', 'Demra', 'Dhanmondi', 'Double Mooring', 'Dumni', 'East Nasirabad', 'Eskaton', 'Fatulla',
             'Firojshah Colony', 'Gazipur Sadar Upazila', 'Gulistan', 'Gulshan', 'Halishahar', 'Hathazari', 'Hatirpool',
             'Hazaribag', 'Ibrahimpur', 'Jalalabad Housing Society', 'Jamal Khan', 'Jatra Bari', 'Joar Sahara',
             'Kachukhet', 'Kafrul', 'Kakrail', 'Kalabagan', 'Kalachandpur', 'Kamrangirchar', 'Kathalbagan',
             'Kazir Dewri', 'Keraniganj', 'Khilgaon', 'Khilkhet', 'Khulshi', 'Kotwali', 'Kuril', 'Lal Khan Bazaar',
             'Lalbagh', 'Lalmatia', 'Maghbazar', 'Malibagh', 'Maniknagar', 'Mirpur', 'Mohakhali', 'Mohakhali Dohs',
             'Mohammadpur', 'Motijheel', 'Mugdapara', 'Muradpur', 'Nadda', 'Narayanganj', 'New Market', 'Niketan',
             'Nikunja', 'North Shahjahanpur', 'Panchlaish', 'Paribagh', 'Patenga', 'Purbachal', 'Railway Colony',
             'Rampura', 'Riaj Uddin Bazar', 'Sagorika Bscic Industrial Area', 'Savar', 'Shahbagh', 'Shahjahanpur',
             'Shantinagar', 'Shegunbagicha', 'Shiddheswari', 'Shiddhirganj', 'Sholokbahar', 'Shyamoli', 'Shyampur',
             'Sreepur', 'Sutrapur', 'Taltola', 'Tejgaon', 'Turag', 'Uttar Khan', 'Uttar Lalkhan', 'Uttara', 'Zafrabad',
             'Zindabazar', 'Siddeshwari', 'Bashundhara', 'Bashundhara Riverview', 'North  Nandipara', 'Keraniganj',
             'South Banasree', 'Nandipara', 'Aftabnagar', 'Modhubag', 'Senpara Porbota', 'Bosila', 'East Rampura',
             'Mugda', 'Mohammadpur', 'West Khulshi', 'Bashundhara R/A', 'West Rampura', 'Chawkbazar', 'Chandanpur']

    try:
        areas.index(name)
        return True

    except:
        return False
