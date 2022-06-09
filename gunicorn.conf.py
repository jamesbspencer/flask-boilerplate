#!/user/bin/env python3

## gunicorn config file.
# Defaults: https://docs.gunicorn.org/en/stable/settings.html#config-file

import os
from datetime import datetime

log_path = "data/logs"
if not os.path.exists(log_path):
    os.makedirs(log_path)

time = datetime.now()
today = time.strftime('%Y%m%d')

loglevel = 'info'
accesslog = 'data/logs/' + today + "-access.log"
errorlog = 'data/logs/' + today + '-error.log'