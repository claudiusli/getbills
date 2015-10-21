#Takes a file with a list of MT account names, one name per line
#also takes a year and month
#note you must use an account with admin privileges
#it outputs the sum of the costs for those users for a given month

import os
import sys
import getopt
import getpass
import base64
import json
import requests

from pprint import pprint

config = dict(
    account_file = '',
    user_name = '',
    year = '',
    month = ''
    )

usage = 'python ' + os.path.basename(__file__) +  ' -a <accounts file> -u <user name> -y <year> -m <month>'

def parse_args(argv):
    '''
    parse through the argument list and update the config dict as appropriate
    '''
    try:
        opts, args = getopt.getopt(argv, "ha:u:y:m:",
                                   ["help",
                                    "accounts",
                                    "username",
                                    "year",
                                    "month"
                                    ])
    except getopt.GetoptError:
        print usage
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print usage
            sys.exit()
        elif opt in ("-a", "--accounts"):
            config['account_file'] = arg
        elif opt in ("-u", "--username"):
            config['user_name'] = arg
        elif opt in ("-y", "--year"):
            config['year'] = arg
        elif opt in ("-m", "--month"):
            config['month'] = arg

def import_accounts():
    '''
    get the list of accounts to check
    '''
    accounts = []
    with open(config['account_file'], 'r') as fh:
        for row in fh:
            accounts.append(row.replace('"','').rstrip())
    config['accounts'] = accounts

def init_config():
    '''
    make sure all the relevant args have been supplied
    '''
    if config['account_file'] == '':
        print usage
        sys.exit()
    if config['user_name'] == '':
        print usage
        sys.exit()
    if config['year'] == '':
        print usage
        sys.exit()
    if config['month'] == '':
        print usage
        sys.exit()
    import_accounts()

def get_password():
    config['password'] = getpass.getpass('Password for {0}: '.format(config["user_name"]))

def get_billing_info():
    '''
    get billing info for each account and add it to <total>
    '''
    total = 0
    #acurl https://<USERNAME>.cloudant.com/_api/v2/bill/<YEAR>/<MONTH#>
    for account in config['accounts']:
        url = 'https://{0}.cloudant.com/_api/v2/bill/{1}/{2}'.format(account, config['year'], config['month'])
        r = requests.get(url, auth=(config['user_name'], config['password']))
        results = json.loads(r.text)
        total += float(results[u'total'].replace(',',''))
    return(total)
        ####Here#####


def main(argv):
    parse_args(argv)
    init_config()
    get_password()
    total = get_billing_info()
    print(total)

if __name__ == "__main__":
    main(sys.argv[1:])
