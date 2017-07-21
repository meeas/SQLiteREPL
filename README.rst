#################################
SQLite Clinet written in python3
#################################

**TODO**

- [ ] Screenshots
- [ ] Expand db.py
- [ ] Test db.py


Good completion
---------------

.. image:: screens/1.png
   :name: my picture
   :scale: 50 %
   :alt: alternate text
   :align: center

.. image:: screens/2.png
   :name: my picture
   :scale: 50 %
   :alt: alternate text
   :align: center


```sh
usage: sqlite [-h] [-d PATH]

optional arguments:
  -h, --help            show this help message and exit
  -d PATH, --database PATH, --db PATH
```

**NOTE**
unless you specify the database location with `--database`, it will be dropped in ~/.sqlite

Limitations
-----------

- Not context sensitive,
- doesn't complete table names
- relies on pandas for displaying data

Dependencies
------------

- [prompt-toolkit](https://github.com/jonathanslenders/python-prompt-toolkit)
- [pandas](https://pandas.pydata.org/)
- python3.6

Related
-------

-  [mycli](https://github.com/dbcli/mycli)



