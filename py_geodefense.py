from geopy.distance import geodesic

def geodist(oldcoords, newcoords):
    print(geodesic(oldcoords, newcoords).miles)
    return geodesic(oldcoords, newcoords).feet

def main():
    oldcoords = (34.049804333333334, -117.62820383333334)
    newcoords = (34.049825166666665, -117.62928633333333)
    dist = geodist(oldcoords, newcoords)
    print(dist)

if __name__ == '__main__':
    main()
