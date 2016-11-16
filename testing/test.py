#!/usr/bin/env python
# -*- coding: utf-8 -*-

import subprocess
import xmlrpc.client
import os
import time
import pyaria2

def main():
    download = pyaria2.PyAria2()
    download.addUri(['http://archvps/next.txt'])
    input()

main()
