# TOKEN: 194a5e2aeb4447f5b6f9f56d85bf786c
import click
import json
import requests

from cgccli.api import ApiService



#type=click.File('r')
#@click.argument('f', type=click.Path(exists=True))   ----- format for file path / read  *click.echo(click.format_filename(f))
#@click.option('--dest', type=click.Path(exists=True), default=None, show_default=True, help='Destination to download files.')
@click.command()
@click.option('--token', required=True, help='Your api token.')
@click.option('--project', required=False, default=None, show_default=True, help='Projects to retrieve.')
@click.option('--file', required=False, default=None, show_default=True, help='Files to retrieve or update.')
@click.argument('argument', nargs=2, required=True)
@click.argument('data', nargs=2, required=False, default=None)
def main(token, argument, project, file, data):

    api_service = ApiService(token)

    if argument[0] == 'projects':
        #cgccli --token 194a5e2aeb4447f5b6f9f56d85bf786c projects list
        response = api_service.get(endpoint='projects/')
        #click.echo(json.dumps(response)) 

    elif argument[0] == 'files':
        if argument[1] == 'list':
            #cgccli --token 194a5e2aeb4447f5b6f9f56d85bf786c files list --project perica22/copy-of-cancer-cell-line-encyclopedia-ccle
            response = api_service.get(
                endpoint="files", query="?project={}".format(project))
            #click.echo(json.dumps(response))             

        elif argument[1] == 'update':
            # check URL for this one
            response = api_service.put(
                endpoint="files", query="?project={}".format(project), data=data)
            #click.echo(json.dumps(response))  

        elif argument[1] == 'stat':
            #cgccli --token 194a5e2aeb4447f5b6f9f56d85bf786c files stat --file 5cff5ac9e4b04e1432b04164
            response = api_service.get(endpoint="files/{}".format(file))
    click.echo(json.dumps(response)) 
            

if __name__ == "__main__":
    main()
