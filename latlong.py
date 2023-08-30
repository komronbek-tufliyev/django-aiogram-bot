# For Geo Location

from geopy.geocoders import Nominatim

def get_lat_lot(latitude, lotitude):
    geolocator = Nominatim(user_agent="geoapiExercises")
    location = geolocator.reverse(f"{latitude}, {lotitude}")
    return location.address