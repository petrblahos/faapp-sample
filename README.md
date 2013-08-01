faapp-sample
============

Sample pyramid + formalchemy application as it evolved.

step01
======
Our starting point

step02
======
* Enumerating models only once in model/meta.py
* edit and saveedit handlers merged

step03
======
* Added a mechanism to define model-specific grids and fieldsets

step04
======
* Wrong implementation of *edit* and *delete* links by adding fields to the grid
* This approach will be abandoned

step05
======
* Using custom templates to implement the *edit* and *delete* links

step06
======
* So far the application only worked if the models have the primary key named *id*
* Here we make a new table (NonId) with a different primary key just to see what it causes

step07
======
* Changed the routes, the primary key is not a part of the route but a request parameter instead
* Added functions to parse and generate the primary key to request parameters mapping

step08
======
* Defined a custom context factory to fetch data for given request params
* The views have been significantly simplified by this

step09
======
* Localization of both formalchemy messages and our own messages must work

