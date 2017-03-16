#!flask/bin/python

from fdfgen import forge_fdf
import os
import sys
import fdfgen
import subprocess
from subprocess import check_output
from re import match
import re
import database
from database import *


def write_values(fields):

	prefix = fields["F[0].Page_8[0].PreferredEmailAddress[0]"]

	fdf = forge_fdf("", fields, [],[],[])
	fdf_file = open( prefix + "_data.fdf", "wb")
	fdf_file.write(fdf)
	fdf_file.close()
	
	os.system("pdftk VBA-21-526EZ-ARE.pdf cat output unsigned_VBA-21-526EZ-ARE.pdf")

	pdftk_cmd = "pdftk unsigned_VBA-21-526EZ-ARE.pdf fill_form " + prefix + "_data.fdf output static/" + prefix + "_VBA-21-526EZ-ARE.pdf"
	print(pdftk_cmd)
	os.system(pdftk_cmd)

def get_fields(pdf_file):
    '''
    Use pdftk to get a pdf's fields as a string, parse the string
    and return the fields as a dictionary, with field names as keys
    and field values as values.
    '''
    fields = {}
    call = ['pdftk', pdf_file, 'dump_data_fields']
    try:
        data_string = check_output(call).decode('utf8')
    except FileNotFoundError:
        raise PdftkNotInstalledError('Could not locate PDFtk installation')
    data_list = data_string.split('\r\n')
    if len(data_list) == 1:
        data_list = data_string.split('\n')
    for line in data_list:
        if line:
            re_object = match(r'(\w+): (.+)', line)
            if re_object is not None:
                if re_object.group(1) == 'FieldName':
                    key = re_object.group(2)
                    fields[key] = ''
                elif re_object.group(1) == 'FieldValue':
                    fields[key] = re_object.group(2)
    return fields

def select_veteran(email):
	veteran = veterans.get_veteran(email)
	return veteran

def build_fields(veteran):
	fields = get_fields("VBA-21-526EZ-ARE.pdf")

	fields["F[0].Page_8[0].PreferredEmailAddress[0]"] = veteran.email
	fields["F[0].Page_8[0].CurrentMailingAddress_NumberAndStreet[0]"] = veteran.address_1
	fields["F[0].Page_8[0].CurrentMailingAddress_ApartmentOrUnitNumber[0]"] = veteran.address_2
	fields["F[0].Page_8[0].CurrentMailingAddress_City[0]"] = veteran.city 
	fields["F[0].Page_8[0].CurrentMailingAddress_StateOrProvince[0]"] = veteran.state 
	fields["F[0].Page_8[0].CurrentMailingAddress_Country[0]"] = "US"
	fields["F[0].Page_8[0].CurrentMailingAddress_ZIPOrPostalCode_FirstFiveNumbers[0]"] = veteran.zip_code

	fields["F[0].Page_8[0].VeteransFirstName[0]"] = veteran.first_name
	fields["F[0].Page_8[0].VeteransLastName[0]"] = veteran.last_name


	if "Army" in veteran.branch:
		fields["F[0].Page_8[0].Army[0]"] = 1
	if "Marine" in veteran.branch:
		fields["F[0].Page_8[0].MarineCorps[0]"] = 1
	if "Navy" in veteran.branch:
		fields["F[0].Page_8[0].Navy[0]"] = 1
	if "Coast" in veteran.branch:
		fields["F[0].Page_8[0].CoastGuard[0]"] = 1
	if "Air" in veteran.branch:
		fields["F[0].Page_8[0].AirForce[0]"] = 1 

	if "Reserve" in veteran.branch:
		fields["F[0].Page_8[0].Reserve[0]"] = 1
		fields["F[0].Page_10[0].CheckBoxYes[3]"] = 1
		fields["F[0].Page_10[0].Component[0]"] = 1
	if "National" in veteran.branch:
		fields["F[0].Page_8[0].NationalGuard[0]"] = 1
		fields["F[0].Page_10[0].CheckBoxYes[3]"] = 1
		fields["F[0].Page_10[0].Component[1]"] = 1

	if veteran.injuries == None:
		veteran.injuries = ""

	injuries_str = str(veteran.injuries)
	injuries = injuries_str.split(',')

	if veteran.mental_h_issues == None:
		vetern.mental_h_issues = ""
	mental_h_issues_str = str(veteran.mental_h_issues)
	mental_h_issues = mental_h_issues_str.split(',')

	disabilities = injuries + mental_h_issues

	for index, disability in enumerate(disabilities):
		if index + 1 <= 20:
			fields["F[0].Page_9[0].DisabilityYouAreClaiming" + str(index+1) + "[0]"] = disability

	if veteran.combat_zone == True:
		fields["F[0].Page_10[0].CheckBoxYes[2]"] = 1

	return fields

def execute(veteran):
	fields = build_fields(veteran)
	write_values(fields)