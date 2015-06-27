#!/bin/sh
# A deploy script to power keystone by Apache2 Httpd.
# @author gpanda (retaelppa@gmail.com)
# @date Sat May 16 23:27:26 CST 2015

USER=gpanda
GROUP=gpanda


MY_PATCH=gpanda
KEYSTONE_LOG_DIR=/var/log/apache2/keystone
KEYSTONE_CONF_DIR=/etc/keystone
KEYSTONE_APACHE2_CONF=keystone.conf
KEYSTONE_APACHE2_CONF_FULL=/etc/apache2/conf-available/$KEYSTONE_APACHE2_CONF
KEYSTONE_APACHE2_SITE_CONF=wsgi-keystone.conf
KEYSTONE_APACHE2_SITE_CONF_DEBUG=wsgi-keystone-debug.conf
KEYSTONE_APACHE2_SITE_CONF_FULL=\
/etc/apache2/sites-available/$KEYSTONE_APACHE2_SITE_CONF
KEYSTONE_APACHE2_SITE_CONF_DEBUG_FULL=\
/etc/apache2/sites-available/$KEYSTONE_APACHE2_SITE_CONF_DEBUG
KEYSTONE_APACHE2_WSGI_SCRIPT_DIR=/var/www/cgi-bin/keystone
KEYSTONE_APACHE2_WSGI_SCRIPT=keystone.py
KEYSTONE_APACHE2_WSGI_SCRIPT_DEBUG=keystone-debug.py

func_setup() {

    # 1. link keystone configurations
    sudo ln -s \
    $KEYSTONE/$MY_PATCH/httpd/$KEYSTONE_CONF_DIR \
    $KEYSTONE_CONF_DIR

    # 2. link the apache2 httpd conf-available keystone.conf
    # a. build conf with heredoc template
    $KEYSTONE/$MY_PATCH/httpd/etc/apache2/conf-available/genconf.sh
    sudo ln -s \
    $KEYSTONE/$MY_PATCH/httpd/$KEYSTONE_APACHE2_CONF_FULL \
    $KEYSTONE_APACHE2_CONF_FULL

    # 2. link the apache2 httpd sites-available wsgi-keystone.conf
    _conf=
    if [ "$1" = "-X" ]; then
        _conf=$KEYSTONE_APACHE2_SITE_CONF_DEBUG_FULL
    else
        _conf=$KEYSTONE_APACHE2_SITE_CONF_FULL
    fi
    sudo ln -s \
    $KEYSTONE/$MY_PATCH/httpd/$_conf \
    $KEYSTONE_APACHE2_SITE_CONF_FULL

    # 3. link the apache2 httpd wsgi keystone scripts
    sudo mkdir -p $KEYSTONE_APACHE2_WSGI_SCRIPT_DIR
    sudo chown $USER:$GROUP $KEYSTONE_APACHE2_WSGI_SCRIPT_DIR
    _script=
    if [ "$1" = "-X" ]; then
        _script=$KEYSTONE_APACHE2_WSGI_SCRIPT_DEBUG
    else
        _script=$KEYSTONE_APACHE2_WSGI_SCRIPT
    fi
    sudo ln -s \
    $KEYSTONE/$MY_PATCH/httpd/$KEYSTONE_APACHE2_WSGI_SCRIPT_DIR/$_script \
    $KEYSTONE_APACHE2_WSGI_SCRIPT_DIR/main
    sudo ln -s \
    $KEYSTONE/$MY_PATCH/httpd/$KEYSTONE_APACHE2_WSGI_SCRIPT_DIR/$_script \
    $KEYSTONE_APACHE2_WSGI_SCRIPT_DIR/admin

    # 4. setup logs
    sudo mkdir -p $KEYSTONE_LOG_DIR
    sudo chown $USER:$GROUP $KEYSTONE_LOG_DIR

    # 5. enable apache2 httpd keystone conf and the wsgi-keystone site
    sudo a2enconf $KEYSTONE_APACHE2_CONF
    sudo a2ensite $KEYSTONE_APACHE2_SITE_CONF

    # 6. reload apache2
    sudo apache2ctl graceful

}

func_clean() {
    sudo a2dissite $KEYSTONE_APACHE2_SITE_CONF
    sudo a2disconf $KEYSTONE_APACHE2_CONF
    sudo apache2ctl graceful
    sudo rm $KEYSTONE_CONF_DIR
    sudo rm $KEYSTONE_APACHE2_SITE_CONF_FULL
    sudo rm $KEYSTONE_APACHE2_CONF_FULL
    sudo rm $KEYSTONE_APACHE2_WSGI_SCRIPT_DIR/main
    sudo rm $KEYSTONE_APACHE2_WSGI_SCRIPT_DIR/admin
    sudo rm -rf $KEYSTONE_APACHE2_WSGI_SCRIPT_DIR
    sudo rm -rf $KEYSTONE_LOG_DIR
}

if [ "$1" = "-c" ]; then
    func_clean
    exit
elif [ "$1" = "-X" ]; then
    func_setup -X
else
    func_setup
fi
