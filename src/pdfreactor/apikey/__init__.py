"""
pdfreactor.apikey: generate API keys for the PDFreactor webservice

This package supports periodically changed API keys.
"""

# Python compatibility:
from __future__ import absolute_import, print_function

from six import string_types as six_string_types

# Standard library:
from datetime import datetime, timedelta
from hashlib import sha1
from time import gmtime, localtime, strftime


def make_key(seed, **kwargs):
    """
    Make an apiKey value to be used in a query string to the PDFreactor web
    service.

    This is used both on the client and the server side.

    Required arguments:

    seed -- the seed value, as given to the client.
            It is part of the description for each key in the JSON file created
            on the server; so it contains usually a readable part (indicating
            the customer, client system, or whatever) and a random part,
            to make it less predictable.

    Optional arguments:

    datefmt -- a strftime format string to convert the current datetime to a
            string, reduced to contain the interesting parts only.
            Should only produce numeric output, i.e. no month and weekday names
            (or abbreviations) which may differ, depending on system languages
            and the like.
    now -- the time value to use.
           If a number, will be converted by the gmtime or localtime function
           (depending on the `local` value);
           if a time tuple (resp. the resulting tuple),
           will be converted to a string using the datefmt option.
    local -- use local time?
            Default is False, which means, we use UTC / GMT time
            (unless given a particular time value)
    info -- a list to take processing information.
            This is intended to be
            used for verbose output when using the commandline tool to
            create an API key, e.g. to help with troubleshooting.

    >>> make_key('Our dear customer-adfuw42', now='2022-06-24')
    'bda11d301febf5266376c3b4062d27a91781c7aa'
    >>> make_key('Our dear customer-adfuw42', now=1656071483.460343)
    'bda11d301febf5266376c3b4062d27a91781c7aa'

    Any little error in the seed will of course yield a completely different
    key:
    >>> make_key('Our dear customer -adfuw42', now='2022-06-24')
    '7d95f0e24213aba6cae97383e6e2d661be7fcdc7'

    """
    pop = kwargs.pop
    have_info = 'info' in kwargs
    if have_info:
        info = pop('info')
        if not isinstance(info, list):
            raise ValueError('Expected info option, if given, '
                'to be a list; found %r!', (type(info),
                 ))
    else:
        info = []

    datefmt = pop('datefmt', '%Y-%m-%d')
    local = pop('local', False)
    now = pop('now', None)
    if have_info and not isinstance(now, datetime):
        if local:
            info.append(('INFO', 'Using local time'))
        else:
            info.append(('INFO', 'Using UTC / GMT time'))
    if now is None:
        now = (localtime() if local
               else gmtime())
        if have_info:
            info.append(('INFO', 'Default time is %(now)r' % locals()))
    if isinstance(now, (int, float)):
        if have_info:
            oldval = now
        now = (localtime(now) if local
               else gmtime(now))
        if have_info:
            info.append(('INFO', 'Converted %(oldval)r to %(now)r' % locals()))
    if not isinstance(now, six_string_types):
        if have_info:
            oldval = now
        now = strftime(datefmt, now)
        if have_info:
            info.append(('INFO', 'Converted %(oldval)r to %(now)r' % locals()))

    return sha1(seed+'+'+now).hexdigest()


def keys_and_descriptions(seeds, now, datefmt, fuzz=None, step=None):
    """
    Generate (apiKey, description) tuples, to produce the JSON file
    for the server to read the currently valid keys from.
    The order of the seeds is retained, and if more than one key per seed is
    produced, those will be in adjacent lines.

    We'll use a little demo function for our doctests:
    >>> def kad(*args, **kwargs):
    ...     return list(keys_and_descriptions(*args, **kwargs))
    >>> now=datetime(2022, 6, 25, 17, 45)
    >>> fmt='%Y-%m-%d'
    >>> kad(['our dear customer'], now, fmt)  # doctest: +NORMALIZE_WHITESPACE
    [('238a1809e8b46688a1839a56ca67193fbe88624a',
        'our dear customer (2022-06-25)')]
    >>> kad(['our dear customer', 'our working horse'], now, fmt)
    ...                                       # doctest: +NORMALIZE_WHITESPACE
    [('238a1809e8b46688a1839a56ca67193fbe88624a',
        'our dear customer (2022-06-25)'),
     ('e246d37105dd58646c4a00e96648b78a58f38bd4',
         'our working horse (2022-06-25)')]

    Now for the fuzz.
    Let's say, we want to be prepared for customers around the world, all using
    their own timezone. We support them by providing an additional key with a
    fuzzyness of one day added:
    >>> fuzz=timedelta(days=1)
    >>> kad(['our dear customer'], now, fmt, fuzz=fuzz)
    ...                                       # doctest: +NORMALIZE_WHITESPACE
    [('238a1809e8b46688a1839a56ca67193fbe88624a',
        'our dear customer (2022-06-25)'),
     ('5f40cfef1cf1ee57bc323384cef51f44ee77069d',
        'our dear customer (2022-06-26)')]

    """
    datestrings = set()
    datestrings.add(now.strftime(datefmt))
    if fuzz is not None:
        if step is None:
            step = fuzz
        enddate = now + fuzz
        while 1:
            now += step
            if now > enddate:
                break
            ds = now.strftime(datefmt)
            datestrings.add(ds)
    datestrings = sorted(datestrings)
    for seed in seeds:
        for ds in datestrings:
            yield (make_key(seed, now=ds),
                   seed+' ('+ds+')')


if __name__ == '__main__':
  if 0:
    seed = 'Our dear customer'
    # Logging / Debugging:
    from pdb import set_trace
    set_trace()
    for kw in [{
      'now': 1656071483.460343,
      }, {
      'now': 1656071483.460343,
      }]:
        liz = []
        res = make_key(seed, info=liz, **kw)
        print(res, liz)
  else:
    # Standard library:
    import doctest
    doctest.testmod()
