#194a5e2aeb4447f5b6f9f56d85bf786c
import click
import json
import requests

from cgccli.api import API


#type=click.File('r')
@click.command()
@click.option('--token', required=True, help='Your api token.')
#@click.argument('f', type=click.Path(exists=True))   ----- format for file path / read  *click.echo(click.format_filename(f))
#@click.option('--dest', type=click.Path(exists=True), default=None, show_default=True, help='Destination to download files.')
@click.option('--project', required=False, default=None, show_default=True, help='Projects to retrieve.')
@click.option('--file', required=False, default=None, show_default=True, help='Files to retrieve or update.')
@click.argument('argument', nargs=2, required=True)
@click.argument('data', nargs=2, required=False, default=None)
def main(token, argument, project, file, data):
    headers = {
            "X-SBG-Auth-Token": token,
            "Accept":"application/json",
            "Content-Type":"application/json"
    }

    if argument[0] == 'projects':
        #cgccli --token 194a5e2aeb4447f5b6f9f56d85bf786c projects list
        #url = " https://cgc-api.sbgenomics.com/v2/projects/"
        #result = requests.get(url, headers=headers)
        myProject = API(path=('projects/'), headers=headers)
        response = myProject.api_call()
        click.echo(json.dumps(response)) 

    elif argument[0] == 'files':
        if argument[1] == 'list':
            #cgccli --token 194a5e2aeb4447f5b6f9f56d85bf786c files list --project perica22/copy-of-cancer-cell-line-encyclopedia-ccle
            #url = "https://cgc-api.sbgenomics.com/v2/files?project={}".format(project)
            #result = requests.get(url, headers=headers)
            #click.echo(result.json()) 
            url = "files?project={}".format(project)

            myProject = API(path=url, headers=headers)
            response = myProject.api_call()
            click.echo(json.dumps(response)) 
            

        elif argument[1] == 'update':
            pass

        elif argument[1] == 'stat':
            #cgccli --token 194a5e2aeb4447f5b6f9f56d85bf786c files stat --file 5cff5ac9e4b04e1432b04164
            url = "files/{}".format(file)
            myProject = API(path=url, headers=headers)
            response = myProject.api_call()
            click.echo(json.dumps(response)) 
            #result = requests.get(url, headers=headers)
            #click.echo(result.json()) 


if __name__ == "__main__":
    main()



'''
@click.option('--token', required=True)
@click.group(chain=True)
def main(token):
    pass

@main.command('customers')
def projects():
    click.echo('customers called')

@main.command('addresses')
@click.option('--file', required=False, default=None)
@click.option('--project', required=False, default=None)
@click.option('--dest', required=False, default=None)
def files(addresses):
    click.echo('addresses called')
'''

