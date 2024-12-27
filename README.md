# OpenLDAP Examples

## exec into container
```shell
docker exec -it ldap /bin/bash
```
## Interact with LDAP

### Create OUs (orgainaization Units).

Create a devops OU
```shell
ldapadd -x -w admin -D "cn=admin,dc=example,dc=in" << EOF
# LDIF file to add organizational unit "ou=devops" under "dc=example,dc=in"
dn: ou=devops,dc=example,dc=in
objectClass: organizationalUnit
ou: devops

EOF
```

Create an appdev OU
```shell
# LDIF file to add organizational unit "ou=appdev" under "dc=example,dc=in"
ldapadd -x -w admin -D "cn=admin,dc=example,dc=in" << EOF
dn: ou=appdev,dc=example,dc=in
objectClass: organizationalUnit
ou: appdev

EOF
```


### Create User accounts.

Create my account
```shell
ldapadd -x -w admin -D "cn=admin,dc=example,dc=in" << EOF
# LDIF file to Create user "ltratcliff" in "ou=appdev" under "dc=example,dc=in"
dn: cn=ltratcliff,ou=devops,dc=example,dc=in
objectClass: iNetOrgPerson
objectClass: person
cn: Tom
uid: larry.t.ratcliff.ctr
givenName: Larry
sn: Ratcliff
mail: larry.t.ratcliff.ctr@socom.mil
userPassword: Password1

EOF
```

Create co-workers account
```shell
# LDIF file to Create user "dave" in "ou=devops" under "dc=example,dc=in"
ldapadd -x -w admin -D "cn=admin,dc=example,dc=in" << EOF
dn: cn=dave,ou=devops,dc=example,dc=in
objectClass: inetOrgPerson
cn: dave
sn: Dave
userPassword: Dave@123
```


### Create Groups
```shell
ldapadd -x -w admin -D "cn=admin,dc=example,dc=in" << EOF
# Group: appdev-team
dn: cn=appdev-team,dc=example,dc=in
objectClass: top
objectClass: groupOfNames
cn: appdev-team
description: App Development Team
member: cn=ltratcliff,ou=appdev,dc=example,dc=in
member: cn=dave,ou=devops,dc=example,dc=in

# Group: devops-team
dn: cn=devops-team,dc=example,dc=in
objectClass: top
objectClass: groupOfNames
cn: devops-team
description: DevOps Team
member: cn=dave,ou=devops,dc=example,dc=in
EOF
```


### Modify and apply MemberOf attribute to Users in Groups.
```shell
ldapadd -x -w admin -D "cn=admin,dc=example,dc=in" << EOF
dn: cn=ltratcliff,ou=appdev,dc=example,dc=in
changetype: modify
add: memberOf
memberOf: cn=devops-team,dc=example,dc=in

EOF
```



## Search

### Search from ldapsearch
```shell
ldapsearch -x -b dc=example,dc=in -D "cn=admin,dc=example,dc=in" -w admin -s sub "objectclass=*"
```

### Search from python
```python
from ldap3 import Server, Connection, ALL

server = Server('localhost', get_info=ALL)
dn = "cn=ltratcliff, ou=devops, dc=example, dc=in"
conn = Connection(server, dn, password='Password1', auto_bind=True)

#conn.search('dc=example,dc=in', '(cn=*)', attributes=['*'])
conn.search('dc=example,dc=in', '(cn=ltratcliff)', attributes=['*'])

for entry in conn.entries:
    print(entry)
```

## Modify ACLs
Check oclAccess permission.
```shell
ldapsearch -Y EXTERNAL -Q -H ldapi:/// -LLL -o ldif-wrap=no -b cn=config '(objectClass=olcDatabaseConfig)' olcAccess
```

Modification to grant read access to the user "ltratcliff"
```shell
ldapmodify -H ldapi:/// -Y EXTERNAL << EOF
dn: olcDatabase={1}mdb,cn=config
changetype: modify
add: olcAccess
olcAccess: {2}to * by dn="cn=ltratcliff,ou=devops,dc=example,dc=in" read
EOF
```
