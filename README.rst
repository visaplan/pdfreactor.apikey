.. This README is meant for consumption by humans and pypi. Pypi can render rst files so please do not use Sphinx features.
   If you want to learn more about writing documentation, please check out: http://docs.plone.org/about/documentation_styleguide.html
   This text does not appear on pypi or github. It is a comment.

==================================================================
pdfreactor.apikey: generate API keys for the PDFreactor webservice
==================================================================
.. image::
   https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336
       :target: https://pycqa.github.io/isort/

It is possible to protect a PDFreactor web service from being used by random
visitors by using API keys, which are not to be confused with the license key.

It is also possible to not install the license key on the server and instead
require the clients to add that key to each conversion request.
This has some drawbacks:

- You must be very very sure not to give access to the license key to anyone
  outside of your own organisation, in order to comply with the license terms.
- There is only one license key in your installation.
  If that key changes, you'd need to reconfigure all of your clients which
  access it; otherwise you might not have access to the newest version on all
  of your clients.
- Anyone who owns a valid license key for PDFreactor can use your server
  (unless other measures to hinder them from doing so, e.g. based on the IP
  address).
  But they did pay to RealObjects (years ago, perhaps),  not to you.

The API key is a possibility to avoid these limitations:
You install your license key on your server, and give API keys to your clients
(or client computers). Now, whenever a key goes wild, you can simply delete
that key from your server configuration.

So far, this package is not needed:  You may create a handcrafted file on your
server, containing keys and descriptions, and distribute the keys to your
respective clients.
Now, whenever one API goes wild, at least your license key is not affected.

But that API key is sent readably with every interesting request to your server (it
is appended to the URL), so it indeed *might* go wild.

This package now offers a possibility to change that key periodically.
This must be done both on client and server side:

On the server, we support the automatic creation of the JSON file which
contains the keys and descriptions, from configured seeds (one per client).
Since the current date is used when creating the keys,
they will be valid for a limited time,
and an attacker will have his/her free lunch for that limited time only.
(You might set up this by a simple cron job, called daily at the same time).

On the client side, everyone gets his/her seed and computes the key,
based on the seed and the current date.
This is done for each request, usually;
the calculation is fast and doesn't require access to any remote data.
The seed is never sent with the conversion requests.

Since the computer clocks might slightly disagree about to current time, we
allow for some fuzz.  For now, the fuzz is one day. This should allow you to
use e.g. date-based keys to support clients all around the world, with wisely
chosen generation time.


Features
========


Examples
========

This add-on can be seen in action at the following sites:

- Is there a page on the internet where everybody can see the features?
- https://www.unitracc.de
- https://www.unitracc.com


Documentation
=============


Translations
------------

This product has been translated into

- Klingon (thanks, K'Plai)


Installation
------------

Install visaplan.PACKAGE by adding it to your buildout::

    [buildout]
    ...
    eggs =
        visaplan.PACKAGE


and then running ``bin/buildout``


Plone integration
~~~~~~~~~~~~~~~~~

After restarting your Zope instance with visaplan.PACKAGE
added to your eggs,
simply use the Plone Add-Ons view or the Quick-Installer to activate it.

Then you may use the configuration registry
to adjust your preferences.


Support
=======

If you are having issues, please let us know;
please use the `issue tracker`_ mentioned below.


Contribute
==========

- Issue Tracker: https://github.com/visaplan/visaplan.PACKAGE/issues
- Source Code: https://github.com/visaplan/visaplan.PACKAGE

License
=======

The project is licensed under the MIT License.

.. _`issue tracker`: https://github.com/visaplan/PACKAGE/issues

.. vim: tw=79 cc=+1 sw=4 sts=4 si et
