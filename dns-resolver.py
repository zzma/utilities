from dns.resolver import NoAnswer, NXDOMAIN
import json
import os.path
import os
import subprocess
import sys
import logging
import multiprocessing
from multiprocessing import Pool
import time
import socket
import dns.resolver

# alexa domains are at http://s3.amazonaws.com/alexa-static/top-1m.csv.zip

PROCESS_PROCESSES = 100

cache = {}

def lookup(name, rank):
    retv = {}
    retv['domain'] = name
    retv['rank'] = int(rank)
    retv['exchanges'] = []
    try:
        answers = dns.resolver.query(name, 'MX')
    except Exception:
        retv["error"] = "no-mx"
        print json.dumps(retv)
        return
    for rdata in answers:
        mx = {"exchange":str(rdata.exchange), "preference":rdata.preference, "ips":[]}
        if str(rdata.exchange) in cache:
            ips = cache[str(rdata.exchange)]
        else:
            ips = set()
            try:
                for ip in dns.resolver.query(rdata.exchange, 'A'):
                    ips.add(ip.address)
                cache[str(rdata.exchange)] = list(ips)
            except Exception:
                mx["error"] = "no-A-for-exch"
        mx["ips"] = list(ips)
        retv["exchanges"].append(mx)
    print json.dumps(retv)


if __name__ == '__main__':

    pool = Pool(PROCESS_PROCESSES)
    results = []
    for line in open(sys.argv[1]):
        domain = line.rstrip().split(",")[1]
        rank = int(line.rstrip().split(",")[0])
        results.append(pool.apply_async(lookup, [domain,rank]))
    for res in results:
        while 1:
            sys.stdout.flush()
            try:
                res.get(10)
                break
            except multiprocessing.TimeoutError:
                pass
