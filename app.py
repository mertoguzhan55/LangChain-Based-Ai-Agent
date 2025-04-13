from app.agent import Agent
from app.config import Configs
from app.logger import Logger


def main(args,configs):

    logger = Logger(**configs["logger"])

    logger.debug("############ AI AGENT CONFIGURATIONS ############")
    logger.debug(configs)

    if args.test:
        exit()

    agent = Agent(**configs["agent"], logger= logger)
    agent.run_agent()


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-e", "--environment", type=str)
    parser.add_argument("--test", action= "store_true")

    args = parser.parse_args()

    configs = Configs().load(config_name=args.environment)
    main(args, configs)