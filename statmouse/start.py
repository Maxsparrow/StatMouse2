import logger
from statmouse.apihandler import APIHandler
from statmouse.connections import HOST, DATABASE, USER, PASS, AUTH_KEY
from statmouse.sql import SQLConnection
from statmouse.sqlhandler import SQLHandler
from statmouse.summoners import Summoners

PROJECT_NAME = 'statmouse'

def start():
    logger.set_logging(PROJECT_NAME)

    sql = SQLConnection(host=HOST, user=USER, passwd=PASS, default_db=DATABASE)
    sqlhandler = SQLHandler(sql)
    apihandler = APIHandler(AUTH_KEY)

    # seeds = [31014009, 53742348, 60783]
    summoners = Summoners(apihandler, sqlhandler)
    summoners.get_new_summoner_ids(amount=50000)

if __name__ == "__main__":
    start()