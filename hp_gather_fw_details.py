#!/usr/bin/env python

# Purpose - To Gather HP Proliant Firmware Details using ILO4
# Amit Biyani - Aug 15, 2016

import hpilo
import sys
import argparse


def connect(host, user, pwd):
    if not (host or user or pwd):
        print("Could not connect! Parameters were not all provided")
    ilo = hpilo.Ilo(host, login=user, password=pwd, timeout=120,
                    port=443, protocol=None)
    return ilo


def get_fw_info(response):
        print "-" * 100
        print ("| {:63} | {:30} |".format("NAME", "VERSION"))
        print "-" * 100
        for fw_name, fw_version in response.iteritems():
            try:
                print ("| {:63} | {:30} |".format(fw_name, fw_version))
            except ValueError:
                continue

        print "-" * 100


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='=> Get HP Proliant Servers \
                                     Firmware Details')
    parser.add_argument('-l', '--login', action='store', help='',
                        dest='ilo_user', required=True)
    parser.add_argument('-p', '--password', action='store', help='',
                        dest='ilo_pass', required=True)
    parser.add_argument('-s', '--serverilo', action='store', help='',
                        dest='ilo_host', required=True)
    ilo_cred = parser.parse_args()

    try:
        ilo_conn = connect(ilo_cred.ilo_host, ilo_cred.ilo_user,
                           ilo_cred.ilo_pass)
        fw_info = ilo_conn.get_embedded_health()['firmware_information']
    except hpilo.IloLoginFailed:
        print "Login Error Failed"
        sys.exit(1)

    get_fw_info(fw_info)
    exit(0)
