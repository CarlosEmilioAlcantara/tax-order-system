import os

def create_directory(license_no, last_name):
    parent = './receipts/'
    directory = f'{parent}{license_no}_{last_name}/'

    if not os.path.exists(parent):
        try:
            os.mkdir(parent)
        except OSError as e:
            print(e)

    if not os.path.exists(directory):
        try:
            os.mkdir(directory)
        except OSError as e:
            print(e)
