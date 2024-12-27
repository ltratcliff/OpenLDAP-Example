# OpenLDAP Examples

## exec into container
```shell
docker exec -it ldap /bin/bash
```

## Create OU (orgainaization Units).
ldapadd -x -w admin -D "cn=admin,dc=example,dc=in" << EOF
# LDIF file to add organizational unit "ou=devops" under "dc=example,dc=in"
dn: ou=devops,dc=example,dc=in
objectClass: organizationalUnit
ou: devops

EOF

# LDIF file to add organizational unit "ou=appdev" under "dc=example,dc=in"
# dn: ou=appdev,dc=example,dc=in
# objectClass: organizationalUnit
# ou: appdev
# EOF

# Create User accounts.
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

# LDIF file to Create user "charlie" in "ou=appdev" under "dc=example,dc=in"
dn: cn=charlie,ou=appdev,dc=example,dc=in
objectClass: inetOrgPerson
cn: charlie
sn: Charlie
userPassword: Charlie@123

# LDIF file to Create user "amit" in "ou=appdev" under "dc=example,dc=in"
dn: cn=amit,ou=appdev,dc=example,dc=in
objectClass: inetOrgPerson
cn: amit
sn: Amit
userPassword: Amit@123
EOF

# Create Groups
ldapadd -x -w admin -D "cn=admin,dc=example,dc=in" << EOF
# Group: appdev-team
dn: cn=appdev-team,dc=example,dc=in
objectClass: top
objectClass: groupOfNames
cn: appdev-team
description: App Development Team
member: cn=ltratcliff,ou=devops,dc=example,dc=in
member: cn=charlie,ou=appdev,dc=example,dc=in

# Group: devops-team
dn: cn=devops-team,dc=example,dc=in
objectClass: top
objectClass: groupOfNames
cn: devops-team
description: DevOps Team
member: cn=amrutha,ou=devops,dc=example,dc=in
member: cn=amit,ou=appdev,dc=example,dc=in
EOF

# Modify and apply MemberOf attribute to Users in Groups.
ldapadd -x -w password -D "cn=admin,dc=example,dc=in" << EOF
dn: cn=amrutha,ou=devops,dc=example,dc=in
changetype: modify
add: memberOf
memberOf: cn=devops-team,dc=example,dc=in

dn: cn=amit,ou=appdev,dc=example,dc=in
changetype: modify
add: memberOf
memberOf: cn=appdev-team,dc=example,dc=in

dn: cn=charile,ou=appdev,dc=example,dc=in
changetype: modify
add: memberOf
memberOf: cn=devops-team,dc=example,dc=in
EOF


### Search
# Searach for users with deafult admin
ldapsearch -x -b dc=example,dc=in -D "cn=admin,dc=example,dc=in" -w admin -s sub "objectclass=*"

### Modify ACLs
# Check oclAccess permission.
ldapsearch -Y EXTERNAL -Q -H ldapi:/// -LLL -o ldif-wrap=no -b cn=config '(objectClass=olcDatabaseConfig)' olcAccess

# Modification to grant read access to the user "ltratcliff"
ldapmodify -H ldapi:/// -Y EXTERNAL << EOF
dn: olcDatabase={1}mdb,cn=config
changetype: modify
add: olcAccess
olcAccess: {2}to * by dn="cn=ltratcliff,ou=devops,dc=example,dc=in" read
EOF

# Searach for perticular user or attributes like cn,sn,groupOfNames and memberOf with Created LDAP admin
ldapsearch -x -D "cn=ltratcliff,ou=devops,dc=example,dc=in" -w Password1 -b "dc=example,dc=in"
