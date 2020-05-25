#!/usr/bin/env python3
import click
import hvac
import os
import json
import pprint
import sys
import requests

client = hvac.Client()

def print_dict_to_console(dict): 
    for key in dict:
        print(key, ':\n\t', dict[key], '\n')

def print_arr_to_console(arr): 
    for key in arr:
        print(key)

def print_dict_to_json_file(path, data):
    file_name = path.replace('/', '-') + '.json'
    file = open(file_name, "w")
    file.write(json.dumps(data, ensure_ascii=False))
    file.close()
    print('Secrets written to file', file_name)

def forbidden_access_to_path(path):
    print('Forbidden access to path', path) 

def invalid_path(path):
    print('Invalid path at', path)

def fetch_read_values(path):
    return client.secrets.kv.v1.read_secret(path=path, mount_point='')['data']    

@click.group()
def cli():
    pass

@click.command(help = 'Authenticate with Vault using LDAP')
@click.option('--username', prompt=True, help='Your LDAP username')
@click.option('--password', prompt=True, hide_input=True, help='Your LDAP password')
def auth(username, password):
    try:
        token = client.auth.ldap.login(
            username=username,
            password=password,
            mount_point='ldap'
        )['auth']['client_token']
        home_path = os.environ['HOME']
        token_helper = open(home_path + '/.vault-token', "w")
        token_helper.write(token)
        token_helper.close()
        print('Login succeeded!')
    except ConnectionError:
        print('Check your vault address is exported!')
    except hvac.exceptions.Forbidden:
        print('Credentials incorrect!')


@click.command(help = "Read secret from a Vault path")
@click.argument('--path')
@click.option('--output', default='console', help='Either `file` or `console`')
def read(path, output):
    if output != 'console' and output != 'file': 
        print('Invalid output format specified [', output,']. Must be `file` or console`')
        sys.exit()
    try:
        secret = fetch_read_values(path)
        if output == 'console': 
            print_dict_to_console(secret)
        if output == 'file':
            print_dict_to_json_file(path, secret)    
    except hvac.exceptions.InvalidPath:
        invalid_path(path)
    except hvac.exceptions.Forbidden:
        forbidden_access_to_path(path)
    except ConnectionError:
        print('Check your vault address is exported!')

@click.command(help = "List secrets in a Vault path")
@click.option('--path', help = 'Path you wish to list')
def list(path):
    try:
        secret = client.secrets.kv.v1.list_secrets(path=path,mount_point='')['data']['keys']
        print_arr_to_console(secret)
    except hvac.exceptions.InvalidPath: 
        invalid_path(path)
    except hvac.exceptions.Forbidden:
        forbidden_access_to_path(path)
    except ConnectionError:
        print('Check your vault address is exported!')

def fetch_level_data(path):
    keys = client.secrets.kv.v1.list_secrets(path=path,mount_point='')['data']['keys']
    data = {}
    for key in keys:
        if '/' not in key:
            data[key] = fetch_read_values(path+'/'+key)
        else:
            fetch_level_data(path + '/' + key)         
    return data        

@click.command(help = "Take a snapshot of all the secrets in a Vault path to a JSON file")
@click.option('--path', help='Path you wish to save a snapshot of')
def snapshot(path):
    try:
        data = fetch_level_data(path) 
        print_dict_to_json_file(path, data)
    except hvac.exceptions.InvalidPath: 
        invalid_path(path)
    except hvac.exceptions.Forbidden:
        forbidden_access_to_path(path)
    except ConnectionError:
        print('Check your vault address is exported!')

@click.command(help = "Delete a secret from Vault")
@click.option('--path', help = 'Path of secrets you want to delete')
def delete(path):
    try:
        read_secret = fetch_read_values(path)
        print('Deleting the following secrets from path',path)
        print_dict_to_console(read_secret)
        delete = str(input('Do you wish to continue? (Only `Yes` will trigger the delete)\n'))
        if delete == 'Yes' :
            client.secrets.kv.v1.delete_secret(path=path,mount_point='',)
            print('Deleted secret at path', path)
        else:
            print('Quitting')
    except hvac.exceptions.InvalidPath: 
        invalid_path(path)
    except hvac.exceptions.Forbidden:
        forbidden_access_to_path(path)            
    except ConnectionError:
        print('Check your vault address is exported!')

def update(path, data, key, value):
    data[key] = value
    client.secrets.kv.v1.create_or_update_secret(path=path,mount_point='',secret=data,)
    print('Done')


def parse_json_file(file):
    try:
        return json.loads(open(file, 'r').read())
    except FileNotFoundError:
        print('File not found')
        sys.exit() 
    except json.decoder.JSONDecodeError:
        print('File does not contain valid JSON')
        sys.exit()    
    except ConnectionError:
        print('Check your vault address is exported!')

@click.command(help = "Update or create a key in a Vault secret")
@click.option('--path', help="Path of the secret to patch")
@click.option('--key', default = 'value', help="Key of the secret, defaults to `value`")
@click.option('--value', default = None, help="Value of the secret")
@click.option('--file', default = None, help="Path of JSON file containing the value of the secret (useful for large values)")
def patch(path, key, value, file):
    data = None
    if (value != None and value != None) or (value == None and file == None):
        print('You must specify either --file or --value')
        sys.exit()
    elif value != None:
        data = value
    elif file != None:
        data = parse_json_file(file)
    else:
        data = value
    try:
        read_data = fetch_read_values(path)
        try:
            existing = read_data[key]
        except KeyError:
            existing = None            
        if existing != None:
            print('Key', key, 'already exists with value:\n\t', existing)
            overwrite = str(input('Overwrite? (Only `Yes` will update)\n'))
            if overwrite == 'Yes':
                update(path, read_data, key, data)        
            else:
                print('Quitting')
        else:
            update(path, read_data, key, data)        
    except hvac.exceptions.InvalidPath: 
        invalid_path(path)
        print('Try running $volt write')
    except hvac.exceptions.Forbidden:
        forbidden_access_to_path(path)                
    except ConnectionError:
        print('Check your vault address is exported!')


def put(path, secret):
    try:
        client.secrets.kv.v1.create_or_update_secret(path=path, secret=secret, mount_point = '',)
        print('Done')
    except hvac.exceptions.InvalidPath: 
        invalid_path(path)
    except hvac.exceptions.Forbidden:
        forbidden_access_to_path(path)
    except ConnectionError:
        print('Check your vault address is exported!')

def could_not_connect():
    print("Could not connect to Vault")

@click.command(help = "Create a new Vault secret")
@click.option('--path', help = "Path of the secret to write")
@click.option('--file', default = None, help = "Path of JSON file containing data to write (useful if more than one secret is being written)")
@click.option('--key', default = 'value', help = "Key of the secret to write, defaults to `value`")
@click.option('--value', default = None, help = "Value of the secret to write")
def write(path, file, key, value):
    secret = None
    if file != None and value != None:
        print('--file flag cannot be used either --key or --value')
        sys.exit()
    elif file != None:
        secret = parse_json_file(file)
        put(path, secret)
    elif value == None:
        print('You must specify either a --file or a --value')
        sys.exit()
    else:
        secret = {key: value}    
        put(path, secret)
                   




def main():
    cli.add_command(delete)
    cli.add_command(auth)    
    cli.add_command(read)
    cli.add_command(list)
    cli.add_command(snapshot)
    cli.add_command(patch)
    cli.add_command(write)
    return cli()
    
