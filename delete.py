# TOKEN: 194a5e2aeb4447f5b6f9f56d85bf786c
import re
import json
import click
import requests

from cgccli.cgccli_controller import CgccliController



@click.command()
@click.argument('argument', nargs=2, required=True)
@click.argument('data', nargs=-1, required=False, default=None)
@click.option('--token', required=True, help='Your api token.')
@click.option('--project', required=False, default=None, show_default=True, help='Projects to retrieve.')
@click.option('--file', required=False, default=None, show_default=True, help='Files to retrieve or update.')
@click.option('--dest', required=False, default=None, show_default=True, help='Destination to download files.')
def main(token, argument, project, file, data, dest):

    import ipdb
    ipdb.set_trace()
    shipping_address_data = {'billing_address[province_state]': u'Michigan', 'shipping_address[last_name]': u'Candy', 'shipping_address[first_name]': u'Lolipop', 'billing_address[phone]': u'', 'shipping_address[province_state]': u'Michigan', 'billing_address[postalcode]': u'48212', 'billing_address[first_name]': u'Lolipop', 'billing_address[address_1]': u'2017 Nikola Tesla Dr', 'shipping_address[city]': u'Detroit', 'billing_is_shipping': u'0', 'shipping_address[phone]': u'', 'shipping_address[address_1]': u'2015 Nikola Tesla Dr', 'billing_address[country]': u'United States', 'shipping_address[country]': u'United States', 'billing_address[email]': u'example_mail@gmail.com', 'shipping_address[postalcode]': u'48212', 'billing_address[company]': u'', 'billing_address[city]': u'Detroit', 'shipping_address[company]': u'', 'billing_address[last_name]': u'Candy', 'shipping_address[address_2]': u'', 'billing_address[address_2]': u''}
    for k,v in shipping_address_data.items():
        print(k)
    cgccli = CgccliController(
        token, file, data, dest)

    if argument[0] == 'projects':
        response = cgccli.make_project_call(argument[1])
    elif argument[0] == 'files':
        response = cgccli.make_project_call(argument[1])

    click.echo(json.dumps(response)) 



if __name__ == "__main__":
    main()
