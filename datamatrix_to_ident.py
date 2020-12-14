#!/usr/bin/env python3
'''
Convert scanned datamatrix to indent.txt file used for hardware identity
'''

import sys
if sys.version_info[0] < 3:
    print ("**** Must use python3 ***")
    raise "Must be using Python 3!"

import time
import re
import subprocess

OUTPUT = "identity_command"

def find_object(obj, indata, length_of_object):
    search_result = re.search(obj, indata)
    if search_result:
        return (indata[search_result.end() + 1 : search_result.end() + length_of_object + 1])
    else:
        return 0

def identity(prod_label):
    identitydictionary = {
      "obj_prefix": "0",
      "obj_class": "0",
      "obj_family": "0",
      "obj_number": "0",
      "obj_suffix": "0",
      "rev_major": "0",
      "rev_minor": "0",
      "rev_preliminary": "0",
      "serial_number": "0",
      "r_state": "0"
    }

    prod_label = prod_label.replace(" ", "/") # "00/5000100207/0PC1 1837337310 000025"
    split_prod_label = re.split(r'/', prod_label)

    identitydictionary["obj_prefix"]    = int(split_prod_label[0])
    identitydictionary["obj_class"]     = int(split_prod_label[1][0:3])
    identitydictionary["obj_family"]    = (split_prod_label[1][3:5])
    identitydictionary["obj_number"]    = int(split_prod_label[1][5:])
    identitydictionary["obj_suffix"]    = int(split_prod_label[2][0:1])
    identitydictionary["r_state"]       = split_prod_label[2][1:]
    identitydictionary["serial_number"] = int(split_prod_label[4])

    product_string = "{}:{} {} {} {}".format(identitydictionary["obj_class"], identitydictionary["obj_family"], identitydictionary["obj_number"], identitydictionary["r_state"], identitydictionary["serial_number"])
    rv_bytes = subprocess.check_output("echo " + product_string + " | perl ident.pl", shell=True)
    rv_string = "".join(map(chr, rv_bytes))

    identitydictionary["obj_class"]       = int(find_object('obj_class:', rv_string, 3))
    identitydictionary["obj_family"]      = int(find_object('obj_family:', rv_string, 1))
    identitydictionary["obj_number"]      = int(find_object('obj_number:', rv_string, 3))
    identitydictionary["rev_major"]       = int(find_object('rev_major:', rv_string, 1))
    identitydictionary["rev_minor"]       = int(find_object('rev_minor:', rv_string, 1))
    identitydictionary["rev_preliminary"] = int(find_object('rev_preliminary:', rv_string, 1))

    # print(identitydictionary)

    return identitydictionary

def convert_scanned(scanned, output_type=0):
    identitydictionary = identity(scanned)

    filename = "SCF-{}_{}_{}_{}_{}.ident.txt".format(identitydictionary["obj_class"],
                                                     str(identitydictionary["obj_family"]).zfill(2),
                                                     identitydictionary["obj_number"],
                                                     identitydictionary["r_state"],
                                                     identitydictionary["serial_number"])

    if output_type == 0:
        format_string = "identity {{\"obj_prefix\":{},\"obj_class\":{},\"obj_family\":{},\"obj_number\":{},\"obj_suffix\":{},\"rev_major\":{},\"rev_minor\":{},\"rev_preliminary\":{},\"serial_number\":{}}}"
        return (format_string.format(identitydictionary["obj_prefix"],
                                   identitydictionary["obj_class"],
                                   identitydictionary["obj_family"],
                                   identitydictionary["obj_number"],
                                   identitydictionary["obj_suffix"],
                                   identitydictionary["rev_major"],
                                   identitydictionary["rev_minor"],
                                   identitydictionary["rev_preliminary"],
                                   identitydictionary["serial_number"]))

    if output_type == 1:
        format_string = "{}_{}_{}_{}_{}_{}_{}"
        return (format_string.format(identitydictionary["obj_prefix"],
                                   identitydictionary["obj_class"],
                                   identitydictionary["obj_family"],
                                   identitydictionary["obj_number"],
                                   identitydictionary["obj_suffix"],
                                   identitydictionary["r_state"],
                                   identitydictionary["serial_number"]))

    original_stdout = sys.stdout
    if output_type == 2:
        with open(filename, 'w') as f:
            sys.stdout = f # Change the standard output to the file we created.
            print('obj_class: {}'.format(identitydictionary["obj_class"]))
            print('obj_family: {}'.format(identitydictionary["obj_family"]))
            print('obj_number: {}'.format(identitydictionary["obj_number"]))
            print('rev_major: {}'.format(identitydictionary["rev_major"]))
            print('rev_preliminary: {}'.format(identitydictionary["rev_preliminary"]))
            print('serial_number: {}'.format(identitydictionary["serial_number"]))
            sys.stdout = original_stdout # Reset the standard output to its original value

        sys.stdout = original_stdout
        return filename

    sys.stdout = original_stdout
    return NULL
