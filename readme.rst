saymybot
========

Saymybot is a produc of following Learn Python's Bot Path. It is awkward but it works.

Installation
------------

Install virtual enviroment and activate it. After that run:

.. code-block: text

    pip install -r requirements.txt

Put some derp pictures in /images folder. Name them derp*.jp*g

Setup
-----

Create file settings.py and add following to it:

..code-block: python

    PROXY = {'proxy_url': 'socks5://YOUR-SOCKS-PROXY:1080',
    'urllib3_proxy_kwargs': {'username': 'learn', 'password': 'python'}}

    API = "API-KEY-BOTFATHER-GAVE-YOU"

    USER_EMOJI = [':smiley_cat:', ':smiling_imp:', ':panda_face:', ':dog:']

Running
-------

In active virtual enviroment run:

..code-block: text

    python3 saymybot.py