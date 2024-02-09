# script to crawl api and record payload

import argparse
import httpx
import logging
from pathlib import Path
import sys

# NSLS2API_BASEURL = "https://api-staging.nsls2.bnl.gov"
NSLS2API_BASEURL = "fail_url"
logger = logging.getLogger(__name__)


def test_request_handler(request):
    url_path_to_filename = {
        "/proposal/312064/directories": "312064_directories.json",
        "/proposal/312064": "312064.json",
        "/proposal/314180/directories": "314180_directories.json",
        "/proposal/314180": "314180.json",
        "/facility/nsls2/cycles": "cycles.json",
        "/instruments": "instruments.json",
        "/proposals/2023-1": "proposals_20231.json",
        "/proposals/2024-1": "proposals_20241.json",
    }
    if request.method != "GET":
        raise ValueError("Only GET requests are mocked.")
    try:
        filename = url_path_to_filename[request.url.path]
    except KeyError:
        raise ValueError(f"No response cached for: {request.url}")
    body = Path("test_data", filename).read_text()
    return httpx.Response(200, content=body)

def main(args=None):
    """
    This can be used interactively like

    >>> main(["--cycle", "2022-2"])

    equivalent to

    $ python3 create_proposal_directories.py 2022-2
    """
    parser = argparse.ArgumentParser(
        description="Create proposal directories for a given cycle. If multiple options of cycle,\
        instrument, and proposal are specified, only directories that meet all criteria are created."
    )
    # parser.add_argument(
    #     "--cycles",
    #     nargs="*",
    #     help="The names of the cycles to process (e.g. 2020-1). If unspecified, do all.",
    # )
    # parser.add_argument(
    #     "--instruments",
    #     nargs="*",
    #     help="Name of the instrument to process (e. g. amx). If unspecified, do all.",
    # )
    # parser.add_argument(
    #     "--proposals",
    #     nargs="*",
    #     help="Number of the proposal to process (e. g. 300000). If unspecified, do all.",
    # )
    parser.add_argument(
        "--prefix",
        type=Path,
        # default="/nsls2/data",
        default="/tmp/proposals/",
        help="Default prefix for path to create. If unspecified, value is '/nsls2/data'.",
    )
    parser.add_argument(
        "--test",
        action="store_true",
        default=True,
        help="Testing mode - use test data.",
    )
    # parser.add_argument(
    #     "--dry-run",
    #     action="store_true",
    #     default=False,
    #     help="Dry run - do not do actions that change file systems.",
    # )
    # parser.add_argument(
    #     "--verbose",
    #     "-v",
    #     action="count",
    #     help="Show more log messages. (Use -vv for even more.)",
    # )
    # parser.add_argument(
    #     "--strict",
    #     action="store_true",
    #     default=False,
    #     help="Die on first failure rather than accumulating errors.",
    # )

    args = parser.parse_args(args or sys.argv[1:])
    if args.verbose:
        if args.verbose == 1:
            logging.basicConfig(level="INFO")
        if args.verbose >= 2:
            logging.basicConfig(level="DEBUG")
        else:
            logging.basicConfig()  # "WARNING" by default

    if args.test:
        logger.info("TESTING MODE - proposals 314180 and 312064 available")
        client = httpx.Client(
            base_url=NSLS2API_BASEURL,
            transport=httpx.MockTransport(test_request_handler),
        )
    # else:
    #     client = httpx.Client(base_url=NSLS2API_BASEURL)

    prefix = args.prefix
