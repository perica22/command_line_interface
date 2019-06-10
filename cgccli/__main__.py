import sys
import click
import requests
from functools import wraps
from .classmodule import MyClass
from .funcmodule import my_function



'''
@click.command()
@click.option('--count', default=1, help='Number of greetings.')
@click.option('--name', help='The person to greet.')
def hello(count, name):
    """Simple program that greets NAME for a total of COUNT times."""
    for x in range(count):
        click.echo('Hello %s!' % name)
'''

@click.command()
@click.option('--token', required=True, help='Your api token.')
@click.option('--customer', default=None, show_default=True,  nargs=2, help='Customer to retrieve.')
#@click.option('--project', default=None, show_default=True,  nargs=2, help='Customer to retrieve.')
#@click.option('--file', default=None, show_default=True,  nargs=2, help='Customer to retrieve.')
#@click.option('--dest', default=None, show_default=True,  nargs=2, help='Customer to retrieve.')
@click.argument('customers', nargs=2)
def search(token, customer, customers=None):

    headers = {
            "X-Recharge-Access-Token": token,
            "Accept":"application/json",
            "Content-Type":"application/json"
    }
    if customer:
        url = "https://api.rechargeapps.com/customers/{}".format(customer)

        result = requests.get(url, headers=headers)
        click.echo(result.json()) 
    elif customers:
        if customers[1] == 'list':
            url = "https://api.rechargeapps.com/customers/"

            result = requests.get(url, headers=headers)
            click.echo(result.json()) 


if __name__ == "__main__":
    search()