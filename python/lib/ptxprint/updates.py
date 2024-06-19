#!/usr/bin/python3

import urllib.request as urq
from urllib.error import HTTPError

def test_url(url):
    request = urq.Request(url)
    request.get_method = lambda: 'HEAD'
    try:
        response = urq.urlopen(request, timeout=30)
    except HTTPError:
        return 404
    return response.status

def test_update(urlt, primary=0, major=0, minor=0, minimus=0):
    newp = primary + 1
    while test_url(urlt.format("{}.{}".format(newp, 0))) == 200:
        newp += 1
    primary = newp - 1
    newm = major + 1
    while test_url(urlt.format("{}.{}".format(primary, newm))) == 200:
        newm += 1
    if newm > major + 1:
        major = newm - 1
        newm = 0
        while test_url(urlt.format("{}.{}.{}".format(primary, major, newm))) == 200:
            newm += 1
        if newm > 0:
            minor = newm - 1
            newm = 1
            while test_url(urlt.format("{}.{}.{}.{}".format(primary, major, minor, newm))) == 200:
                newm += 1
            if newm > 1:
                minimus = newm - 1
                res = urlt.format("{}.{}.{}.{}".format(primary, major, minor, minimus))
            else:
                minimus = 0
                res = urlt.format("{}.{}.{}".format(primary, major, minor))
        else:
            minimus = 0
            minor = 0
            res = urlt.format("{}.{}".format(primary, major))
    else:
        major = 0
        minor = 0
        minimus = 0
        res = urlt.format("{}".format(primary))

    return (res, primary, major, minor, minimus)
    

if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        print(test_url(sys.argv[1]))
    else:
        print(test_update("https://software.sil.org/downloads/r/ptxprint/SetupPTXprint({}).exe", 1, 7)[0])

