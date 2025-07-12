#!/bin/bash

coverage run -m pytest tests/
coverage report
coverage html
firefox-esr htmlcov/index.html
