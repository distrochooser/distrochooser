#!/bin/bash

cp -R node_modules/bootstrap-icons/font/fonts/ ../static/bi-fonts/
cp -R node_modules/flag-icons/flags/ ../static/flags/
sass --watch scss/custom.scss ../static/custom.css   --style compressed
