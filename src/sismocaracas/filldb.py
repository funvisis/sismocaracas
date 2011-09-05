# -*- coding: utf-8 -*-

def pluralize(s):
    '''quick and dirty implementation.

    when finded, substitute the function pluralize:

    args = ['spanish', ...]
    kwargs = {'speed':'be quick', ...}
    pluralize = lambda _: the_good_pluralize_implementation(_, *args, **kwargs)
    '''
    if any(s.endswith(_) for _ in ('aeiou')):
        s += 's'
    else:
        s += 'es'
    return s

import sys
import os

sys.path.append(os.getcwd().rsplit('/', 1)[0])

from optparse import OptionParser

usage = "usage: %prog -s SETTINGS -f CSV | --settings=SETTINGS --from=CSV"
parser = OptionParser(usage)
parser.add_option('-s', '--settings', dest='settings', metavar='SETTINGS',
                  help="The Django settings module to use")
parser.add_option('-f', '--from', dest='csv', metavar='CSV',
                  help="The Comma Separated Values file to read from")
(options, args) = parser.parse_args()
if not options.settings:
    parser.error("You must specify a settings module")

if not options.csv:
    parse.error("You must specify a source file")

os.environ['DJANGO_SETTINGS_MODULE'] = options.settings

from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from funvisis.django.fvisusers.models import FVISUser

import csv

reader = csv.reader(open(options.csv, 'r'), delimiter='\t', quotechar='\\')

row_dist = {
    'ci': 0,
    'first_name': 1,
    'last_name': 2,
    'email': 3,
    'phone': 4,
    'group': 5,}

all_groups = {_.name.lower(): _ for _ in Group.objects.all()}
base_groups = ['base'] # Everybody beongs to these groups
admin_groups = ['administradores', 'admins']

base_groups = [Group.objects.get(name=_) for _ in base_groups]

for record in reader:
    userkw = {}
    fill_kwargs = lambda d, kw: d.update(
        {
            kw: record[row_dist[kw]]})
    fill_kwargs(userkw, 'first_name')
    fill_kwargs(userkw, 'last_name')
    fill_kwargs(userkw, 'email')

    userkw['username'] = ''.join(
        letter for letter in
        userkw['first_name'][0] + userkw['last_name']
        if letter.isalpha()).lower()

    userkw['is_staff'] = True
    userkw['is_active'] = True

    u = User(**userkw)

    password = User.objects.make_random_password()
    u.set_password(password)

    u.save()
    print u.first_name, u.last_name, u.email, u.username, password

    for group_name in (
        pluralize(_.strip()).lower() for _ in
        record[row_dist['group']].split(',')):

        if group_name in admin_groups:
            u.is_superuser = True
        else:
            try:
                u.groups.add(all_groups[group_name])
            except KeyError:
                sys.stderr.write('Error: ' +  group_name + '\n')

    for group in base_groups:
        u.groups.add(group)

    fvisuserkw = {}
    fill_kwargs(fvisuserkw, 'ci')
    fill_kwargs(fvisuserkw, 'phone')
    fvisuserkw['user'] = u
    fu = FVISUser(**fvisuserkw)

# Probar con nombres diferentes que generen iguales usuarios
