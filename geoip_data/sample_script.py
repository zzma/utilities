'''
Processes a file of IP addresses and adds geographic and ASN information

Usage: sample_script.py ip.list

Output: csv with ip,asn,country_code,longitude,latitude

'''

import csv
import sys
import time

import geoip2.database
import pyasn

start = time.clock()
reader = geoip2.database.Reader('GeoIP2-City.mmdb')
print("Read geoip database in: " + str(time.clock() - start))
sys.stdout.flush()

start = time.clock()
ASES = pyasn.pyasn('ipasn_db_20200119')
print("Read asn database in: " + str(time.clock() - start))
sys.stdout.flush()

def get_asn(ip_address):
    asn = ASES.lookup(ip_address)[0]
    return int(asn) if asn else 0

def get_geo_info(ip_address):
    try:
        response = reader.city(ip_address)
    except Exception:
        return {
            'country_code': '',
            'longitude': '',
            'latitude': '',
        }

    return {
        'country_code': response.country.iso_code,
        'longitude': response.location.longitude,
        'latitude': response.location.latitude,
    }


with open(sys.argv[2], "w") as out:
    writer = csv.writer(out)
    for line in open(sys.argv[1]):
        ip_addr = line.strip()

        geo_info = get_geo_info(ip_addr)
        data = [ip_addr, get_asn(ip_addr),geo_info['country_code'],geo_info['longitude'],geo_info['latitude']]

        writer.writerow(data)


