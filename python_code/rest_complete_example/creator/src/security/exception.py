#!/usr/bin/env python


class SecurityException(Exception):
    def __init__(self, errc, errm):
        self.msg = errc + ': ' + errm
        self.errc = errc
        self.errm = errm
