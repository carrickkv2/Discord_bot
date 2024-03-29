from geopy.extra.rate_limiter import RateLimiter
from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder


def get_timezone_of_user(time: str) -> str:
    """
    Get's the timezone from a string.
    The string is then converted to the longitude and latitude of the place
    the user gives and from there converted to a pytz timezone.
    """
    geo_locator = Nominatim(user_agent="Testing_for_bot")  # replace with yours
    RateLimiter(geo_locator.geocode, min_delay_seconds=5, return_value_on_exception=None)

    lad = str(time)
    location = geo_locator.geocode(lad)
    obj = TimezoneFinder()
    result = obj.timezone_at(lng=location.longitude, lat=location.latitude)
    return str(result)
