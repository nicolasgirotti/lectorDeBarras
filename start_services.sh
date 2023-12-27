#!/bin/bash
service mariadb start
python app.py host=0.0.0.0

