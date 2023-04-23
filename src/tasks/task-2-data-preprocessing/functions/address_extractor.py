"""
 The functions below are developed by @Shariar Hossain Omee

 get_detailed_address() :
    - Take a full comma separated address as input
    - Split the address into City, Area, Address
    - Return a dictionary containing City, Area (a.k.a. "Locality"), Address as keys

This function splits input address according to the commas, then it checks each separated string with the values in
the arrays which we pre-defined in the function. It will return one area name under the 'Area' key and one city name
under the 'City' key, if it could match them with the pre-defined areas and cities in the function , the rest of the
string or address will be under the 'Address' key.

For example,
    Input --> "Block M, South Banasree Project, Banasree, Dhaka"
    Output --> {"city": "Dhaka", "area": "Banasree", "address": "Block M, South Banasree Project"}

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
        address_dict = {"city": "", "area": "", "address": ""}

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
                address_dict["area"] = i.strip().replace('.', '')
                # removing the matched name from the splitted address list.
                splitted_address.remove(i)

        # joining the rest of the input and assigning it under the "address" key.
        address_dict["address"] = ','.join(splitted_address)

        # returning the output dictionary
        return address_dict

    except:

        # if any exception occurs, it assigns the whole input under the "address" key and return the dictionary
        return {"city": "", "area": "", "address": address}


def get_city_name(name):

    # a list containing different cities of Bangladesh
    cities = ['Dhaka', 'Chattogram', 'Narayanganj City', 'Gazipur', 'Sylhet', 'Barishal', 'Bhairab', 'Bogura',
              'Brahmanbaria', 'Chandpur', 'Chittagong', 'Chowmuhani', 'Chuadanga', 'Coxs Bazar',
              'Cumilla', 'Cumilla Sadar Dakshin', 'Dinajpur', 'Faridpur', 'Feni', 'Gazipur', 'Jamalpur',
              'Jashore', 'Jhenaidah', 'Khulna', 'Kishoreganj', 'Kushtia', 'Maijdee', 'Mymensingh',
              'Naogaon', 'Narayanganj', 'Narsingdi', 'Nawabganj', 'Pabna', 'Rajshahi', 'Rangpur', 'Saidpur', 'Satkhira',
              'Savar', 'Siddhirganj', 'Sirajganj', 'Sreepur', 'Tangail', 'Tarabo', 'Tongi']

    try:

        # if it finds match with the input, it returns true.
        cities.index(name)
        return True

    except:

        # if it doesn't find any match with the input, it returns false.
        return False


def get_area_name(name):

    # a list containing different areas of Bangladesh
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
             'West Rampura', 'Zafrabad', 'Zindabazar', 'Akhaura', 'Akkelpur', 'Alamdanga', 'Badarganj', 'Bagerhat',
             'Bagha', 'Bajitpur', 'Bandarban', 'Banshkhali', 'Baraigram', 'Barguna', 'Barlekha', 'Barura', 'Basurhat',
             'Beani Bazar', 'Belkuchi', 'Benapole', 'Bera', 'Bhairab', 'Bhaluka', 'Bhanga', 'Bhangura', 'Bheramara',
             'Bhola', 'Bhuapur', 'Birampur', 'Birganj', 'Boalmari', 'Chakaria', 'Chandanaish', 'Chandina', 'Chandpur',
             'Char Fasson', 'Charghat', 'Chatkhil', 'Chauddagram', 'Chaugachha', 'Chaumohoni', 'Chhagalnaiya',
             'Chhatak', 'Chhengarchar', 'Chuadanga', 'Chunarughat', 'Coxs Bazar', 'Daganbhuiyan', 'Darshana',
             'Daudkandi', 'Debidwar', 'Derai', 'Dewanganj', 'Dhamrai', 'Dhanbari', 'Dohar', 'Dupchanchia', 'Durgapur',
             'Durgapur', 'Faridganj', 'Faridpur', 'Feni', 'Fulbaria', 'Gabtali', 'Gaffargaon', 'Gaibandha', 'Galachipa',
             'Gangni', 'Gaurnadi', 'Ghatail', 'Ghoraghat', 'Ghorashal', 'Goalunda Ghat', 'Gobindaganj', 'Godagari',
             'Golapganj', 'Gopalganj', 'Gopalpur', 'Gopalpur', 'Gouripur', 'Gurudaspur', 'Habiganj', 'Hajiganj',
             'Hakimpur', 'Haragacha', 'Harinakundu', 'Hatiya', 'Homna', 'Hossainpur', 'Ishwardi', 'Ishwarganj',
             'Islampur', 'Jagannathpur', 'Jaipurhat', 'Jajira', 'Jaldhaka', 'Jhalakati', 'Jhenaidah', 'Jhikargacha',
             'Jibannagar', 'Kachua', 'Kalaroa', 'Kalia', 'Kaliakair', 'Kaliganj', 'Kaliganj', 'Kalihati', 'Kalkini',
             'Kanaighat', 'Kanchan', 'Karimganj', 'Kasba', 'Katakhali', 'Katiadi', 'Kendua', 'Keshabpur', 'Kesharhat',
             'Khagrachhari', 'Kishoreganj', 'Kotchandpur', 'Kulaura', 'Kuliarchar', 'Kumarkhali', 'Kurigram', 'Kushtia',
             'Laksham', 'Lakshmipur', 'Lalmohan', 'Lalmonirhat', 'Lama', 'Lohagara', 'Madarganj', 'Madaripur',
             'Madhabdi', 'Madhabpur', 'Madhupur', 'Magura', 'Maheshkhali', 'Maheshpur', 'Manikganj', 'Manirampur',
             'Matiranga', 'Matlab', 'Maulvi Bazar', 'Mehendiganj', 'Meherpur', 'Melandaha', 'Mirkadim', 'Mirpur',
             'Mirzapur', 'Mohanganj', 'Mongla', 'Morrelganj', 'Muksudpur', 'Muktagachha', 'Muladi', 'Mundumala',
             'Munshiganj', 'Nabiganj', 'Nabinagar', 'Nageshwari', 'Nakla', 'Nalchiti', 'Nalitabari', 'Nandail',
             'Nangalkot', 'Naohata', 'Narail', 'Naria', 'Narsingdi', 'Natore', 'Nazipur', 'Netrakona', 'Nilphamari',
             'Noakhali', 'Noapara', 'Pakundia', 'Panchagarh', 'Panchbibi', 'Pangsha', 'Parbatipur', 'Parshuram',
             'Patgram', 'Patiya', 'Patuakhali', 'Phulbari', 'Phulpur', 'Pirganj', 'Pirojpur', 'Puthia', 'Rahanpur',
             'Raipur', 'Raipura', 'Rajbari', 'Ramganj', 'Ramgarh', 'Ramgati', 'Rangamati', 'Rangunia', 'Raozan',
             'Saidpur', 'Sakhipur', 'Sandwip', 'Santahar', 'Santhia', 'Sarishabari', 'Satkania', 'Satkhira', 'Savar',
             'Senbagh', 'Setabganj', 'Shahjadpur', 'Shahrasti', 'Shailkupa', 'Shaistaganj', 'Shariatpur', 'Sherpur',
             'Sherpur', 'Shibchar', 'Shibganj', 'Shibganj', 'Shibpur', 'Singair', 'Singra', 'Sirajganj', 'Sitakunda',
             'Sonagazi', 'Sonaimuri', 'Sonargaon', 'Sonatala', 'Sreebardi', 'Sreemangal', 'Sreepur', 'Sujanagar',
             'Sunamganj', 'Swarupkati', 'Tanore', 'Tarabo', 'Teknaf', 'Thakurgaon', 'Trishal', 'Ulipur', 'Ullahpara']

    try:

        # if it finds match with the input, it returns true.
        areas.index(name)
        return True

    except:

        # if it doesn't find any match with the input, it returns false.
        return False

