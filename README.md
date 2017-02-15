# Odoo-new-module
Odoo is an open source ERP system, previously named OpenERP. It is made in Python ;)  
In this project I build a new module for Odoo 10.0 that complies the following requirements:
- Propose ideas. Each idea has the fields Name, Group, Description, Votes, Score (average of the votes' score).
- Vote ideas. Each vote has the fields Score (decimal, 0-10), Person, Datetime.
- Every idea has a start and finish voting date. The finish date should be set automatically one month later
after the start date.
- Grouping people. Each group is composed of a Name and various Persons.

###Installation
Put the module Ideas inside your addons folder. In Windows it is `C:\Program Files\Odoo 10.0\server\odoo\addons`.

###Updating
For updating the module once you have made changes to the code, use: `odoo-bin -d <Database name> --update ideas`.

###Odoo considerations
For creating a new module, use: `odoo-bin scaffold ideas ./odoo/addons`. It will create all the standard files needed for a new module.  
Service port: 8069. Database port: 5432.  
Testing in your browser: `localhost:8069`.  
