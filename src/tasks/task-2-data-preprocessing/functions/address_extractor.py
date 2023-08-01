"""
 The functions below are developed by @Shariar Hossain Omee

 get_detailed_address() :
    - Take a full comma separated address as input
    - Split the address into City, Area, Address
    - Return a dictionary containing division, city, zone, locality (a.k.a. area), address as keys

This function splits input address according to the commas, then it checks each separated string with the values in
the arrays which we pre-defined in the function. It will return one area name under the 'locality' key and one city name
under the 'city' key, if it could match them with the pre-defined areas and cities in the function , the rest of the
string or address will be under the 'address' key. Then, according to the 'locality' it finds the 'zone' for that area,
as well as, it finds 'division' according to the 'city'.

For example,
    Input --> "Block M, South Banasree Project, Banasree, Dhaka"
    Output --> {"divison": "Dhaka", "city": "Dhaka", "zone": "Khilgaon" "locality": "Banasree", "address": "Block M, South Banasree Project"}

Note: The input has to be comma separated in order to get meaningful output like the example above. Otherwise, it
won't recognize the address properly.

please, see the commented notebook of bproperty (https://github.com/OmdenaAI/dhaka-bangladesh-real-estate-
recommendation/blob/main/src/tasks/task-2-data-preprocessing/bproperty%20--%20cleaning/bproperty%20--%20cleaning.ipynb)
for use.

Note: This function doesn't have all the areas and cities of Bangladesh yet. I am adding them periodically according
to the upload cleaned dataset.
"""


def get_detailed_address(address):
    try:
        # converting the initial letter of each word to a capital letter of input.
        address = address.title()

        # defining output dictionary
        address_dict = {"division": "", "city": "", "zone": "", "locality": "", "address": ""}

        # splitting the input according to commas
        splitted_address = address.split(',')

        # getting each splitted and checking them with pre-defined address and area names.
        for i in reversed(splitted_address):

            # calling get_city_name() and passing name from splitted address
            if get_city_name(i.strip().replace('.', '')):
                # assigning matched city name under the "city" key.
                address_dict["city"] = i.strip().replace('.', '')
                # removing the matched name from the splitted address list.
                splitted_address.remove(i)

            # calling get_area_name() and passing name from splitted address
            elif get_area_name(i.strip().replace('.', '')):
                # assigning matched area name under the "area" key.
                address_dict["locality"] = i.strip().replace('.', '')
                # removing the matched name from the splitted address list.
                splitted_address.remove(i)

        # joining the rest of the input and assigning it under the "address" key.
        address_dict["address"] = ','.join(splitted_address)

        # called get_division() and passing "city" in order to find 'division'
        address_dict["division"] = get_division(address_dict["city"])
        # called get_zone() and passing "locality" in order to find 'zone'
        address_dict["zone"] = get_zone(address_dict["locality"])

        # returning the output dictionary
        return address_dict

    except:

        # if any exception occurs, it assigns the whole input under the "address" key and return the dictionary
        return {"division": "", "city": "", "zone": "", "locality": "", "address": address}


def get_city_name(name):
    # a list containing different cities and districts of Bangladesh
    cities = ['Bandar', 'Bandarban', 'Barguna', 'Barishal', 'Bhairab', 'Bhola', 'Bogra', 'Bogura', 'Brahmanbaria',
              'Chandpur', 'Chapai Nawabganj', 'Chattogram', 'Chittagong', 'Chowmuhani', 'Chuadanga', 'Comilla',
              'Coxs Bazar', 'Cumilla', 'Cumilla Sadar Dakshin', 'Dhaka', 'Dinajpur', 'Faridpur', 'Feni', 'Gaibandha',
              'Gazipur', 'Gopalganj', 'Habiganj', 'Jamalpur', 'Jashore', 'Jessore', 'Jhalokathi', 'Jhenaidah',
              'Joypurhat', 'Kaliakair', 'Khagrachari', 'Khulna', 'Kishoreganj', 'Kurigram', 'Kushtia', 'Kustia',
              'Lalmonirhat', 'Laxmipur', 'Madaripur', 'Magura', 'Maijdee', 'Manikganj', 'Maulvibazar', 'Meherpur',
              'Munsiganj', 'Mymensingh', 'Naogaon', 'Narail', 'Narayanganj', 'Narayanganj City', 'Narayangonj',
              'Narsingdi', 'Natore', 'Nawabganj', 'Netrokona', 'Nilphamari', 'Noakhali', 'Pabna', 'Panchagarh',
              'Pirojpur', 'Potuakhali', 'Rajbari', 'Rajshahi', 'Rangamati', 'Rangpur', 'Saidpur', 'Satkhira', 'Savar',
              'Shariatpur', 'Sherpur', 'Siddhirganj', 'Sirajganj', 'Sonargoan', 'Sreepur', 'Sunamganj', 'Sylhet',
              'Tangail', 'Tarabo', 'Thakurgaon', 'Tongi', 'TongiBagerhat', 'Coxs Bazar']

    try:

        # if it finds match with the input, it returns true.
        cities.index(name)
        return True

    except:

        # if it doesn't find any match with the input, it returns false.
        return False


def get_area_name(name):
    # a list containing different areas of Bangladesh
    areas = ['33 No. Firingee Bazaar Ward', '22 No. Enayet Bazaar Ward', '15 No. Bagmoniram Ward',
             '9 No. North Pahartali Ward', '11 No. South Kattali Ward', '15 No. Bagmoniram Ward',
             '16 No. Chawk Bazaar Ward',
             '22 No. Enayet Bazaar Ward', '29 No. West Madarbari Ward', '30 No. East Madarbari Ward',
             '31 No. Alkoron Ward', '32 No. Andarkilla Ward', '33 No. Firingee Bazaar Ward', '36 Goshail Danga Ward',
             '4 No Chandgaon Ward', '7 No. West Sholoshohor Ward', '9 No. North Pahartali Ward', 'Adabar', 'Adabor',
             'Aftab Nagar', 'Aftabnagar', 'Agargaon', 'Agrabad', 'Airport', 'Akhaura', 'Akkelpur', 'Alamdanga',
             'Ambarkhana', 'Araihazar', 'Arapur', 'Ashkona', 'Ashulia', 'Azimpur', 'Azompur', 'Badarganj', 'Badda',
             'Bagerhat', 'Bagerhat Sadar', 'Bagha', 'Baily Road', 'Baipayl', 'Bajitpur', 'Bakalia', 'Banani',
             'Banani Dohs', 'BananiDOHS', 'Banashree', 'Banasree', 'Bandar', 'Bandarban', 'Bandarban Sadar',
             'Bangla Motor', 'Banglamotor', 'Banglamotors', 'Bangshal', 'Banshkhali', 'Baraigram', 'Barguna',
             'Barguna Sadar', 'Baridhara', 'Baridhara Diplomatic Zone', 'Baridhara Dohs', 'Barishal City', 'Barlekha',
             'Barura', 'Basabo', 'Bashabo', 'Bashundhara', 'Bashundhara R /A', 'Bashundhara R-A', 'Bashundhara R/A',
             'Bashundhara RA', 'Bashundhara Residential Area', 'Bashundhara Riverview', 'Basila', 'Basundhara',
             'Basurhat', 'Bayazid', 'Beani Bazar', 'Belabo', 'Belkuchi', 'Benapole', 'Bera', 'Bhairab', 'Bhaluka',
             'Bhandaria', 'Bhanga', 'Bhangura', 'Bhashantek ', 'Bheramara', 'Bhola', 'Bhola Sadar', 'Bhuapur',
             'Birampur', 'Birganj', 'Boalkhali', 'Boalmari', 'Bogura Sadar', 'Boshila', 'Bosila', 'Botiaghata',
             'Brahmanbaria Sadar', 'Cantonment', 'Chack Bazar', 'Chak Bazar', 'Chakaria', 'Chandanaish', 'Chandanpur',
             'Chandgaon', 'Chandina', 'Chandpur', 'Chandpur Sadar', 'Chandra', 'Chapainawabganj Sadar', 'Char Fasson',
             'Charghat', 'Chatkhil', 'Chattogram City', 'Chauddagram', 'Chaugachha', 'Chaumohoni', 'Chawkbazar',
             'Chhagalnaiya', 'Chhatak', 'Chhengarchar', 'Choukbazar', 'Chuadanga', 'Chunarughat', 'Comilla Cantonment',
             'Cornelhat', "Cox's Bazar Sadar", 'Coxs Bazar', 'Cumilla City', 'DOHS Banani', 'DOHS Baridhara',
             'DOHS Mirpur', 'DOHS Mohakhali', 'Daganbhuiyan', 'DakhinKhan', 'Dakshin Khan', 'Dakshinsurma', 'Darshana',
             'Daskhinkhan', 'Daudkandi', 'Debidwar', 'Demra', 'Derai', 'Dewanganj', 'Dhaka Cantonment', 'Dhamrai',
             'Dhanbari', 'Dhanmondi', 'Dhour', 'Digholia', 'Dinajpur Sadar', 'Diyabari', 'Dohar', 'Dohar ',
             'Double Mooring', 'Dumni', 'Dupchanchia', 'Durgapur', 'East Nasirabad', 'East Rampura', 'Elephant Rd',
             'ElephantRoad', 'Eskaton', 'Fakirhat', 'Faridganj', 'Faridpur', 'Faridpur City', 'Faridpur Sadar',
             'Farmgate', 'Fatulla', 'Faujdarhat', 'Fenchuganj', 'Feni', 'Feni Sadar', 'Firojshah Colony', 'Fulbaria',
             'Gabtali', 'Gabtoli', 'Gaffargaon', 'Gaibandha', 'Gaibandha Sadar', 'Gajaria', 'Galachipa', 'Gandaria ',
             'Gangni', 'Gaurnadi', 'Gazipur Sadar', 'Gazipur Sadar Upazila', 'Ghatail', 'Ghoraghat', 'Ghorashal',
             'Goalunda Ghat', 'Gobindaganj', 'Godagari', 'Gohail Road', 'Golapganj', 'Gollamari', 'Golmari',
             'Gopalganj', 'Gopalganj Sadar', 'Gopalpur', 'Goran', 'Gouripur', 'Green Road', 'Gulistan', 'Gulshan',
             'Gulshan 01', 'Gulshan 02', 'Gulshan 1', 'Gulshan 2', 'Gulshan One', 'Gulshan-1', 'Gulshan-2',
             'Gurudaspur', 'Habiganj', 'Habiganj Sadar', 'Hajiganj', 'Hakimpur', 'Halishahar', 'Haragacha',
             'Harinakundu', 'Hathazari', 'Hatirpool', 'Hatiya', 'Hazaribag', 'Hazaribag ', 'Hemayetpur', 'Homna',
             'Hossainpur', 'Ibrahimpur', 'Ishwardi', 'Ishwarganj', 'Islampur', 'Jagannathpur', 'Jaintiapur',
             'Jaipurhat', 'Jajira', 'Jalalabad Housing Society', 'Jaldhaka', 'Jamal Khan', 'Jamalpur Sadar',
             'Jashore Sadar', 'Jatra Bari', 'Jatrabari', 'Jhalakathi Sadar', 'Jhalakati', 'Jhenaidah',
             'Jhenaidah Sadar', 'Jhigatala', 'Jhikargacha', 'Jibannagar', 'Joar Sahara', 'Joydebpur', 'Joypurhat Sadar',
             'Kachua', 'Kachukhet', 'Kadamtali', 'Kafrul', 'Kakrail', 'Kalabagan', 'Kalachandpur', 'Kalapara',
             'Kalaroa', 'Kalia', 'Kaliakair', 'Kaliganj', 'Kalihati', 'Kalkini', 'Kallayanpur', 'Kallaynpur',
             'Kallyanpur', 'Kalurghat', 'Kalyanpur', 'Kamalapur', 'Kamarkhand', 'Kamrangir Char', 'Kamrangirchar',
             'Kanaighat', 'Kanchan', 'Karimganj', 'Karnafuli', 'Karwan Bazar', 'Kasba', 'Katakhali', 'Kathalbagan',
             'Katiadi', 'Kawran Bazar', 'Kazipara', 'Kazir Dewri', 'Kemal Ataturk Avenue', 'Kendua', 'Keraniganj',
             'Keshabpur', 'Kesharhat', 'Khagrachhari', 'Khan Jahan Ali', 'Khilgaon', 'Khilkhet', 'Khulna City',
             'Khulshi', 'Kishoreganj', 'Kona Bari', 'Kotchandpur', 'Kotwali', 'Kulaura', 'Kuliarchar', 'Kumarkhali',
             'Kurigram', 'Kuril', 'Kushtia', 'Kushtia Sadar', 'Laksham', 'Lakshmipur', 'Lakshmipur Sadar',
             'Lal Khan Bazaar', 'Lalbag', 'Lalbagh', 'Lalmatia', 'Lalmohan', 'Lalmonirhat', 'Lalpur', 'Lama',
             'Lohagara', 'Madani Avenue', 'Madarganj', 'Madaripur', 'Madaripur Sadar', 'Madhabadi', 'Madhabdi',
             'Madhabpur', 'Madhupur', 'Maghbazar', 'Magura', 'Magura Sadar', 'Maheshkhali', 'Maheshpur', 'Malibag',
             'Malibagh', 'Manikganj Sadar', 'Maniknagar', 'Manirampur', 'Matiranga', 'Matlab', 'Matuail',
             'Maulvi Bazar', 'Mehendiganj', 'Meherpur', 'Melandaha', 'Mirkadim', 'Mirpur', 'Mirpur 1', 'Mirpur 10',
             'Mirpur 11', 'Mirpur 12', 'Mirpur 13', 'Mirpur 14', 'Mirpur 2', 'Mirpur 6', 'Mirpur Dohs', 'MirpurDOHS',
             'Mirsharai', 'Mirzapur', 'Mithapukur', 'Modhubag', 'Mogbazar', 'Moghbazar', 'Mohakhali', 'Mohakhali Dohs',
             'MohakhaliDOHS', 'Mohammadpur', 'Mohammadpur ', 'Mohanganj', 'Mongla', 'Monipur10 No. North Kattali Ward',
             'Morrelganj', 'Motijheel', 'Moulvibazar Sadar', 'Mugda', 'Mugda Para', 'Mugdapara', 'Muksudpur',
             'Muktagacha', 'Muktagachha', 'Muladi', 'Mundumala', 'Munshiganj', 'Munshiganj Sadar', 'Muradpur',
             'Mymensingh City', 'Nabiganj', 'Nabinagar', 'Nadda', 'Nageshwari', 'Nakhalpara', 'Nakla', 'Nalchiti',
             'Nalitabari', 'Nandail', 'Nandipara', 'Nangalkot', 'Naogaon Sadar', 'Naohata', 'Narail', 'Narayanganj',
             'Narayangonj Sadar', 'Naria', 'Narinda', 'Narsingdi Sadar', 'Nasirbad', 'Natore', 'Natore Sadar',
             'Naya Paltan', 'NayaPaltan', 'Nazipur', 'Netrakona', 'Netrokona Sadar', 'New Eskaton', 'New Market',
             'Niketan', 'Niketon', 'Nikunja', 'Nikunjo', 'Nilphamari', 'Nilphamari Sadar', 'Noakhali', 'Noakhali Sadar',
             'Noapara', 'North  Nandipara', 'North Shahjahanpur', 'Pabna Sadar', 'Pahartali', 'Pakundia', 'Pallabi',
             'Pallabi ', 'Paltan', 'Panchagarh', 'Panchagarh Sadar', 'Panchbibi', 'Panchlaish', 'Pangsha', 'Panthapath',
             'Parbatipur', 'Paribagh', 'Parshuram', 'Patenga', 'Patgram', 'Patiya', 'Patuakhali', 'Patuakhali Sadar',
             'Phulbari', 'Phulpur', 'Pirerbag', 'Pirganj', 'Pirojpur', 'Progoti Sarani', 'Pubail', 'Puran Bogra',
             'Purana Paltan', 'Purbachal', 'Purbachal New Town', 'Puthia', 'Rahanpur', 'Railway Colony', 'Raipur',
             'Raipura', 'Rajabazar', 'Rajasthali', 'Rajbari', 'Rajbari Sadar', 'Rajoir', 'Rajshahi City', 'Ramganj',
             'Ramgarh', 'Ramgati', 'Ramna', 'Rampura', 'Rangamati', 'Rangpur City', 'Rangpur City Corporation',
             'Rangunia', 'Ranisankail', 'Raozan', 'Rayer Bazar', 'Riaj Uddin Bazar', 'Rupganj', 'Rupnagar', 'Rupsha',
             'Sabujbag', 'Sadar', 'Sagorika Bscic Industrial Area', 'Saidpur', 'Sakhipur', 'Sandwip', 'Santahar',
             'Santhia', 'Sarishabari', 'Satkania', 'Satkhira', 'Satkhira Sadar', 'Savar', 'Segun Bagicha', 'Senbagh',
             'Senpara Porbota', 'Setabganj', 'Shagun Bagicha', 'Shah Ali', 'Shahbag ', 'Shahbagh', 'Shahjadpur',
             'Shahjahanpur', 'Shahporan', 'Shahrasti', 'Shailkupa', 'Shaistaganj', 'Shajahanpur', 'Shanti Nagar',
             'Shantinagar', 'Shariatpur', 'Shariatpur Sadar', 'Shegunbagicha', 'Sher E Bangla Nagar ', 'Sherpur',
             'Sherpur Sadar', 'Shewrapara', 'Shibchar', 'Shibganj', 'Shibpur', 'Shiddeshwari', 'Shiddheswari',
             'Shiddhirganj', 'Shitakunda', 'Sholokbahar', 'Shukrabad', 'Shyamoli', 'Shyampur', 'Shyampur ',
             'Siddeshwari', 'Singair', 'Singiar', 'Singra', 'Sirajganj', 'Sirajganj Sadar', 'Sitakunda', 'Sokipur',
             'Sonadanga', 'Sonagazi', 'Sonaimuri', 'Sonargaon', 'Sonatala', 'South Banasree', 'Sreebardi', 'Sreemangal',
             'Sreepur', 'Subid Bazar', 'Sujanagar', 'Sunamganj', 'Sunamganj Sadar', 'Sutrapur', 'Swarupkati',
             'Sylhet City', 'Taltali', 'Taltola', 'Tangail Sadar', 'Tanore', 'Tarabo', 'Tarakanda', 'Tejgaon',
             'Tejgaon I/A', 'Teknaf', 'Tetulia', 'Thakurgaon', 'Thakurgaon Sadar', 'Tikatuli', 'Tongi', 'Trishal',
             'Turag', 'Ulipur', 'Ullahpara', 'Ullapara', 'Uposhohor', 'Uttar Khan', 'Uttar Lalkhan', 'Uttara',
             'Uttara East', 'Uttara West', 'Uttarkhan', 'Valuka', 'Vatara', 'Vatara ', 'Wari', 'West Dhanmondi',
             'West Khulshi', 'West Rampura', 'Zafrabad', 'Zigatola', 'Zindabazar', 'Zirabo', 'Nikunja 1', 'Dhaka south',
             'Mirpur-1', 'Khilgoan', 'Kazi Para', 'Dakkhin Khan', 'Agargoan', 'Mirpur-2', 'Mirpur-11', 'Madartek',
             'Mirpur-10', 'Keranigonj', 'Kathal Bagan', 'Mirpur-8', 'Mirpur-12', 'Mirpur-6']

    try:

        # if it finds match with the input, it returns true.
        areas.index(name)
        return True

    except:

        # if it doesn't find any match with the input, it returns false.
        return False


"""
get_division():
    - takes a city name as a string
    - returns a division name string (returns an emtpy string ("") if it finds none)
    
Note: Please, input one city name only. Make sure there is no other character along with the input, otherwise, it won't
recognize it. For example,

    wrong inputs --> "Dhaka.", ",Dhaka", "/ Dhaka,"
    Correct input --> "Dhaka"
"""


def get_division(city_name):
    # removing spacing before and after if there are any
    city_name = city_name.strip()

    # a dictionary of divisions and their cities
    divisions = {
        'Dhaka': ['Tongi', 'Tarabo', 'Tangail', 'Sreepur', 'Sonargoan', 'Siddhirganj', 'Shariatpur', 'Savar', 'Rajbari',
                  'Nawabganj', 'Narsingdi', 'Narayanganj', 'Narayanganj City', 'Narayangonj', 'Munsiganj', 'Manikganj',
                  'Madaripur', 'Kishoreganj', 'Kaliakair', 'Gopalganj', 'Gazipur', 'Faridpur', 'Bandar', 'Bhairab',
                  'Dhaka', ],
        'Chattogram': ['Coxs Bazar', 'Rangamati', 'Noakhali', 'Maijdee', 'Laxmipur', 'Khagrachari', 'Feni', 'Cumilla',
                       'Cumilla Sadar Dakshin', 'Coxs Bazar', 'Comilla', 'Chowmuhani', 'Chattogram', 'Chittagong',
                       'Chandpur', 'Brahmanbaria', 'Bandarban', ],
        'Barisal': ['Potuakhali', 'Pirojpur', 'Jhalokathi', 'Barguna', 'Barishal', 'Bhola', ],
        'Khulna': ['TongiBagerhat', 'Satkhira', 'Narail', 'Meherpur', 'Magura', 'Kustia', 'Kushtia', 'Khulna',
                   'Chuadanga',
                   'Jashore', 'Jessore', 'Jhenaidah', ],
        'Mymensingh': ['Sherpur', 'Netrokona', 'Mymensingh', 'Jamalpur', 'Joypurhat', ],
        'Rajshahi': ['Sirajganj', 'Rajshahi', 'Pabna', 'Natore', 'Naogaon', 'Chapai Nawabganj', 'Bogra', 'Bogura', ],
        'Rangpur': ['Thakurgaon', 'Saidpur', 'Rangpur', 'Panchagarh', 'Nilphamari', 'Lalmonirhat', 'Kurigram',
                    'Dinajpur',
                    'Gaibandha', ],
        'Sylhet': ['Habiganj', 'Maulvibazar', 'Sunamganj', 'Sylhet', ],
    }

    # finding division name according the input city name. If it finds match then, it returns the division name
    for division, cities in divisions.items():
        for city in cities:
            if city_name == city:
                return division

    # if it finds none, then it returns an emtpy string.
    return ""


"""
 get_zone():
    - takes a locality as a string
    - returns a zone name string (returns an emtpy string ("") if it finds none)

Note: Please, input one locality only. Make sure there is no other character along with the input, otherwise, it won't
recognize it. For example,

    wrong inputs --> "Banasree.", ",Banasree", ". Banasree,"
    Correct input --> "Banasree"
"""


def get_zone(locality_name):
    # removing spacing before and after if there are any
    locality_name = locality_name.strip()

    # a dictionary of zones and their localities
    zones = {
        'Mirpur': ['Kazi Para', 'Shewrapara', 'Rupnagar', 'Pirerbag', 'Pallabi ', 'Pallabi', 'Kafrul', 'Kachukhet',
                   'Ibrahimpur', 'Mirpur', 'Mirpur 1', 'Mirpur 10', 'Mirpur 11', 'Mirpur 12', 'Mirpur 13', 'Mirpur 14',
                   'Mirpur 2', 'Mirpur 6', 'Mirpur Dohs', 'MirpurDOHS', 'Mirpur-1', 'Mirpur-2', 'Mirpur-11', 'Mirpur-8',
                   'Mirpur-12', 'Mirpur-6', 'Mirpur-10', 'DOHS Mirpur', 'Kazipara', 'Bhashantek ', 'Senpara Porbota',
                   'Shah Ali', ],
        'Bashundhara R/A': ['Bashundhara R.A', 'Bashundhara', 'Bashundhara R /A', 'Bashundhara R-A', 'Bashundhara R/A',
                            'Bashundhara RA',
                            'Bashundhara Residential Area', 'Bashundhara Riverview', 'Basundhara'],
        'Chattogram City': ['33 No. Firingee Bazaar Ward', '22 No. Enayet Bazaar Ward', '15 No. Bagmoniram Ward',
                            '9 No. North Pahartali Ward', 'Sholokbahar', 'Sagorika Bscic Industrial Area', 'Nasirbad',
                            'Khulshi', 'Kazir Dewri',
                            'Kalurghat', 'Jamal Khan', 'Chandgaon', 'Bayazid', 'West Khulshi', 'Uttar Lalkhan',
                            'Riaj Uddin Bazar', 'Patenga', 'Pahartali', 'Muradpur', 'Lal Khan Bazaar', 'Halishahar',
                            'Firojshah Colony', 'Jalalabad Housing Society', 'East Nasirabad', 'Double Mooring',
                            'Cornelhat', 'Chattogram City', 'Bandar', '11 No. South Kattali Ward',
                            '15 No. Bagmoniram Ward',
                            '16 No. Chawk Bazaar Ward', '22 No. Enayet Bazaar Ward', '29 No. West Madarbari Ward',
                            '30 No. East Madarbari Ward', '31 No. Alkoron Ward', '32 No. Andarkilla Ward',
                            '33 No. Firingee Bazaar Ward', '36 Goshail Danga Ward', '4 No Chandgaon Ward',
                            '7 No. West Sholoshohor Ward', '9 No. North Pahartali Ward',
                            'Monipur10 No. North Kattali Ward',
                            'Agrabad', '10 No. North Kattali Ward'],
        'Sub-district of Chattogram': ['Sitakunda', 'Shitakunda', 'Satkania', 'Sandwip', 'Raozan', 'Rangunia', 'Patiya',
                                       'Panchlaish', 'Mirsharai', 'Lohagara', 'Karnafuli', 'Hathazari', 'Faujdarhat',
                                       'Chandanaish', 'Boalkhali', 'Banshkhali', 'Akhaura', 'Bakalia', ],
        'Sub-district of Chuadanga': ['Jibannagar', 'Alamdanga', 'Chuadanga', 'Darshana', ],
        'Sylhet City': ['Zindabazar', 'Uposhohor', 'Sylhet City', 'Ambarkhana', 'Subid Bazar'],
        'Sub-district of Joypurhat': ['Panchbibi', 'Joypurhat Sadar', 'Jaipurhat', 'Akkelpur', ],
        'Sub-district of Dhaka': ['Dhaka south', 'Kanchan', 'Dohar', 'Dohar ', 'Dumni', ],
        'Sub-district of Sylhet': ['Sreemangal', 'Shahporan', 'Kanaighat', 'Jaintiapur', 'Golapganj', 'Dakshinsurma',
                                   'Fenchuganj', ],
        'Sub-district of Narayanganj': ['Tarabo', 'Sonargaon', 'Shiddhirganj', 'Rupganj', 'Narayangonj Sadar',
                                        'Narayanganj', 'Araihazar', 'Fatulla', ],
        'Sub-district of Kishoreganj': ['Pakundia', 'Kuliarchar', 'Kishoreganj', 'Katiadi', 'Karimganj', 'Hossainpur',
                                        'Bajitpur', 'Bhairab', ],
        'Sub-district of Rangpur': ['Rangpur City', 'Rangpur City Corporation', 'Pirganj', 'Mithapukur', 'Haragacha',
                                    'Badarganj', ],
        'Sub-district of Rajshahi': ['Tanore', 'Rajshahi City', 'Puthia', 'Naohata', 'Mundumala', 'Kesharhat',
                                     'Godagari',
                                     'Bagha', 'Charghat', ],
        'Sub-district of Chapainawabganj': ['Chapainawabganj Sadar', 'Rahanpur', ],
        'Sub-district of Sunamganj': ['Sunamganj', 'Sunamganj Sadar', 'Jagannathpur', 'Chhatak', 'Derai', ],
        'Sub-district of Natore': ['Singra', 'Natore', 'Natore Sadar', 'Lalpur', 'Baraigram', 'Gurudaspur', ],
        'Sub-district of Jamalpur': ['Sarishabari', 'Melandaha', 'Madarganj', 'Jamalpur Sadar', 'Dewanganj', ],
        'Sub-district of Shariatpur': ['Jajira', 'Naria', 'Shariatpur', 'Shariatpur Sadar', ],
        'Sub-district of Thakurgaon': ['Ranisankail', 'Thakurgaon', 'Thakurgaon Sadar', ],
        'Sub-district of Madaripur': ['Shibchar', 'Madaripur', 'Madaripur Sadar', 'Kalkini', 'Rajoir', ],
        'Sub-district of Khagrachari': ['Ramgarh', 'Matiranga', 'Khagrachhari', ],
        'Sub-district of Nilphamari': ['Saidpur', 'Nilphamari', 'Nilphamari Sadar', 'Jaldhaka', ],
        'Sub-district of Jhenaidah': ['Shailkupa', 'Maheshpur', 'Kotchandpur', 'Jhenaidah Sadar', 'Jhenaidah',
                                      'Harinakundu', ],
        'Sub-district of Feni': ['Sonagazi', 'Parshuram', 'Feni', 'Feni Sadar', 'Chhagalnaiya', 'Daganbhuiyan', ],
        'Sub-district of Habiganj': ['Shaistaganj', 'Nabiganj', 'Madhabpur', 'Madhupur', 'Chunarughat', 'Habiganj',
                                     'Habiganj Sadar', ],
        'Sub-district of Moulvibazar': ['Moulvibazar Sadar', 'Maulvi Bazar', 'Kulaura', 'Barlekha', ],
        'Sub-district of Bogura': ['Sonatala', 'Shibganj', 'Shajahanpur', 'Santahar', 'Gohail Road', 'Bogura Sadar',
                                   'Puran Bogra', ],
        'Sub-district of Barguna': ['Taltali', 'Dupchanchia', 'Barguna', 'Barguna Sadar', ],
        'Sub-district of Barishal': ['Muladi', 'Mehendiganj', 'Barishal City', 'Gaurnadi', ],
        'Sub-district of Cumilla': ['Nangalkot', 'Laksham', 'Homna', 'Debidwar', 'Daudkandi', 'Cumilla City',
                                    'Comilla Cantonment', 'Barura', 'Chandina', 'Chauddagram', ],
        'Sub-district of Noakhali': ['Sonaimuri', 'Senbagh', 'Noakhali', 'Noakhali Sadar', 'Hatiya', 'Basurhat',
                                     'Chatkhil',
                                     'Chaumohoni', ],
        'Sub-district of Gazipur': ['Tongi', 'Sreepur', 'Pubail', 'Kona Bari', 'Kaliganj', 'Kaliakair', 'Joydebpur',
                                    'Chandra', 'Gazipur Sadar', 'Gazipur Sadar Upazila', ],
        'Sub-district of Patuakhali': ['Patuakhali', 'Patuakhali Sadar', 'Kalapara', 'Galachipa', ],
        'Sub-district of Netrokona': ['Kendua', 'Durgapur', 'Netrakona', 'Netrokona Sadar', ],
        'Sub-district of Gopalganj': ['Muksudpur', 'Gopalganj', 'Gopalganj Sadar', ],
        'Sub-district of Meherpur': ['Gangni', 'Meherpur', ],
        'Sub-district of Jhalokati': ['Nalchiti', 'Jhalakathi Sadar', 'Jhalakati', ],
        'Sub-district of Narsingdi': ['Shibpur', 'Raipura', 'Narsingdi Sadar', 'Madhabadi', 'Madhabdi', 'Belabo',
                                      'Ghorashal', ],
        'Sub-district of Munshiganj': ['Singair', 'Munshiganj', 'Munshiganj Sadar', 'Gajaria', 'Mirkadim', ],
        'Sub-district of Narail': ['Kalia', 'Narail', ],
        'Sub-district of Panchagarh': ['Panchagarh', 'Panchagarh Sadar', 'Tetulia', ],
        'Sub-district of Naogaon': ['Naogaon Sadar', 'Nazipur', ],
        'Sub-district of Manikganj': ['Manikganj Sadar', ],
        'Sub-district of Rangamati': ['Rajasthali', 'Rangamati', ],
        'Sub-district of Magura': ['Magura', 'Magura Sadar', 'Kalia', ],
        'Sub-district of Lalmonirhat': ['Patgram', 'Lalmonirhat', ],
        'Sub-district of Lakshmipur': ['Ramgati', 'Ramganj', 'Lakshmipur', 'Lakshmipur Sadar', 'Raipur', ],
        'Sub-district of Kurigram': ['Ulipur', 'Nageshwari', 'Kurigram', ],
        'Sub-district of Gaibandha': ['Gobindaganj', 'Gaibandha', 'Gaibandha Sadar', ],
        'Sub-district of Sirajganj': ['Ullahpara', 'Ullapara', 'Sirajganj', 'Sirajganj Sadar', 'Shahjadpur',
                                      'Kamarkhand',
                                      'Belkuchi', ],
        'Sub-district of Jessore': ['Noapara', 'Manirampur', 'Keshabpur', 'Jhikargacha', 'Jashore Sadar', 'Benapole',
                                    'Chaugachha', ],
        'Sub-district of Pabna': ['Sujanagar', 'Santhia', 'Pabna Sadar', 'Ishwardi', 'Bera', 'Bhangura', ],
        'Sub-district of Rajbari': ['Goalunda Ghat', 'Pangsha', 'Rajbari', 'Rajbari Sadar', ],
        'Sub-district of Sherpur': ['Sreebardi', 'Sherpur Sadar', 'Sherpur', 'Nakla', 'Nalitabari', ],
        'Sub-district of Chandpur': ['Chhengarchar', 'Matlab', 'Shahrasti', 'Kachua', 'Hajiganj', 'Faridganj',
                                     'Chandpur',
                                     'Chandpur Sadar'],
        'Sub-district of Faridpur': ['Faridpur', 'Faridpur City', 'Faridpur Sadar', 'Bhanga', 'Boalmari', ],
        'Sub-district of Kushtia': ['Kushtia', 'Kushtia Sadar', 'Kumarkhali', 'Bheramara', ],
        'Sub-district of Khulna': ['Khan Jahan Ali', 'Sonadanga', 'Khulna City', 'Rupsha', 'Gollamari', 'Golmari',
                                   'Botiaghata', 'Digholia', ],
        'Sub-district of Satkhira': ['Satkhira', 'Satkhira Sadar', 'Kalaroa', 'Chandanpur', ],
        'Sub-district of Bhola': ['Lalmohan', 'Bhola', 'Bhola Sadar', 'Char Fasson', ],
        'Sub-district of Mymensingh': ['Islampur', 'Valuka', 'Trishal', 'Tarakanda', 'Phulpur', 'Nandail',
                                       'Mymensingh City', 'Muktagacha', 'Muktagachha', 'Mohanganj', 'Ishwarganj',
                                       'Gouripur', 'Bhaluka', 'Fulbaria', 'Gaffargaon', ],
        'Sub-district of Tangail': ['Tangail Sadar', 'Sokipur', 'Sakhipur', 'Mirzapur', 'Kalihati', 'Gopalpur',
                                    'Bhuapur',
                                    'Dhanbari', 'Ghatail', ],
        'Sub-district of Dinajpur': ['Setabganj', 'Phulbari', 'Parbatipur', 'Hakimpur', 'Ghoraghat', 'Birampur',
                                     'Birganj',
                                     'Dinajpur Sadar', ],
        'Sub-district of Pirojpur': ['Swarupkati', 'Bhandaria', 'Pirojpur', ],
        "Sub-district of Cox's Bazar": ['Teknaf', 'Maheshkhali', 'Chakaria', "Cox's Bazar Sadar", 'Coxs Bazar', ],
        'Sub-district of Brahmanbaria': ['Nabinagar', 'Kasba', 'Brahmanbaria Sadar', ],
        'Sub-district of Bandarban': ['Lama', 'Bandarban', 'Bandarban Sadar', ],
        'Sub-district of Bagerhat': ['Morrelganj', 'Mongla', 'Katakhali', 'Fakirhat', 'Bagerhat', 'Bagerhat Sadar', ],
        'Banani': ['Banani', 'Banani Dohs', 'BananiDOHS', 'DOHS Banani', 'Kemal Ataturk Avenue'],
        'Gulshan': ['Madani Avenue', 'Gulshan', 'Gulshan 01', 'Gulshan 02', 'Gulshan 1', 'Gulshan 2', 'Gulshan One',
                    'Gulshan-1', 'Gulshan-2', 'DOHS Baridhara', 'Baridhara', 'Baridhara Diplomatic Zone',
                    'Baridhara Dohs', ],
        'Mohammadpur': ['Zafrabad', 'Adabar', 'Adabor', 'Mohammadpur', 'Mohammadpur ', 'Lalmatia', 'Basila', 'Boshila',
                        'Bosila', ],
        'Shyamoli': ['Kalyanpur', 'Shyamoli', 'Kallayanpur', 'Kallaynpur', 'Kallyanpur', ],
        'Mohakhali': ['Niketan', 'Niketon', 'DOHS Mohakhali', 'Mohakhali', 'Mohakhali Dohs', 'MohakhaliDOHS', ],
        'Khilgaon': ['Shahjahanpur', 'Rampura', 'Madartek', 'Khilgoan', 'West Rampura', 'Taltola', 'South Banasree',
                     'Khilgaon', 'Basabo', 'Bashabo', 'Taltola', 'Goran', 'East Rampura', 'Banashree', 'Banasree',
                     'Aftab Nagar', 'Aftabnagar'],
        'Kurmitola': ['Airport', 'Ashkona', ],
        'Savar': ['Zirabo', 'Savar', 'Hemayetpur', 'Baipayl', 'Ashulia', 'Beani Bazar', 'Dhamrai', ],
        'Old Dhaka': ['Narinda', 'Choukbazar', 'Lalbag', 'Lalbagh', 'Kotwali', 'Kamrangirchar', 'Kamrangir Char',
                      'Chawkbazar', 'Azimpur', 'Azompur', 'Bangshal', 'Chack Bazar', 'Chak Bazar', ],
        'Badda': ['Kalachandpur', 'Badda', 'Nadda', 'Vatara', 'Vatara ', ],
        'Dakshin Khan': ['Dakkhin Khan', 'Uttarkhan', 'Uttar Khan', 'DakhinKhan', 'Dakshin Khan', 'Daskhinkhan', ],
        'Demra': ['Demra', 'Matuail', 'Shyampur ', ],
        'Dhaka Cantonment': ['Cantonment', ],
        'Dhanmondi': ['Jhigatala', 'Zigatola', 'West Dhanmondi', 'Shukrabad', 'Dhanmondi', 'Rayer Bazar', ],
        'Uttara': ['Diyabari', 'Dhour', 'Uttara', 'Uttara East', 'Uttara West', ],
        'Hatirpool': ['Green Road', 'Kalabagan', 'Elephant Rd', 'ElephantRoad', 'Hatirpool', ],
        'Gabtoli': ['Gabtali', 'Gabtoli', ],
        'Tejgaon': ['Panthapath', 'Tejgaon', 'Tejgaon I/A', 'Rajabazar', 'Railway Colony', 'Nakhalpara', 'Farmgate',
                    'Karwan Bazar', 'Kawran Bazar', ],
        'Hazaribagh': ['Hazaribag', 'Hazaribag ', ],
        'Keraniganj': ['Keraniganj', 'Kadamtali', ],
        'Mugdapara': ['Mugdapara', 'Mugda Para', 'Mugda', ],
        'Khilkhet': ['Khilkhet', 'Joar Sahara', 'Nikunja 1', 'Progoti Sarani', 'Kuril', 'Nikunja', 'Nikunjo', ],
        'Golapbag': ['Maniknagar', ],
        'Motijheel': ['Kamalapur', 'Motijheel', 'North Shahjahanpur', 'Siddeshwari', 'Shiddeshwari', 'Shiddheswari',
                      'Shegunbagicha', 'Shantinagar', 'Shanti Nagar', 'Shagun Bagicha', 'Segun Bagicha',
                      'Purana Paltan',
                      'Paltan', 'Naya Paltan', 'NayaPaltan', 'Kakrail', 'Baily Road', ],
        'New Market': ['New Market', ],
        'Purbachal': ['Purbachal', 'Purbachal New Town', ],
        'Shabujbag': ['Sabujbag', 'North  Nandipara', 'Nandipara', ],
        'Ramna': ['Shahbag ', 'Shahbagh', 'Modhubag', 'Mogbazar', 'Moghbazar', 'Malibagh', 'Malibag', 'Maghbazar',
                  'Ramna',
                  'Eskaton', 'New Eskaton', 'Paribagh', 'Kathal Bagan', 'Bangla Motor', 'Banglamotor', 'Banglamotors',
                  'Kathalbagan', ],
        'Sher-E-Bangla Nagar': ['Sher E Bangla Nagar ', 'Agargoan', 'Agargaon', ],
        'Jatrabari': ['Jatra Bari', 'Jatrabari', 'Gandaria ', ],
        'Sutrapur': ['Sutrapur', 'Tikatuli', 'Wari', 'Gulistan', ],
        'Turag': ['Turag'],
        'Keranigonj': ['Keranigonj'],
        'Arapur': ['Arapur'],
        'Sadar': ['Sadar']
    }

    # finding zone name according the input locality. If it finds match then, it returns the zone name
    for zone, localities in zones.items():
        for locality in localities:
            if locality_name == locality:
                return zone

    # if it finds none, then it returns an emtpy string.
    return ""
