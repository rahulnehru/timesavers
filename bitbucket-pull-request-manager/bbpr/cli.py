import os
from .bbpr import check_status
import getpass
import click

@click.command()
@click.option('--username', prompt=True, help='Your LDAP username')
@click.option('--password', prompt=True, hide_input=True, help='Your LDAP password')
def main(username, password):
    check_status((username, password))

