# -*- coding: utf-8 -*-

# Ordered Dict because A1 > A2 > A3 (A1 has presedence over A2).
# If any of A1 list element is True in the object being studied, A1 scale is used. If not, if any A2 list element is True ...

threat_index_by_macro_zones_national = {
    1: (0.23, 0.25),
    2: (0.34, 0.38),
    3: (0.45, 0.50),
    4: (0.56, 0.63),
    5: (0.68, 0.75),
    6: (0.80, 0.88),
    7: (0.90, 1.00),}

threat_index_by_macro_zones_caracas = {
    'sur':          (0.68, 0.75),
    'centro_sur':   (0.60, 0.66),
    'centro_norte': (0.64, 0.70),
    'norte':        (0.68, 0.75),
    }

building_ussage = { 
    'A1':{
        'scale':[
            (lambda _: _ <= 10.0, 0.9),
            (lambda _: 10.0 < _ <= 100.0, 0.92),
            (lambda _: 100.0 < _ <= 500.0, 0.95),
            (lambda _: 500.0 < _ <= 1000.0, 0.97),
            (lambda _: 1000.0 < _, 1.0)
            ],
        'list':['firemen', 'civil_defense', 'medical_care']
        },
    'A2':{
        'scale':[
            (lambda _: _ <= 10.0, 0.85),
            (lambda _: 10.0 < _ <= 100.0, 0.87),
            (lambda _: 100.0 < _ <= 500.0, 0.90),
            (lambda _: 500.0 < _ <= 1000.0, 0.93), # único con diferencia de 4 en vez de 5 con respecto a A1
            (lambda _: 1000.0 < _, 0.95)
            ],
        'list':['governmental', 'police', 'military', 'educational']
        },
    'A3':{
        'scale':[
            (lambda _: _ <= 10.0, 0.80),
            (lambda _: 10.0 < _ <= 100.0, 0.82),
            (lambda _: 100.0 < _ <= 500.0, 0.85),
            (lambda _: 500.0 < _ <= 1000.0, 0.87),
            (lambda _: 1000.0 < _, 0.90)
            ],
        'list':['popular_housing', 'single_family', 'multifamily', 'sports_recrea', 'cultural', 'industrial', 'commercial', 'office', 'religious', 'other']
        }
    }

building_age = dict([
    ('<1940', 100),
    ('[1940, 1947]', 80),
    ('[1948, 1955]', 80),
    ('[1956, 1967]', 100),
    ('[1968, 1982]', 60),
    ('[1983, 1998]', 40),
    ('[1999, 2001]', 15),
    ('>2001', 20)
    ])
