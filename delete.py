# TOKEN: 194a5e2aeb4447f5b6f9f56d85bf786c
import re
import json
import click
import requests

from cgccli.cgccli_controller import CgccliController
from cgccli.api_service import ApiService



dict_update = ('metadata', 'tags')

@click.command()
@click.option('--token', required=True, help='Your api token.')
@click.option('--project', required=False, default=None, show_default=True, help='Projects to retrieve.')
@click.option('--file', required=False, default=None, show_default=True, help='Files to retrieve or update.')
@click.option('--dest', required=False, default=None, show_default=True, help='Destination to download files.')
@click.argument('argument', nargs=2, required=True)
@click.argument('data', nargs=-1, required=False, default=None)
def main(token, argument, project, file, data, dest):

    cgccli = CgccliController(
        token, argument, project, file, data, dest)

    response = cgccli.make_call()

    click.echo(json.dumps(response)) 



if __name__ == "__main__":
    main()
