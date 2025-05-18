from app.agent import Agent
from app.config import Configs
from app.logger import Logger
from app.fastapi import Fastapi
from app.fastapi_chat import FastAPIServer
from dotenv import load_dotenv
from app.crud import CRUDOperations
import os

def main(args,configs):

    logger = Logger(**configs["logger"])

    logger.debug("############ AI AGENT CONFIGURATIONS ############")
    logger.debug(configs)

    if args.test:
        exit()
    
    agent = Agent(**configs["agent"], logger= logger)

    if args.fastapi:
        crud = CRUDOperations(**configs["crud"], logger = logger)
        # fastapi = Fastapi(**configs["fastapi"],logger=logger, crud = crud)
        fastapi = FastAPIServer(**configs["fastapi_chat"], crud=crud, logger=logger)
        fastapi.run()
    else:
        agent.run_agent()


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-e", "--environment", type=str)
    parser.add_argument("-f", "--fastapi", action= "store_true")
    parser.add_argument("--test", action= "store_true")

    args = parser.parse_args()

    configs = Configs().load(config_name=args.environment)
    main(args, configs)