import random



USER_CREDENTIALS_CHOICES = {
    'team24@techwise.edu': 'team24_techwiseUSA',
    'mark.cuban@havard.edu':"the_mavericks",
    'ladygaga@fashion.show':'telephone_hit_song',
    'jayz@nine-ninety-nine':'im_not_black_im_oj',
    'p3t3r@google.com':'just_an_undergrad_student',
    'emailaddress@yahoo.com':'yahoo_rocks',
    'sgriffin@techwise.edu': 'changing_lives_at_techiwise',
    'president@us.army': 'eagle_one_has_landed'
}

class Packet:
    global USER_CREDENTIALS_CHOICES
    def __init__(self, id_number):
        self.setter = random.randint(0,len(USER_CREDENTIALS_CHOICES)*2)
        self.Raw = self.__initialize_raw(self.setter)
        self.id = id_number

    def load(self):
        return self.Raw

    def has_layer(self):
        return self.Raw is not None

    def __initialize_raw(self, number):
        global USER_CREDENTIALS_CHOICES
        obj = {}
        if number in range(len(USER_CREDENTIALS_CHOICES)):
            key, val = list(USER_CREDENTIALS_CHOICES.items())[number]
            obj[key] = val
        else:
            obj["encypted_field_XXXXXXXXX"] = 'encrypted_data_XXXXXXXXXXXX'
        return obj
def get_packets(target):
    packets = list()
    for num in range(target):
        packets.append(Packet(num))
    return packets