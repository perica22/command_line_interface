import click
import requests



#type=click.File('r')
@click.command()
@click.option('--token', required=True, help='Your api token.')
#@click.argument('f', type=click.Path(exists=True))   ----- format for file path / read  *click.echo(click.format_filename(f))
#@click.option('--project', default=None, show_default=True,  nargs=2, help='Projects to retrieve.')
#@click.option('--file', default=None, show_default=True,  nargs=2, help='Files to retrieve or update.')
#@click.option('--dest', type=click.Path(exists=True), default=None, show_default=True, help='Destination to download files.')
#@click.argument('--customer', default=None)
@click.option('--customer', required=False, default=None)
@click.option('--address', required=False, default=None)
@click.argument('argument', nargs=2, required=True)
def search(token, argument, customer, address):

    headers = {
            "X-Recharge-Access-Token": token,
            "Accept":"application/json",
            "Content-Type":"application/json"
    }

    if customer:
        url = "https://api.rechargeapps.com/customers/{}/addresses".format(customer)

        result = requests.get(url, headers=headers)
        click.echo(result.json()) 
    elif address:
        url = "https://api.rechargeapps.com/addresses/{}".format(address)

        result = requests.get(url, headers=headers)
        click.echo(result.json()) 
    else:
        if argument[1] == 'list':
            url = "https://api.rechargeapps.com/customers/"

            result = requests.get(url, headers=headers)
            click.echo(result.json()) 
        elif argument[1] == 'update':
            pass
        else:
            url = "https://api.rechargeapps.com/customers/{}".format(argument)

            result = requests.get(url, headers=headers)
            click.echo(result.json()) 
    '''
    if argument[0] == 'customer':
    elif argument[1] == 'address':
         if argument[1] == 'list':
            query = argument[1] + 'es'
            url = "https://api.rechargeapps.com/{}/".format(query)

            result = requests.get(url, headers=headers)
            click.echo(result.json()) 
        elif argument[1] == 'update':
            pass
        else:
            url = "https://api.rechargeapps.com/customers/{}".format(argument)

            result = requests.get(url, headers=headers)
            click.echo(result.json()) 
    '''

if __name__ == "__main__":
    search()