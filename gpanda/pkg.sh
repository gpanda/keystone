#!/bin/sh

zip -rue gpanda-patch.zip \
    pkg.sh \
    memo.rst \
    bootstrap \
    httpd \
    -x \
    httpd/.ropeproject/* \
    httpd/.ropeproject/ \
    httpd/etc/apache2/conf-available/keystone.conf \
    *.log
