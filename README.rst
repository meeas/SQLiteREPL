#################################
SQLite Clinet written in python3
#################################

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


.. code-block:: sh

	usage: sqlite [-h] [-d PATH]

	optional arguments:
	-h, --help            show this help message and exit
	-d PATH, --database PATH, --db PATH


.. note::
	unless you specify the database location with `--database`, it will
	be dropped in ~/.sqlite


Limitations
-----------
- Not context sensitive,
- doesn't complete table names
- no table headings

Dependencies
------------
- `prompt-toolkit <https://github.com/jonathanslenders/python-prompt-toolkit>`__
- `tabulate`__
- python3.6

Related
-------

- <https://github.com/dbcli/mycli>

