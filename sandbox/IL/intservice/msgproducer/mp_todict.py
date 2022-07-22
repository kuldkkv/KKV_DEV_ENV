#!/usr/bin/env python


def to_dict(col_names, row):
    dict = {}
    
    for i in range(0, len(col_names)):
        dict [ col_names[i] ] = row[i]

    return dict
