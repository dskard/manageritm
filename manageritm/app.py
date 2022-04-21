from manageritm.server import create_app

import argparse
import logging

def parse_arguments():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--config",
        "-c",
        help='configuration file',
        default=None,
        type=str,
    )

    opts, unknowns = parser.parse_known_args()
    return opts,unknowns


def main():
    opts, unknowns = parse_arguments()
    app = create_app(opts.config)

    # share flask app logs with gunicorn
    # set the flask app log level to the same as gunicorn
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)

    return app


if __name__ == "__main__":
    # module was called as a program
    app = main()
    app.run()
