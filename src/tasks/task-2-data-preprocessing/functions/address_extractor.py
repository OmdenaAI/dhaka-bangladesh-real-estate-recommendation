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
                     '7 No. West Sholoshohor Ward', '9 No. North Pahartali Ward', 'Adabor', 'Aftab Nagar', 'Aftabnagar',
                     'Agargaon', 'Airport', 'Akkelpur', 'Ambarkhana', 'Araihazar', 'Badda', 'Bagerhat Sadar', 'Bagha',
                     'Bakalia', 'Banani', 'Banani Dohs', 'Banashree', 'Banasree', 'Bandar', 'Bandarban Sadar',
                     'Banglamotor', 'Banglamotors', 'Bangshal', 'Banshkhali', 'Barguna Sadar', 'Baridhara',
                     'Baridhara Dohs', 'Barishal City', 'Basabo', 'Bashabo', 'Bashundhara', 'Bashundhara R-A',
                     'Bashundhara R/A', 'Bashundhara RA', 'Bashundhara Riverview', 'Bayazid', 'Belabo', 'Bhairab',
                     'Bhaluka', 'Bhandaria', 'Bhashantek ', 'Bhola Sadar', 'Birampur', 'Boalkhali', 'Boalmari',
                     'Bogura Sadar', 'Bosila', 'Botiaghata', 'Brahmanbaria Sadar', 'Cantonment', 'Chack Bazar',
                     'Chandanpur', 'Chandpur Sadar', 'Chandra', 'Chapainawabganj Sadar', 'Chattogram City',
                     'Chauddagram', 'Chawkbazar', 'Chhagalnaiya', 'Chunarughat', "Cox's Bazar Sadar", 'Cumilla City',
                     'DOHS Banani', 'DOHS Baridhara', 'DOHS Mirpur', 'DOHS Mohakhali', 'Dakshin Khan', 'Dakshinsurma',
                     'Daskhinkhan', 'Debidwar', 'Demra', 'Dhamrai', 'Dhanmondi', 'Digholia', 'Dinajpur Sadar', 'Dohar ',
                     'Double Mooring', 'Dumni', 'East Nasirabad', 'East Rampura', 'Eskaton', 'Fakirhat',
                     'Faridpur Sadar', 'Farmgate', 'Fatulla', 'Fenchuganj', 'Feni Sadar', 'Firojshah Colony',
                     'Fulbaria', 'Gaibandha Sadar', 'Gajaria', 'Gandaria ', 'Gazipur Sadar', 'Gazipur Sadar Upazila',
                     'Ghatail', 'Gopalganj Sadar', 'Gulistan', 'Gulshan', 'Gulshan 1', 'Gulshan 2', 'Habiganj Sadar',
                     'Halishahar', 'Hathazari', 'Hatirpool', 'Hazaribag', 'Hazaribag ', 'Ibrahimpur', 'Jaintiapur',
                     'Jalalabad Housing Society', 'Jamal Khan', 'Jamalpur Sadar', 'Jashore Sadar', 'Jatra Bari',
                     'Jatrabari', 'Jhalakathi Sadar', 'Jhenaidah Sadar', 'Joar Sahara', 'Joypurhat Sadar', 'Kachukhet',
                     'Kadamtali', 'Kafrul', 'Kakrail', 'Kalabagan', 'Kalachandpur', 'Kalapara', 'Kaliakair', 'Kaliganj',
                     'Kalkini', 'Kallaynpur', 'Kamarkhand', 'Kamrangir Char', 'Kamrangirchar', 'Karnafuli',
                     'Karwan Bazar', 'Kathalbagan', 'Kazir Dewri', 'Keraniganj', 'Khilgaon', 'Khilkhet', 'Khulna City',
                     'Khulshi', 'Kotwali', 'Kuril', 'Kushtia Sadar', 'Lakshmipur Sadar', 'Lal Khan Bazaar', 'Lalbag',
                     'Lalbagh', 'Lalmatia', 'Lalpur', 'Madaripur Sadar', 'Maghbazar', 'Magura Sadar', 'Malibagh',
                     'Manikganj Sadar', 'Maniknagar', 'Mirpur', 'Mirsharai', 'Modhubag', 'Moghbazar', 'Mohakhali',
                     'Mohakhali Dohs', 'Mohammadpur', 'Mohammadpur ', 'Mongla', 'Motijheel', 'Moulvibazar Sadar',
                     'Mugda', 'Mugda Para', 'Mugdapara', 'Muktagacha', 'Munshiganj Sadar', 'Muradpur',
                     'Mymensingh City', 'Nadda', 'Nandipara', 'Nangalkot', 'Naogaon Sadar', 'Narayanganj',
                     'Narsingdi Sadar', 'Natore Sadar', 'Netrokona Sadar', 'New Market', 'Niketan', 'Nikunja',
                     'Nilphamari Sadar', 'Noakhali Sadar', 'North  Nandipara', 'North Shahjahanpur', 'Pabna Sadar',
                     'Pakundia', 'Pallabi ', 'Paltan', 'Panchagarh Sadar', 'Panchlaish', 'Paribagh', 'Patenga',
                     'Patuakhali Sadar', 'Purbachal', 'Puthia', 'Railway Colony', 'Rajasthali', 'Rajbari Sadar',
                     'Rajoir', 'Rajshahi City', 'Ramna', 'Rampura', 'Rangpur City', 'Ranisankail', 'Riaj Uddin Bazar',
                     'Rupganj', 'Rupnagar', 'Rupsha', 'Sabujbag', 'Sagorika Bscic Industrial Area', 'Sakhipur',
                     'Sarishabari', 'Satkhira Sadar', 'Savar', 'Senpara Porbota', 'Shah Ali', 'Shahbag ', 'Shahbagh',
                     'Shahjahanpur', 'Shajahanpur', 'Shantinagar', 'Shariatpur Sadar', 'Shegunbagicha',
                     'Sher E Bangla Nagar ', 'Sherpur Sadar', 'Shibpur', 'Shiddheswari', 'Shiddhirganj', 'Sholokbahar',
                     'Shyamoli', 'Shyampur', 'Shyampur ', 'Siddeshwari', 'Singiar', 'Sirajganj Sadar', 'Sitakunda',
                     'Sonargaon', 'South Banasree', 'Sreemangal', 'Sreepur', 'Sunamganj Sadar', 'Sutrapur',
                     'Sylhet City', 'Taltali', 'Taltola', 'Tangail Sadar', 'Tarakanda', 'Tejgaon', 'Tejgaon I/A',
                     'Tetulia', 'Thakurgaon Sadar', 'Tongi', 'Turag', 'Ullapara', 'Uttar Khan', 'Uttar Lalkhan',
                     'Uttara', 'Uttara East', 'Uttara West', 'Uttarkhan', 'Vatara ', 'Wari', 'West Khulshi',
                     'West Rampura', 'Zafrabad', 'Zindabazar']

    try:
        areas.index(name)
        return True

    except:
        return False
