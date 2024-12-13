from ldap3 import Server, Connection, ALL

# Define the server and the connection
server = Server('localhost', get_info=ALL)
#conn = Connection(server, user='ltratcliff', password='Password1', auto_bind=True)
dn = "cn=ltratcliff, ou=devops, dc=example, dc=in"
conn = Connection(server, dn, password='Password1', auto_bind=True)

who = input("Who are you looking for: ")

# Perform the search
#conn.search('dc=devops,dc=example,dc=in', '(objectClass=person)', attributes=['*'])
#conn.search('dc=example,dc=in', '(cn=*)', attributes=['*'])
#conn.search('dc=example,dc=in', '(cn=ltratcliff)', attributes=['*'])
conn.search('ou=devops,dc=example,dc=in', f'(sn={who})', attributes=['*'])


# Print the results
for entry in conn.entries:
    print(entry)

