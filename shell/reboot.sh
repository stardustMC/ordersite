#!/usr/bin/env bash

echo -e "\033[34m--------------------wsgi process--------------------\033[0m"

ps -ef|grep uwsgi_ordersite.ini | grep -v grep

sleep 0.5

echo -e '\n--------------------going to close--------------------'

ps -ef |grep uwsgi_ordersite.ini | grep -v grep | awk '{print $2}' | xargs -I{} kill -9 {}

sleep 0.5

echo -e '\n----------check if the kill action is correct----------'

//root/pyenvs/ordersite/bin/uwsgi  --ini uwsgi_ordersite.ini &  >/dev/null

echo -e '\n\033[42;1m----------------------started...----------------------\033[0m'
sleep 1

ps -ef |grep uwsgi_ordersite.ini | grep -v grep
