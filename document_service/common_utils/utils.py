from .custom_exceptions import Custom_Error
from rest_framework import status
import re


# COUNTRIES_IDOC_MAP -- > country --> '<ID Name>' --> '<Formal Name>'
COUNTRIES_IDOC_MAP = {
        'Argentina': {'driver_license': 'Driver Licence','nic': 'National Identity Document (DNI)','passport': 'Passport'},
        'Australia': {'driver_license': 'Driver Licence','tfn':'Tax File Number (TFN)','passport': 'Passport'},
        'Austria': {'driver_license': 'Driver Licence','nic': 'National Identity Card (CCR ID)','passport': 'Passport'},
        'Belgium': {'driver_license': 'Driver Licence','nic': 'National Register Number (National ID)','passport': 'Passport'},
        'Bosnia': {'driver_license': 'Driver Licence','nic': 'National Identity Card (Citizen Number)','passport': 'Passport'},
        'Brazil': {'cpf':'Cadastro de Pessoas Físicas (CPF)','driver_license': 'Driver Licence','nic': 'National Identity Card','passport': 'Passport','ssc': 'Social Security Card'},
        'Bulgaria': {'driver_license': 'Driver Licence','nic': 'National Identity Card (Civil Number)','passport': 'Passport'},
        'Canada': {'driver_license': 'Driver Licence','sic':'Social Insurance Card','passport': 'Passport'},
        'Chile': {'driver_license': 'Driver Licence','nic': 'National Identity Card (RUN / RUT)','passport': 'Passport'},
        'China': {'driver_license': 'Driver Licence','nic': 'National Identity Card (ID Number)','passport': 'Passport'},
        'Croatia': {'driver_license': 'Driver Licence','nic': 'National Identity Card (Personal Identification Number - OIB)','passport': 'Passport'},
        'Czech Republic': {'birth_number':'Birth Number','driver_license': 'Driver Licence','nic': 'National Identity Card (Citizen Identification Card Number)','passport': 'Passport'},
        'Denmark': {'cvr_number':'CVR Number','driver_license': 'Driver Licence','nic': 'National Identity Card (Personal Identification - CPR Number)','passport': 'Passport','vat_number':'VAT Registration Number'},
        'Estonia': {'driver_license': 'Driver Licence','nic': 'National Identity Card (Personal Identification Code / Number)','passport': 'Passport'},
        'Finland': {'driver_license': 'Driver Licence','hetu':'Personal Identification Number (HETU)','nic': 'National Identity Card','passport': 'Passport'},
        'France': {'driver_license': 'Driver Licence','nic': 'National Identity Card / Number','passport': 'Passport'},
        'Herzegovina': {'driver_license': 'Driver Licence','nic': 'National Identity Card (Citizen Number)','passport': 'Passport'},
        'Iceland': {'driver_license': 'Driver Licence','nic': 'National Identity Card (Kennitala)','passport': 'Passport'},
        'India': {'aadhar': 'AADHAR Card','driver_license': 'Driver Licence','pancard': 'PAN Card','passport': 'Passport','voterid': 'Voter ID'},
        'Indonesia':{'driver_license': 'Driver Licence','nic': 'National Identity Card (National ID)','passport': 'Passport'},
        'Israel': {'driver_license': 'Driver Licence','nic': 'National Identity Card (National ID)','passport': 'Passport'},
        'Italy': {'driver_license': 'Driver Licence','hic':'Health Insurance Card','nic': 'National Identity Card (Fiscal Code Card)','passport': 'Passport'},
        'Latvia': {'driver_license': 'Driver Licence','nic': 'National Identity Card (Personal Code)','passport': 'Passport'},
        'Lithuania': {'driver_license': 'Driver Licence','nic': 'National Identity Card (Personal Code)','passport': 'Passport'},
        'Macedonia': {'driver_license': 'Driver Licence','nic': 'National Identity Card (Citizen Number)','passport': 'Passport'},
        'Malaysia': {'driver_license': 'Driver Licence','nic': 'National Identity Card (National ID)','passport': 'Passport'},
        'Mexico': {'driver_license': 'Driver Licence','nic': 'National Identity Card (CURP) ','passport': 'Passport','ssc': 'Social Security Card'},
        'Moldova': {'driver_license': 'Driver Licence','nic': 'National Identity Card (Personal Code)','passport': 'Passport'},
        'Montenegro': {'driver_license': 'Driver Licence','nic': 'National Identity Card (Citizen Number)','passport': 'Passport'},
        'Netherlands': {'driver_license': 'Driver Licence','nic': 'National Identity Card (Citizen Service / Personal Number)','passport': 'Passport'},
        'New Zealand': {'driver_license': 'Driver Licence','nhi':'National Health Index Number','passport': 'Passport'},
        'Norway': {'driver_license': 'Driver Licence','nic': 'National Identity Card (Birth Number)','passport': 'Passport'},
        'Poland': {'driver_license': 'Driver Licence','nic': 'National Identity Card (Polish National ID Card)','tin':'Tax Identification Number (NIP)','passport': 'Passport','pesel_number':'PESEL Number','regon':'REGON - Identification for Business'},
        'Portugal': {'driver_license': 'Driver Licence','hun':'Health User Number','ic_number':'Civil Identification Number','passport': 'Passport','ssc': 'Social Security Card /  Number','tin':'Tax Identification Number','voterid': 'Voter ID / Number'},
        'Romania': {'driver_license': 'Driver Licence','nic': 'National Identity Card / Personal Numeric Code - CNP','passport': 'Passport'},
        'Serbia': {'driver_license': 'Driver Licence','nic': 'National Identity Card (Citizen Number)','passport': 'Passport'},
        'Singapore': {'driver_license': 'Driver Licence','nic': 'National Identity Card (National ID)','passport': 'Passport'},
        'Slovakia': {'birth_number':'Birth Number','driver_license': 'Driver Licence','nic': 'National Identity Card (Citizen Identification Card Number)','passport': 'Passport'},
        'Slovenia': {'driver_license': 'Driver Licence','nic': 'National Identity Card (Citizen Number)','passport': 'Passport'},
        'South Africa': {'driver_license': 'Driver Licence','nic': 'National Identity Card','passport': 'Passport'},
        'South Korea': {'driver_license': 'Driver Licence','nic': 'National Identity Card (Resident Registration Number)','passport': 'Passport'},
        'Spain': {'driver_license': 'Driver Licence','nic': 'National Identity Card (DNI)','nie': 'NIE','passport': 'Passport'},
        'Sweden': {'driver_license': 'Driver Licence','con': 'Co-Ordination Number','orn':'Organisation Number','passport': 'Passport','nic':'National Identity Card (Personal Identity Number - PIN)'},
        'Switzerland': {'driver_license': 'Driver Licence','passport': 'Passport','ssc': 'Social Security Card'},
        'Turkey': {'driver_license': 'Driver Licence','passport': 'Passport','nic': 'National Identity Card (Turkish Identification Number)'},
        'Ukraine': {'driver_license': 'Driver Licence','passport': 'Passport','nic': 'National Identity Card (Individual Identification Number)'},
        'United Arab Emirates': {'driver_license': 'Driver License','passport':'Passport','nic':'Emirates ID'},
        'United Kingdom': {'nino':'National Insurance Number','nhsn':'National Health Service Number','driver_license': 'Driver Licence','passport': 'Passport','ssc': 'Social Security Card','nic':'National Identity Card (Identity Card)'},
        'USA':{'driver_license': 'Driver Licence','passport': 'Passport','ssc': 'Social Security Card'}
}

# COUNTRIES_IDOC_VALIDATE -- > country --> '<ID Name>' --> '<Regular Expression>'
COUNTRIES_IDOC_VALIDATE = {
        'Argentina': {'driver_license': None,'nic':None,'passport':None},
        'Australia': {'driver_license': None,'tfn':None,'passport':None},
        'Austria': {'driver_license': None,'nic':None,'passport':None},
        'Belgium': {'driver_license': None,'nic':None,'passport':None},
        'Bosnia': {'driver_license': None,'nic':None,'passport':None},
        'Brazil': {'cpf':None,'driver_license': None,'nic':None,'passport':None,'ssc':None},
        'Bulgaria': {'driver_license': None,'nic':None,'passport':None},
        'Canada': {'driver_license': None,'sic':None,'passport':None},
        'Chile': {'driver_license': None,'nic':None,'passport':None},
        'China': {'driver_license': None,'nic':None,'passport':None},
        'Croatia': {'driver_license': None,'nic':None,'passport':None},
        'Czech Republic': {'birth_number':None,'driver_license': None,'nic':None,'passport':None},
        'Denmark': {'cvr_number':None,'driver_license': None,'nic':None,'passport':None,'vat_number':None},
        'Estonia': {'driver_license': None,'nic':None,'passport':None},
        'Finland': {'driver_license': None,'hetu':None,'nic':None,'passport':None},
        'France': {'driver_license': None,'nic':None,'passport':None},
        'Herzegovina': {'driver_license': None,'nic':None,'passport':None},
        'Iceland': {'driver_license': None,'nic':None,'passport':None},
        'India': {'aadhar': '^[0-9]{12}$','driver_license': None,'pancard': '^[A-Z]{5}[0-9]{4}[A-Z]{1}$','passport': None,'voterid': '^[A-Z]{3}[0-9]{7}$'},
        'Indonesia':{'driver_license': None,'nic':None,'passport':None},
        'Israel': {'driver_license': None,'nic': None,'passport':None},
        'Italy': {'driver_license': None,'hic':None,'nic':None,'passport':None},
        'Latvia': {'driver_license': None,'nic': None,'passport':None},
        'Lithuania': {'driver_license': None,'nic': None,'passport':None},
        'Macedonia': {'driver_license': None,'nic': None,'passport':None},
        'Malaysia': {'driver_license': None,'nic': None,'passport':None},
        'Mexico': {'driver_license': None,'nic': None,'passport':None,'ssc':None},
        'Moldova': {'driver_license': None,'nic': None,'passport':None},
        'Montenegro': {'driver_license': None,'nic': None,'passport':None},
        'Netherlands': {'driver_license': None,'nic': None,'passport':None},
        'New Zealand': {'driver_license': None,'nhi':None,'passport':None},
        'Norway': {'driver_license': None,'nic': None,'passport':None},
        'Poland': {'driver_license': None,'nic': None,'tin':None,'passport':None,'pesel_number':None,'regon':None},
        'Portugal': {'driver_license': None,'hun':None,'ic_number':None,'passport':None,'ssc':None,'tin':None,'voterid':None},
        'Romania': {'driver_license': None,'nic': None,'passport':None},
        'Serbia': {'driver_license': None,'nic': None,'passport':None},
        'Singapore': {'driver_license': None,'nic': None,'passport':None},
        'Slovakia': {'birth_number':None,'driver_license': None,'nic':None,'passport':None},
        'Slovenia': {'driver_license': None,'nic': None,'passport':None},
        'South Africa': {'driver_license': None,'nic':None,'passport':None},
        'South Korea': {'driver_license': None,'nic':None,'passport':None},
        'Spain': {'driver_license': None,'nic': None,'nie':None,'passport':None},
        'Sweden': {'driver_license': None,'con': None,'orn':None,'passport':None,'nic':None},
        'Switzerland': {'driver_license': None,'passport':None,'ssc':None},
        'Turkey': {'driver_license': None,'passport':None,'nic':None},
        'Ukraine': {'driver_license': None,'passport':None,'nic':None},
        'United Arab Emirates': {'driver_license': None,'passport':None,'nic':None},
        'United Kingdom': {'nino':None,'nhsn':None,'driver_license': None,'passport':None,'ssc':None,'nic':None},
        'USA':{'driver_license': None,'passport':None,'ssc': None}
}


def doctype_validate(country, doctype, docid):
    
    types = COUNTRIES_IDOC_VALIDATE[country.capitalize()]
    if doctype not in list(types.keys()):
        raise Custom_Error(f'Doctype must be one of the following values {list(types.keys())}', status.HTTP_400_BAD_REQUEST)
    if country.capitalize() == 'India':
        if types[doctype] != None:
            match = re.match(types[doctype], docid)
            if not match:
                raise Custom_Error(f'Invalid {doctype} ID format')
            return True
    return True
    

def con_citz(citizen):
    citz_index = []
    for item in citizen:
        citz_index.append(item['index'])
    return citz_index