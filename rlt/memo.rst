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

Keystone
--------

.. code:: bash

   cp etc/keystone.conf.sample etc/keystone.conf
   # config admin_token
   openssl rand -hex 10

References
----------

reStructuredText 'code' name: http://pygments.org/docs/lexers/

http://docs.openstack.org/

  + http://docs.openstack.org/juno/install-guide/install/apt/content/keystone-install.html
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
