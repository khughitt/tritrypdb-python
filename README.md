tritrypdb-python
================
Overview
--------
A few small Python functions for working with [TriTrypDB](http://tritrypdb.org/tritrypdb/)
data files. An alternate version written for the R programming language is 
available at
[github.com/khughitt/tritrypdb](https://www.github.com/khughitt/tritrypdb).

Installation
------------
Download the latest version of tritrypdb-python from Github:

    git clone https://www.github.com/khughitt/tritrypdb-python

Usage
-----
```python
import tritrypdb
df = tritrypdb.parse_gene_info_table('TriTrypDB-5.0_TbruceiLister427Gene.txt')
```

