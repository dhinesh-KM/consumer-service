import os

env = os.getenv('ENV', 'dev')  # Default to 'dev' if 'ENV' is not set

if env == 'prod':
    from devsettings import *
else:
    from prodsettings import *
