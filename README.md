# SQLite Clinet written in python3

**TODO**
- [ ] Screenshots
- [ ] Expand db.py
- [ ] Test db.py


## Good completion

![1](screens/1.png)
![2](screens/2.png)

```sh
usage: sqlite [-h] [-d PATH]

optional arguments:
  -h, --help            show this help message and exit
  -d PATH, --database PATH, --db PATH
```

**NOTE**
unless you specify the database location with `--database`, it will be dropped in ~/.sqlite

## Limitations

- Not context sensitive,
- doesn't complete table names
- relies on pandas for displaying data

------------------------------------------------------------------------

#### Dependencies

- [prompt-toolkit](https://github.com/jonathanslenders/python-prompt-toolkit)
- [pandas](https://pandas.pydata.org/)
- python3.6

##### Related

-  [mycli](https://github.com/dbcli/mycli)



