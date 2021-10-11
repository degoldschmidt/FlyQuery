import requests
from bs4 import BeautifulSoup
import ast
import pandas as pd
import numpy as np
from IPython.display import display

def fill_in(data, id_col=None, add_columns=[]):
    for col in add_columns:
        data[col] = np.nan
    for i, row in data.iterrows():
        if row[id_col].isnumeric():
            stock_id = int(row[id_col])
        else:
            print('[FlyQuery] WARNING: Not valid stock number.')
        for col in add_columns:
            data.loc[i, col] = get(col, stock_id)
    return data

class FlyBaseStocks(object):
    def __init__(self, list_of_ids):
        self.data = {   'Collection': [],
                        'Collection Type': [],
                        'Species': [],
                        'Stock Number': [],
                        'Link': [],
                        'FlyBase ID': [],
                        'Stock List Description': [],
                        'FlyBase Genotype': [],
                        'State of Stock': [],
                        'Feature': []}
        for el in list_of_ids:
            url = 'http://flybase.org/reports/{}'.format(el)
            page = requests.get(url)
            soup = BeautifulSoup(page.text, 'html.parser')
            ### finding details
            key = soup.find_all('div', class_='col-sm-3 col-sm-height field_label')
            value = soup.find_all('div', class_=['col-sm-9 col-sm-height', 'col-sm-3 col-sm-height'])
            for i, t in enumerate(key):
                for k in self.data.keys():
                    iden = str(t.text).strip()
                    if iden == k:
                        #print(iden, 'found.')
                        self.data[k].append(str(value[i].text))
            self.data['Link'].append('https://bdsc.indiana.edu/Home/Search?presearch={}'.format(int(el.split('FBst')[1])))
        self.data = pd.DataFrame(self.data)

    def __str__(self):
        return str(self.data)

    def display(self):
        display(self.data)

class FlyBaseQuery(object):
    def __init__(self, list_of_ids):
        self.ids = list_of_ids
        self.stocks = FlyBaseStocks([el for el in self.ids if get_short_hand('stocks') in el])

    def __str__(self):
        return str(self.ids)

    def select(self, types):
        if type(types) is str:
            sh = get_short_hand(types)
            return FlyBaseQuery([el for el in self.ids if sh in el])

def get(_type, _val):
    valids = ['genotype', 'shortname']
    if _type not in valids:
        raise IndexError('Could not find requested type. Valid types are {}'.format(valids))
    if _type == 'genotype':
        return get_genotype(_val)
    if _type == 'shortname':
        return get_short_name(_val)

def parse_vdrc_stock(url):
    result = None
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    ### finding genotype
    key = soup.find_all('tr')
    value = soup.find_all('td')
    for i, t in enumerate(key):
        print(t.text)
        if 'FlyBase gene number' in t.text:
            result = str(value[i].text)
    return result

def parse_flybase_stock(url):
    result = None
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    ### finding genotype
    key = soup.find_all('div', class_='col-sm-3 col-sm-height field_label')
    value = soup.find_all('div', class_=['col-sm-9 col-sm-height', 'col-sm-3 col-sm-height'])
    for i, t in enumerate(key):
        if 'Stock List Description' in t.text:
            result = str(value[i].text)
    return result

def get_genotype(stock_number):
    if type(stock_number) is int:
        urlpre = 'http://flybase.org/reports/FBst'
        url = urlpre + '{:07d}'.format(stock_number)
        result = parse_flybase_stock(url)
    elif stock_number.startswith('v'):
        url = 'https://stockcenter.vdrc.at/control/product/~product_id={}'.format(stock_number)
        result = parse_vdrc_stock(url)
    else:
        url = 'http://flybase.org/reports/{}'.format(stock_number)

    if result is None:
        print('[FlyQuery] WARNING: stock number {} not found.'.format(stock_number))
    return result

def get_short_name(stock_number):
    result = None
    if type(stock_number) is int:
        urlpre = 'http://flybase.org/reports/FBst'
        url = urlpre + '{:07d}'.format(stock_number)
    else:
        url = 'http://flybase.org/reports/{}'.format(stock_number)
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    ### finding genotype
    key = soup.find_all('div', class_='col-sm-3 col-sm-height field_label')
    value = soup.find_all('div', class_=['col-sm-9 col-sm-height', 'col-sm-3 col-sm-height'])
    for i, t in enumerate(key):
        if 'Stock List Description' in t.text:
            if 'P{y[+t7.7] w[+mC]=GMR' in value[i].text and 'GAL4' in value[i].text: ### Gen1 GAL4s
                result = str(value[i].text).split('GMR')[1].split('}')[0]
            elif 'P{y[+t7.7] w[+mC]=R' in value[i].text in value[i].text: ### Split Halves AD/DBDs
                result = str(value[i].text).split('=R')[1].split('}')[0].replace('GAL4.DBD', 'DBD').replace('p65.AD', 'AD')
            elif 'P{y[+t7.7] w[+mC]=VT' in value[i].text in value[i].text: ### VT GAL4s
                result = str(value[i].text).split('[+mC]=')[1].split('}')[0].replace('GAL4.DBD', 'DBD').replace('p65.AD', 'AD')
            else:
                print('[FlyQuery] WARNING: Cannot query shorthand for {}.'.format(value[i].text))
    if result is None:
        print('[FlyQuery] WARNING: stock number {} not found.'.format(stock_number))
    return result

def get_short_hand(val):
    if not val.endswith('s'):
        val += 's'
    dictionary = {  'alleles': 'al',
                    'genes': 'gn',
                    'stocks': 'st',
                    'transgenic constructs': 'tp',
                    'insertions': 'ti',
                    'transcripts': 'tr',
                    'proteins': 'pp',}
    try:
        return 'FB'+dictionary[val]
    except KeyError:
        raise KeyError('could not process term: {}'.format(val))

def query(identifier):
    url = 'http://flybase.org/search/{}'.format(identifier)
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    key = soup.find_all('script', type='text/javascript')
    for i,t in enumerate(key):
        if t.string is not None:
            if 'FlyBaseHitList' in t.string:
                lstr = t.string.split('"ids":')[1].split(',"filters"')[0]
    return FlyBaseQuery(ast.literal_eval(lstr))
