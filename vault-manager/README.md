## Volt

### Overview 

A better Vault client with safety included.

### Usage

#### Read
Read will by default print the secrets to console.
```
$ volt read secret/path --output file
```
It is possible to write the secrets to a JSON file by specifying `--output file`.
```
$ volt read secret/path --output file
```

#### List
List will print the secrets under a given Vault path.
```
$ volt list secret/path/
```

#### Auth
Volt lets you authenticate with Vault using LDAP.
```
$ volt auth
    Username: user.name
    Password:
```

#### Snapshot
Volt allows you to take a snapshot of all secrets and subpaths under a given Vault path. 
```
$ volt snapshot secret/foo/bar
```
The file will be created with the name `secret-foo-bar.json` in the current working directory.

#### Patch
Volt allows you to update or create a key-value pair in an existing secret. If a key-value pair already exists with that key, Volt gives you a warning.  
```
$ volt patch secret/foo/bar --key application.secret --value changeme 
```

For particularly large values, such as keys, encoded certificates etc. it is advised that you use JSON files.
```
$ volt patch secret/foo/bar --file data.json
```

#### Delete
Volt gives you the ability to delete secrets from Vault. It will print the current secret and warn you before changes are made to the server.
```
$ volt delete secret/foo/bar
```

#### Write 
Volt gives you the ability to create secrets in Vault. If your secret only contains one key-value pair, you might want to use the following command.

For keys or values containing special characters, you can enclose these in `''`.
```
$ volt write secret/foo/bar --key application.secret --value changeme
```

For creating secrets with multiple key-value pairs, or encoded certificates, keys etc. it is recommeded that you use files such as the following:
```json 
{
    "application.secret": "changeme",
    "certificate_chain": "SEVMTE8gSSBBTSBBIENFUlRJRklDQVRF"
}
```
JSON files can be written into Vault using:
```
$ volt write secret/foo/bar --file data.json
```