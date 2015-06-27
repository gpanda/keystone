#!/bin/sh
cur=`pwd`
box=`dirname $0`

cd $box

. ./keystone.env
cat >keystone.conf<<EOF
Define KEYSTONE_ROOT ${KEYSTONE_ROOT}
EOF

cd $cur
