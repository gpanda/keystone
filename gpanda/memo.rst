#######################
Gpanda's Keystone Notes
#######################


venv
----

.. code:: bash

   python tools/bin/install_venv.py
   source .venv/bin/activate
   deactivate


doc
---

.. code:: bash

   cd doc
   make html


MySQL
-----

.. code:: mysql

   mysql> create database keystone charset utf8;
   mysql> create user 'keystone'@'localhost' identified by 'keyst0ne';
   mysql> grant all on keystone.* to 'keystone'@'localhost';
   mysql> grant all on keystone.* to 'keystone'@'%';

   pip install MySQL-python

Keystone
--------

.. code:: bash

   cp etc/keystone.conf.sample etc/keystone.conf

   # config admin_token
   # openssl rand -hex 10
   [DEFAULT]
   ...
   admin_token=71f796c2943f084e2dc5

   # config db connection
   [database]
   ...
   connection = mysql://keystone:<KEYSTONE_DBPASS>@<controller>/keystone

   [memcache]
   ...
   servers = localhost:11211

   [token]
   ...
   provider = keystone.token.providers.uuid.Provider
   # driver = keystone.token.persistence.backends.sql.Token
   driver = keystone.token.persistence.backends.memcache.Token

   hash_algorithm = sha256

   [revoke]
   ...
   driver = keystone.contrib.revoke.backends.sql.Revoke

   [DEFAULT]
   ...
   log_dir = /var/log/keystone
   # (Optional)
   [DEFAULT]
   ...
   debug = true
   verbose = true

Keystone on Apache2 Httpd
-------------------------

.. code:: bash

   #!/bin/sh

   # 1. link keystone configurations
   sudo ln -s \
   $KEYSTONE/gpanda/httpd/etc/keystone \
   /etc/keystone

   # 2. link the apache2 httpd sites-available wsgi-keystone.conf
   sudo ln -s \
   $KEYSTONE/gpanda/httpd/etc/apache2/sites-available/wsgi-keystone.conf \
   /etc/apache2/sites-available/wsgi-keystone.conf

   # 3. link the apache2 httpd wsgi keystone scripts
   sudo mkdir -p /var/www/cgi-bin/keystone
   sudo chown gpanda:gpanda /var/www/cgi-bin/keystone
   sudo ln -s \
   $KEYSTONE/gpanda/httpd/var/www/cgi-bin/keystone/keystone.py \
   /var/www/cgi-bin/keystone/main
   sudo ln -s \
   $KEYSTONE/gpanda/httpd/var/www/cgi-bin/keystone/keystone.py \
   /var/www/cgi-bin/keystone/admin

   # 4. setup log directory
   sudo mkdir -p /var/log/apache2/keystone
   sudo chown gpanda:gpanda /var/log/apache2/keystone

   # 5. enable keystone apache2 wsgi site
   sudo a2ensite wsgi-keystone.conf

   # 6. reload
   sudo apache2ctl graceful

Keystone BootStrap
------------------



References
----------

reStructuredText 'code' name: http://pygments.org/docs/lexers/

http://docs.openstack.org/

  + http://docs.openstack.org/kilo/install-guide/install/apt/content/keystone-install.html
  + http://docs.openstack.org/api/quick-start/content/
  + http://docs.openstack.org/user-guide/content/cli_openrc.html
  + http://docs.openstack.org/developer/python-openstackclient/
  + http://docs.openstack.org/developer/keystone/cli_examples.html
  + http://docs.openstack.org/developer/keystone/api_curl_examples.html
  + http://docs.openstack.org/developer/python-openstackclient/
  + http://docs.openstack.org/developer/keystone/http-api.html

http://adam.younglogic.com/

  + http://adam.younglogic.com/2013/07/a-vision-for-keystone/
  + http://adam.younglogic.com/2013/09/keystone-v3-api-examples/
