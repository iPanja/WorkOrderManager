# Work Order Manager
Created by iPanja#0959. Please open an issue or contact me if you have any problems.

# Dependencies
* Python 3
* MySQLdb
* Discord-py

# Setup
Install some type of application to setup a MySQL server.

* WAMP is a free Windows option
* MAMO is a free OS X option

Execute/import the `database.sql` file to automatically setup the database

Replace `key="<TOKEN>"` with your Discord bot token (Obtained from the [Discord developer portal](https://discordapp.com/developers/applications/me))

Run the `main.py` file. Thats it! Your bot should now be fully functional!

# Usage
* `!order <item> <amount>` - Creates a new order. (Amount will be set to 1 if not provided)
* `!orderfinish <item> <amount>` - Updates an existing order, subtracting the old amount by the provided one. (Amount will be set to 1 if not provided)
* `!orderlist` - Direct messages the list of all current orders

# MySQL Errors
If you are receiving MySQL related errors you may have to change some of the options on `line 8` of `Manager.py`. In the future these options will be put in the config file.

# Dislaimer
This product is new and has not been extensively tested, you may run into issues.