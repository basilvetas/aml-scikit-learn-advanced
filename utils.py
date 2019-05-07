#!/usr/bin/python

""" defines utility functions for use in jupyter notebook """
import sys, glob, ssl, certifi
from os import remove
from os.path import dirname, realpath, join
from timeit import default_timer as timer
from tqdm import tqdm
import pandas as pd
import geopy.geocoders
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter

cache_path = join(dirname(realpath(__file__)), '../cache/')
tqdm.pandas()

# https://stackoverflow.com/questions/52824637/why-does-my-geolocation-it-is-not-working
ctx = ssl.create_default_context(cafile=certifi.where())
geopy.geocoders.options.default_ssl_context = ctx


def save_to_cache(path, name, df, **kwargs):
  """ saves df to cache at path under given name """
  start = timer()
  tqdm.write(f'Caching {name} data...')

  if path.endswith('.pkl'):
    df.to_pickle(path, **kwargs)
  elif path.endswith('.hdf'):
    with pd.HDFStore(path, mode='w') as store:
      store.append(name, df, **kwargs)
  else:
    raise ValueError(f'Invalid file extension for path {path}')

  tqdm.write(f'Took {timer() - start:.2f} seconds to cache {name}')
  return


def load_from_cache(path, name, **kwargs):
  """ loads df from cache at path based on given name """
  start = timer()
  tqdm.write(f'Loading {name} data from cache...')
  if path.endswith('.pkl'):
    df = pd.read_pickle(path, **kwargs)
  elif path.endswith('.hdf'):
    df = pd.read_hdf(path, name, **kwargs)
  else:
    raise ValueError(f'Invalid file extension for path {path}')

  tqdm.write(f'Took {timer() - start:.2f} seconds to load {name} data')
  return df


def clear_cache(extensions):
  """ clears cached files of specified extension types """
  tqdm.write('Clearing cache...')
  cached_files = []
  if not extensions:
    extensions = ['hdf', 'pkl', 'tmp']

  for ext in extensions:
    cached_files.extend(glob.glob(join(cache_path, f'*.{ext}*'), recursive=True))

  for file in cached_files:
    remove(file)
  return


def geocoords(addresses):
  """ gets appx latitudes and longitudes from given series of addresses """
  geolocator = Nominatim(timeout=10)
  geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)

  # empty filler
  filler = pd.Series({'Recipient_Latitude': None, 'Recipient_Longitude': None})

  # get coordinates
  coords = addresses.progress_apply(geocode).apply(
    lambda loc: pd.Series({
      'Recipient_Latitude': loc.latitude,
      'Recipient_Longitude': loc.longitude}) if loc is not None else filler)

  return coords


def datetime_lookup(series):
  """
  This is an extremely fast approach to datetime parsing.
  For large data, the same dates are often repeated. Rather than
  re-parse these, we store all unique dates, parse them, and
  use a lookup to convert all dates.

  https://stackoverflow.com/questions/29882573/pandas-slow-date-conversion
  """
  dates = {date: pd.to_datetime(date) for date in series.unique()}
  return series.map(dates)

if __name__ == '__main__':
	clear_cache([]) # clear all cached files
	sys.exit(0)