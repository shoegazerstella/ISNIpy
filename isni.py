import os
import argparse
import requests
import xmltodict, json, ast

SAVE_DIR = '.'


def searchByISNI(ISNI):

    url = "https://isni.org/isni/%s/about.xml" % (ISNI)
    response = requests.get(url)
    xpars = xmltodict.parse(response.text)
    data = json.dumps(xpars)
    data = ast.literal_eval(data)

    with open(os.path.join(SAVE_DIR, str(ISNI) + '.json'), 'w') as outfile:
        json.dump(data, outfile, indent=4)

def searchByString(searchString):

    url = "http://isni.oclc.org/sru/DB=1.2/?query=pica.nw+%3D+%22"+ str(searchString) +"%22&version=1.1&operation=searchRetrieve&stylesheet=http%3A%2F%2Fisni.oclc.org%2Fsru%2FDB%3D1.2%2F%3Fxsl%3DsearchRetrieveResponse&recordSchema=isni-b&maximumRecords=10&startRecord=1&recordPacking=xml&sortKeys=none&x-info-5-mg-requestGroupings=none"
    response = requests.get(url)
    xpars = xmltodict.parse(response.text)
    data = json.dumps(xpars)
    data = ast.literal_eval(data)

    ISNI_list = []
    for i, elem in enumerate(data['srw:searchRetrieveResponse']['srw:records']['srw:record']):
        ISNIAssigned = elem['srw:recordData']['responseRecord']['ISNIAssigned']['isniUnformatted']
        ISNI_list.append(ISNIAssigned)

    return ISNI_list

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    usage = "python isni.py -i 0000000114448576"
    parser=argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter, description=usage, add_help=False)
    parser.add_argument('-i', '--isni', required=False, default=None)
    parser.add_argument('-s', '--search', required=False, default=None)
    args = parser.parse_args()

    ISNI = args.isni
    searchString = args.search

    if ISNI is None and searchString is None:
        raise Exception('provide a valid ISNI or search string in input.')

    if ISNI is not None:
        searchByISNI(ISNI)
        
    elif searchString is not None:
        ISNI_list = searchByString(searchString)
        print('Found', len(ISNI_list), 'results matching the query:', str(searchString))
        for id_ in ISNI_list:
            print('Searching ISNI:', str(id_))
            searchByISNI(id_)
