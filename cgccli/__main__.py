# TOKEN: 194a5e2aeb4447f5b6f9f56d85bf786c
import json
import click

from cgccli.utils import noCommandFound
from cgccli.cgccli_controller import CgccliController



@click.command()
@click.argument('argument', nargs=2, required=True)
@click.argument('data', nargs=-1, required=False, default=None)
@click.option('--token', required=True, help='Your api token.')
@click.option('--project', required=False, default=None, show_default=True, help='Projects to retrieve.')
@click.option('--file', required=False, default=None, show_default=True, help='Files to retrieve or update.')
@click.option('--dest', required=False, default=None, show_default=True, help='Destination to download files.')
def main(token, argument, project, file, data, dest):

    # instance of cgccli controler
    cgccli = CgccliController(token)

    # checkig the project and file, and calling the controller
    if argument[0] == 'projects':
        response = cgccli.make_project_call(argument[1])
        if response:
            click.echo(json.dumps(response)) if isinstance(response, dict) else click.echo(response)
        else:
            noCommandFound(argument[1])

    elif argument[0] == 'files':
        response = cgccli.make_files_call(
            argument[1], project=project, data=data, file=file, dest=dest)
        if response:
            click.echo(json.dumps(response)) if isinstance(response, dict) else click.echo(response)
        else:
            noCommandFound(argument[1])
    else:
        noCommandFound(argument[0])



if __name__ == "__main__":
    main()
