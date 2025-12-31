def final(stylometry, temporal):
    return round((stylometry * 0.7 + temporal * 0.3) * 100, 2)
