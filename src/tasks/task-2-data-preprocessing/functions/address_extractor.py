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
    cities = ['Barishal', 'Bhairab', 'Bogra', 'Bogura', 'Brahmanbaria', 'Chandpur', 'Chattogram', 'Chittagong',
              'Chowmuhani', 'Chuadanga', 'Comilla', 'Coxs Bazar', 'Cumilla', 'Cumilla Sadar Dakshin', 'Dhaka',
              'Dinajpur', 'Faridpur', 'Feni', 'Gazipur', 'Jamalpur', 'Jashore', 'Jhenaidah', 'Khulna', 'Kishoreganj',
              'Kushtia', 'Maijdee', 'Mymensingh', 'Naogaon', 'Narayanganj', 'Narayanganj City', 'Narayangonj',
              'Narsingdi', 'Nawabganj', 'Pabna', 'Rajshahi', 'Rangpur', 'Saidpur', 'Satkhira', 'Savar', 'Siddhirganj',
              'Sirajganj', 'Sreepur', 'Sylhet', 'Tangail', 'Tarabo', 'Tongi']

    try:

        # if it finds match with the input, it returns true.
        cities.index(name)
        return True

    except:

        # if it doesn't find any match with the input, it returns false.
        return False


def get_area_name(name):
    # a list containing different areas of Bangladesh
    areas = ['11 No. South Kattali Ward', '15 No. Bagmoniram Ward', '16 No. Chawk Bazaar Ward',
             '22 No. Enayet Bazaar Ward', '29 No. West Madarbari Ward', '30 No. East Madarbari Ward',
             '31 No. Alkoron Ward', '32 No. Andarkilla Ward', '33 No. Firingee Bazaar Ward', '36 Goshail Danga Ward',
             '4 No Chandgaon Ward', '7 No. West Sholoshohor Ward', '9 No. North Pahartali Ward', 'Adabor',
             'Aftab Nagar', 'Aftabnagar', 'Agargaon', 'Agrabad', 'Airport', 'Akhaura', 'Akkelpur', 'Alamdanga',
             'Ambarkhana', 'Araihazar', 'Ashkona', 'Ashulia', 'Azimpur', 'Azompur', 'Badarganj', 'Badda', 'Bagerhat',
             'Bagerhat Sadar', 'Bagha', 'Bajitpur', 'Bakalia', 'Banani', 'Banani Dohs', 'Banashree', 'Banasree',
             'Bandar', 'Bandarban', 'Bandarban Sadar', 'Banglamotor', 'Banglamotors', 'Bangshal', 'Banshkhali',
             'Baraigram', 'Barguna', 'Barguna Sadar', 'Baridhara', 'Baridhara Dohs', 'Barishal City', 'Barlekha',
             'Barura', 'Basabo', 'Bashabo', 'Bashundhara', 'Bashundhara R-A', 'Bashundhara R/A', 'Bashundhara RA',
             'Bashundhara Riverview', 'Basila', 'Basurhat', 'Bayazid', 'Beani Bazar', 'Belabo', 'Belkuchi', 'Benapole',
             'Bera', 'Bhairab', 'Bhaluka', 'Bhandaria', 'Bhanga', 'Bhangura', 'Bhashantek ', 'Bheramara', 'Bhola',
             'Bhola Sadar', 'Bhuapur', 'Birampur', 'Birganj', 'Boalkhali', 'Boalmari', 'Bogura Sadar', 'Bosila',
             'Botiaghata', 'Brahmanbaria Sadar', 'Cantonment', 'Chack Bazar', 'Chak Bazar', 'Chakaria', 'Chandanaish',
             'Chandanpur', 'Chandgaon', 'Chandina', 'Chandpur', 'Chandpur Sadar', 'Chandra', 'Chapainawabganj Sadar',
             'Char Fasson', 'Charghat', 'Chatkhil', 'Chattogram City', 'Chauddagram', 'Chaugachha', 'Chaumohoni',
             'Chawkbazar', 'Chhagalnaiya', 'Chhatak', 'Chhengarchar', 'Chuadanga', 'Chunarughat', 'Comilla Cantonment',
             'Cornelhat', "Cox's Bazar Sadar", 'Coxs Bazar', 'Cumilla City', 'DOHS Banani', 'DOHS Baridhara',
             'DOHS Mirpur', 'DOHS Mohakhali', 'Daganbhuiyan', 'Dakshin Khan', 'Dakshinsurma', 'Darshana', 'Daskhinkhan',
             'Daudkandi', 'Debidwar', 'Demra', 'Derai', 'Dewanganj', 'Dhamrai', 'Dhanbari', 'Dhanmondi', 'Dhour',
             'Digholia', 'Dinajpur Sadar', 'Diyabari', 'Dohar', 'Dohar ', 'Double Mooring', 'Dumni', 'Dupchanchia',
             'Durgapur', 'East Nasirabad', 'East Rampura', 'Eskaton', 'Fakirhat', 'Faridganj', 'Faridpur',
             'Faridpur Sadar', 'Farmgate', 'Fatulla', 'Fenchuganj', 'Feni', 'Feni Sadar', 'Firojshah Colony',
             'Fulbaria', 'Gabtali', 'Gaffargaon', 'Gaibandha', 'Gaibandha Sadar', 'Gajaria', 'Galachipa', 'Gandaria ',
             'Gangni', 'Gaurnadi', 'Gazipur Sadar', 'Gazipur Sadar Upazila', 'Ghatail', 'Ghoraghat', 'Ghorashal',
             'Goalunda Ghat', 'Gobindaganj', 'Godagari', 'Gohail Road', 'Golapganj', 'Gollamari', 'Gopalganj',
             'Gopalganj Sadar', 'Gopalpur', 'Goran', 'Gouripur', 'Green Road', 'Gulistan', 'Gulshan', 'Gulshan 01',
             'Gulshan 02', 'Gulshan 1', 'Gulshan 2', 'Gurudaspur', 'Habiganj', 'Habiganj Sadar', 'Hajiganj', 'Hakimpur',
             'Halishahar', 'Haragacha', 'Harinakundu', 'Hathazari', 'Hatirpool', 'Hatiya', 'Hazaribag', 'Hazaribag ',
             'Hemayetpur', 'Homna', 'Hossainpur', 'Ibrahimpur', 'Ishwardi', 'Ishwarganj', 'Islampur', 'Jagannathpur',
             'Jaintiapur', 'Jaipurhat', 'Jajira', 'Jalalabad Housing Society', 'Jaldhaka', 'Jamal Khan',
             'Jamalpur Sadar', 'Jashore Sadar', 'Jatra Bari', 'Jatrabari', 'Jhalakathi Sadar', 'Jhalakati', 'Jhenaidah',
             'Jhenaidah Sadar', 'Jhigatala', 'Jhikargacha', 'Jibannagar', 'Joar Sahara', 'Joypurhat Sadar', 'Kachua',
             'Kachukhet', 'Kadamtali', 'Kafrul', 'Kakrail', 'Kalabagan', 'Kalachandpur', 'Kalapara', 'Kalaroa', 'Kalia',
             'Kaliakair', 'Kaliganj', 'Kalihati', 'Kalkini', 'Kallaynpur', 'Kallyanpur', 'Kamalapur', 'Kamarkhand',
             'Kamrangir Char', 'Kamrangirchar', 'Kanaighat', 'Kanchan', 'Karimganj', 'Karnafuli', 'Karwan Bazar',
             'Kasba', 'Katakhali', 'Kathalbagan', 'Katiadi', 'Kawran Bazar', 'Kazipara', 'Kazir Dewri', 'Kendua',
             'Keraniganj', 'Keshabpur', 'Kesharhat', 'Khagrachhari', 'Khan Jahan Ali', 'Khilgaon', 'Khilkhet',
             'Khulna City', 'Khulshi', 'Kishoreganj', 'Kotchandpur', 'Kotwali', 'Kulaura', 'Kuliarchar', 'Kumarkhali',
             'Kurigram', 'Kuril', 'Kushtia', 'Kushtia Sadar', 'Laksham', 'Lakshmipur', 'Lakshmipur Sadar',
             'Lal Khan Bazaar', 'Lalbag', 'Lalbagh', 'Lalmatia', 'Lalmohan', 'Lalmonirhat', 'Lalpur', 'Lama',
             'Lohagara', 'Madarganj', 'Madaripur', 'Madaripur Sadar', 'Madhabdi', 'Madhabpur', 'Madhupur', 'Maghbazar',
             'Magura', 'Magura Sadar', 'Maheshkhali', 'Maheshpur', 'Malibag', 'Malibagh', 'Manikganj',
             'Manikganj Sadar', 'Maniknagar', 'Manirampur', 'Matiranga', 'Matlab', 'Matuail', 'Maulvi Bazar',
             'Mehendiganj', 'Meherpur', 'Melandaha', 'Mirkadim', 'Mirpur', 'Mirpur 1', 'Mirpur 10', 'Mirpur 11',
             'Mirpur 12', 'Mirpur 13', 'Mirpur 14', 'Mirpur 2', 'Mirpur 6', 'Mirpur Dohs', 'Mirsharai', 'Mirzapur',
             'Mithapukur', 'Modhubag', 'Moghbazar', 'Mohakhali', 'Mohakhali Dohs', 'Mohammadpur', 'Mohammadpur ',
             'Mohanganj', 'Mongla', 'Monipur10 No. North Kattali Ward', 'Morrelganj', 'Motijheel', 'Moulvibazar Sadar',
             'Mugda', 'Mugda Para', 'Mugdapara', 'Muksudpur', 'Muktagacha', 'Muktagachha', 'Muladi', 'Mundumala',
             'Munshiganj', 'Munshiganj Sadar', 'Muradpur', 'Mymensingh City', 'Nabiganj', 'Nabinagar', 'Nadda',
             'Nageshwari', 'Nakhalpara', 'Nakla', 'Nalchiti', 'Nalitabari', 'Nandail', 'Nandipara', 'Nangalkot',
             'Naogaon Sadar', 'Naohata', 'Narail', 'Narayanganj', 'Narayangonj Sadar', 'Naria', 'Narinda', 'Narsingdi',
             'Narsingdi Sadar', 'Nasirbad', 'Natore', 'Natore Sadar', 'Nazipur', 'Netrakona', 'Netrokona Sadar',
             'New Market', 'Niketan', 'Niketon', 'Nikunja', 'Nikunjo', 'Nilphamari', 'Nilphamari Sadar', 'Noakhali',
             'Noakhali Sadar', 'Noapara', 'North  Nandipara', 'North Shahjahanpur', 'Pabna Sadar', 'Pahartali',
             'Pakundia', 'Pallabi', 'Pallabi ', 'Paltan', 'Panchagarh', 'Panchagarh Sadar', 'Panchbibi', 'Panchlaish',
             'Pangsha', 'Parbatipur', 'Paribagh', 'Parshuram', 'Patenga', 'Patgram', 'Patiya', 'Patuakhali',
             'Patuakhali Sadar', 'Phulbari', 'Phulpur', 'Pirerbag', 'Pirganj', 'Pirojpur', 'Puran Bogra',
             'Purana Paltan', 'Purbachal', 'Puthia', 'Rahanpur', 'Railway Colony', 'Raipur', 'Raipura', 'Rajasthali',
             'Rajbari', 'Rajbari Sadar', 'Rajoir', 'Rajshahi City', 'Ramganj', 'Ramgarh', 'Ramgati', 'Ramna', 'Rampura',
             'Rangamati', 'Rangpur City', 'Rangunia', 'Ranisankail', 'Raozan', 'Riaj Uddin Bazar', 'Rupganj',
             'Rupnagar', 'Rupsha', 'Sabujbag', 'Sadar', 'Sagorika Bscic Industrial Area', 'Saidpur', 'Sakhipur',
             'Sandwip', 'Santahar', 'Santhia', 'Sarishabari', 'Satkania', 'Satkhira', 'Satkhira Sadar', 'Savar',
             'Senbagh', 'Senpara Porbota', 'Setabganj', 'Shah Ali', 'Shahbag ', 'Shahbagh', 'Shahjadpur',
             'Shahjahanpur', 'Shahporan', 'Shahrasti', 'Shailkupa', 'Shaistaganj', 'Shajahanpur', 'Shantinagar',
             'Shariatpur', 'Shariatpur Sadar', 'Shegunbagicha', 'Sher E Bangla Nagar ', 'Sherpur', 'Sherpur Sadar',
             'Shewrapara', 'Shibchar', 'Shibganj', 'Shibpur', 'Shiddheswari', 'Shiddhirganj', 'Sholokbahar', 'Shyamoli',
             'Shyampur', 'Shyampur ', 'Siddeshwari', 'Singair', 'Singiar', 'Singra', 'Sirajganj', 'Sirajganj Sadar',
             'Sitakunda', 'Sonadanga', 'Sonagazi', 'Sonaimuri', 'Sonargaon', 'Sonatala', 'South Banasree', 'Sreebardi',
             'Sreemangal', 'Sreepur', 'Sujanagar', 'Sunamganj', 'Sunamganj Sadar', 'Sutrapur', 'Swarupkati',
             'Sylhet City', 'Taltali', 'Taltola', 'Tangail Sadar', 'Tanore', 'Tarabo', 'Tarakanda', 'Tejgaon',
             'Tejgaon I/A', 'Teknaf', 'Tetulia', 'Thakurgaon', 'Thakurgaon Sadar', 'Tikatuli', 'Tongi', 'Trishal',
             'Turag', 'Ulipur', 'Ullahpara', 'Ullapara', 'Uttar Khan', 'Uttar Lalkhan', 'Uttara', 'Uttara East',
             'Uttara West', 'Uttarkhan', 'Vatara', 'Vatara ', 'Wari', 'West Dhanmondi', 'West Khulshi', 'West Rampura',
             'Zafrabad', 'Zindabazar', 'Madani Avenue', 'Rayer Bazar', 'Panthapath', 'New Eskaton', 'Kallayanpur',
             'MohakhaliDOHS', 'MirpurDOHS', 'Choukbazar', 'Zigatola', 'Basundhara', 'DakhinKhan', 'BananiDOHS',
             'ElephantRoad', 'Kalyanpur', 'NayaPaltan', 'Rajabazar', 'Mogbazar', 'Shagun Bagicha', 'Shiddeshwari',
             'Gabtoli', 'Shanti Nagar', 'Bangla Motor', 'Gulshan-1', 'Gulshan-2', 'Baridhara Diplomatic Zone',
             'Bashundhara R /A', 'Arapur', 'Golmari']

    try:

        # if it finds match with the input, it returns true.
        areas.index(name)
        return True

    except:

        # if it doesn't find any match with the input, it returns false.
        return False
