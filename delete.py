# TOKEN: 194a5e2aeb4447f5b6f9f56d85bf786c
import re
import json
import click
import requests

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

    api_service = ApiService(token)

    if argument[0] == 'projects':
        #cgccli --token 194a5e2aeb4447f5b6f9f56d85bf786c projects list
        response = api_service.get(endpoint='projects/')

    elif argument[0] == 'files':
        if argument[1] == 'list':
            #cgccli --token 194a5e2aeb4447f5b6f9f56d85bf786c files list --project perica22/copy-of-cancer-cell-line-encyclopedia-ccle
            response = api_service.get(
                endpoint="files", query="?project={}/".format(project))

        elif argument[1] == 'update':
            #cgccli --token 194a5e2aeb4447f5b6f9f56d85bf786c files update --file 5cff5ac9e4b04e1432b04164 tags=["marina", "perica", "nikola", "jovica"]
            
            data = re.findall(r"[\w']+", ' '.join(data))

            if data[0] in dict_update:
                endpoint_extension = data.pop(0)

                response = api_service.put(
                    endpoint="files/{}/{}".format(file, endpoint_extension), data=data)
            else:
                response = api_service.patch(
                    endpoint="files/{}/".format(file), data=data)

        elif argument[1] == 'stat':
            #cgccli --token 194a5e2aeb4447f5b6f9f56d85bf786c files stat --file 5cff5ac9e4b04e1432b04164
            response = api_service.get(endpoint="files/{}/".format(file))

        elif argument[1] == 'download':
            #cgccli --token 194a5e2aeb4447f5b6f9f56d85bf786c files download --file 5cff5ac9e4b04e1432b04164 --dest perica.txt
            response = api_service.get(
                endpoint="files/{}/download_info/".format(file))
            content = downloadFile(response['url'], dest)

    click.echo(json.dumps(response)) 
            
def downloadFile(url, file_name):
    with open(file_name, "wb") as file:
        # get request
        response = requests.get(url)
        # write to file
        file.write(response.content)


if __name__ == "__main__":
    main()
