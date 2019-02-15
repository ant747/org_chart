'''
Usage:
  org_chart_cli.py <server> reset
  org_chart_cli.py <server> add <add_seq>...
  org_chart_cli.py <server> drop <drop_id>
  org_chart_cli.py -h | --help

Options:
  -h --help     Show this screen

Comments:
  <server>      Server address
  <add_seq>     One or more strings of the following shape: "B1,E1,E2,E3,..." where B1 is boss and E1,... are employees
  <drop_id>     Name of boss/employee to delete
'''

from docopt import docopt
import requests


def print2(s):
    print('  '+s)

def print_response(r):
    print('RESPONSE:')
    print2('status_code: {}'.format(r.status_code))
    print2('content:     {}'.format(r.json()))


def reset(args):
    print('REQUEST...')
    url = 'http://{}/api/orgchart/new'.format(args['<server>'])
    r = requests.post(url)
    print2(r.url)
    print_response(r)

def check_seq_len(seq):
    if len(seq) < 2:
        return 'Sequence too small. At least 2 elements required.'
    return ''

def check_seq_empty_elements(seq):
    if not all(seq):
        return 'Where are empty elements in sequence. Skipping request.'
    return ''

def check_seq_letter(seq):
    if not all([s.isupper() or s.islower() for s in seq]):
        return 'At least 1 element contain no leters. Skipping request.'
    return ''

def add(args):
    seqs = args['<add_seq>']
    for i, s in enumerate(seqs):
        print('REQUEST {}/{}...'.format(i + 1, len(seqs)))
        seq = s.split(',')

        for check in (check_seq_len, check_seq_empty_elements, check_seq_letter):
            wmsg = check(seq)
            if wmsg: break
        if wmsg:
            print2(wmsg)
            continue

        params = {'parent': seq[0], 'childs': ','.join(seq[1:])}
        url = 'http://{}/api/orgchart/add'.format(args['<server>'])
        r = requests.post(url, params=params)
        print2(r.url)
        print2('params={}'.format(params))
        print_response(r)

def drop(args):
    print('REQUEST...')
    url = 'http://{}/api/orgchart/{}'.format(args['<server>'], args['<drop_id>'])
    r = requests.delete(url)
    print2(r.url)
    print_response(r)


if __name__ == '__main__':
    args = docopt(__doc__)
    if args['reset']:
        reset(args)
    elif args['add']:
        add(args)
    elif args['drop']:
        drop(args)

