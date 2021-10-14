
# data types used
class FieldTypes:
    string = 1
    string_list = 2
    iso_date_string = 3
    long_string = 4
    decimal = 5
    integer = 6
    boolean = 7

class Size:
    label_frame_width = 800
    label_frame_height = 150

    button_width = 9
    button_height = 1

    listbox_width = 70
    listbox_height = 10

    # hd sizes
    hd_frame_width = 1280
    hd_frame_height = 720

    # textbox frame sizes
    txt_box_width = 100
    txt_box_height = 10

class DataTypes:
    likert_6 = ['I need a lot\nof additional\nknowledge about the topic',
                'I need some\nadditional knowledge\nabout the topic',
                'I need a little\nadditional knowledge\nabout the topic',
                'I have some\nknowledge about\nthe topic',
                'I have good\nknowledge about\nthe topic',
                'I have strong\nknowledge about\nthe topic']

    likert_6_score = {'I need a lot of additional knowledge about the topic' : 1,
                    'I need some additional knowledge about the topic' : 2,
                    'I need a little additional knowledge about the topic' : 3,
                    'I have some knowledge about the topic' : 4,
                    'I have good knowledge about the topic' : 5,
                    'I have strong knowledge about the topic' : 6}

    likert_7 = ['strongly\ndisagree',
                'disagree',
                'somewhat\ndisagree',
                'neither agree\nor disagree',
                'somewhat\nagree',
                'agree',
                'strongly\nagree']

    likert_7_score = {'strongly disagree' : 1,
                    'disagree' : 2,
                    'somewhat disagree' : 3,
                    'neither agree or disagree' : 4,
                    'somewhat agree' : 5,
                    'agree' : 6,
                    'strongly agree' : 7}







