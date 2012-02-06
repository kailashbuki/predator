import logging
from logging.handlers import SysLogHandler
import sys

FORMAT = '%(asctime)s %(levelname)s %(message)s'

logging.basicConfig(format=FORMAT)
logger = logging.getLogger()
logger.setLevel(logging.INFO)

if 'linux' in sys.platform:
    address = "/dev/log"
else:
    address = ('127.0.0.1', 514)
    
syslog_handler = SysLogHandler(address=address)
logger.addHandler(syslog_handler)
