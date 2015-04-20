import os
import platform
import re


__author__ = 'Maira'
file_path = os.path.abspath(os.path.dirname(__file__))
path = file_path+'/pellet-2.3.1'
print('----------------------------------------------------------------------------')
print(' Welcome to the reasoner! We are using the pellet reasoner, version 2.3.1\n\n')
print(' IMPORTANT: This project assume that the namespace of the ontology is the file name\n\n')
r_file = input(' File to reasoner on (must be an RDF(.owl) or Notation 3(.ttl) file): ')
correct_file = False
url = ''
onto_type = ''
query_file_name = ''
while not correct_file:
    try:
        f = open(r_file.strip())
        for i, line in enumerate(f):
            if i == 0 and '@prefix' not in line and '<?xml version="1.0"?>' not in line:
                break
            if '@prefix' in line:
                pattern = re.compile(r'<(.+?)>', flags=re.DOTALL)
                results = pattern.findall(line)
                url = results[0]
                correct_file = True
                onto_type = 'Turtle'
                break
            elif '<!ENTITY '+r_file.strip().replace('.owl', '') in line:
                pattern = re.compile(r'\"(.+?)\"', flags=re.DOTALL)
                results = pattern.findall(line)
                url = results[0]
                onto_type = 'RDF/XML'
                correct_file = True
                break
        if url == '':
            print(' Problem with the ontology file. It was not possible to determine the '
                  ' ontology URL. Please check the file and try again!')
            print(' The file should be of the type RDF or Notation 3!')
            r_file = input(' File to reasoner on: ')
    except Exception as e:
        print(e)
        print(' File not found! Make sure that the file is on the same directory of the script!')
        r_file = input(' File to reasoner on (must be an RDF or Notation 3 file): ')

print('\n\n Select the desired reasoner:')
print(' 1) Get the packages from the DEBIAN COMMUNITY type')
print(' 2) Get the packages from the WINDOW MANAGER type')
print(' 3) Get the CONFLICTS of a given package')
print(' 4) Get the list of packages that DEPENDS of a given package')
print(' 5) Get the SUGGESTIONS of a given package')
print(' 6) Get the RECOMMENDATIONS of a given package')
print(' 7) Get the packages PROVIDED by a given package')
print(' 8) Get the list of the conflicts given a list of packages to install')
action = input(' Option: ')
correct_action = False
while not correct_action:
    action = int(action)
    query = 'PREFIX url: <'+url+'>\n'
    if action == 1:
        correct_action = True
        query += 'SELECT ?debian_community_packages\n'
        query += 'WHERE {\n'
        query += '\t?debian_community_packages a url:debianCommunity.\n'
        query += '}'
        query_file = open('query_temp_debian_community', 'w+')
        query_file_name = 'query_temp_debian_community'
        query_file.write(query)
        query_file.close()
    elif action == 2:
        correct_action = True
        query += 'SELECT ?window_manager_packages\n'
        query += 'WHERE {\n'
        query += '\t?window_manager_packages a url:windowManager.\n'
        query += '}'
        query_file = open('query_temp_window_manager', 'w+')
        query_file_name = 'query_temp_window_manager'
        query_file.write(query)
        query_file.close()
    elif action == 3:
        pack = input(' Package to extract the Conflicts from: ')
        pack = pack.split('(')
        pack = pack[0].split('<')
        pack = pack[0].split('|')
        pack = pack[0].replace('/', '_or_').replace('+', '_').replace('>', '').replace('"', '').replace("'", "") \
                      .replace('~', '').replace('.', '_').strip().replace(' ', '_').replace('&', '_and_')
        query += 'SELECT ?conflicts\n'
        query += 'WHERE {\n'
        query += '\turl:'+pack+' a url:debianPackage.\n'
        query += '\turl:'+pack+' url:conflicts ?conflicts.\n'
        query += '}'
        query_file = open('query_temp_conflicts', 'w+')
        query_file_name = 'query_temp_conflicts'
        query_file.write(query)
        query_file.close()
        correct_action = True
    elif action == 4:
        pack = input(' Package to extract the dependent packages from: ')
        pack = pack.split('(')
        pack = pack[0].split('<')
        pack = pack[0].split('|')
        pack = pack[0].replace('/', '_or_').replace('+', '_').replace('>', '').replace('"', '').replace("'", "") \
                      .replace('~', '').replace('.', '_').strip().replace(' ', '_').replace('&', '_and_')
        query += 'SELECT ?dependents\n'
        query += 'WHERE {\n'
        query += '\t?dependents a url:debianPackage.\n'
        query += '\t?dependents url:depends url:'+pack+'.\n'
        query += '}'
        query_file = open('query_temp_depends', 'w+')
        query_file_name = 'query_temp_depends'
        query_file.write(query)
        query_file.close()
        correct_action = True
    elif action == 5:
        pack = input(' Package to extract the Suggestions from: ')
        pack = pack.split('(')
        pack = pack[0].split('<')
        pack = pack[0].split('|')
        pack = pack[0].replace('/', '_or_').replace('+', '_').replace('>', '').replace('"', '').replace("'", "") \
                      .replace('~', '').replace('.', '_').strip().replace(' ', '_').replace('&', '_and_')
        query += 'SELECT ?suggestions\n'
        query += 'WHERE {\n'
        query += '\turl:'+pack+' a url:debianPackage.\n'
        query += '\turl:'+pack+' url:suggests ?suggestions.\n'
        query += '}'
        query_file = open('query_temp_suggests', 'w+')
        query_file_name = 'query_temp_suggests'
        query_file.write(query)
        query_file.close()
        correct_action = True
    elif action == 6:
        pack = input(' Package to extract the Recommendations from: ')
        pack = pack.split('(')
        pack = pack[0].split('<')
        pack = pack[0].split('|')
        pack = pack[0].replace('/', '_or_').replace('+', '_').replace('>', '').replace('"', '').replace("'", "") \
                      .replace('~', '').replace('.', '_').strip().replace(' ', '_').replace('&', '_and_')
        query += 'SELECT ?recommendations\n'
        query += 'WHERE {\n'
        query += '\turl:'+pack+' a url:debianPackage.\n'
        query += '\turl:'+pack+' url:recommends ?recommendations.\n'
        query += '}'
        query_file = open('query_temp_recommends', 'w+')
        query_file_name = 'query_temp_recommends'
        query_file.write(query)
        query_file.close()
        correct_action = True
    elif action == 7:
        pack = input(' Package to extract the provided packages from: ')
        pack = pack.split('(')
        pack = pack[0].split('<')
        pack = pack[0].split('|')
        pack = pack[0].replace('/', '_or_').replace('+', '_').replace('>', '').replace('"', '').replace("'", "") \
                      .replace('~', '').replace('.', '_').strip().replace(' ', '_').replace('&', '_and_')
        query += 'SELECT ?provided_packages\n'
        query += 'WHERE {\n'
        query += '\turl:'+pack+' a url:debianPackage.\n'
        query += '\turl:'+pack+' url:provides ?provided_packages.\n'
        query += '}'
        query_file = open('query_temp_provides', 'w+')
        query_file_name = 'query_temp_provides'
        query_file.write(query)
        query_file.close()
        correct_action = True
    elif action == 8:
        packs = input(' Give the list of packages to extract the conflicts from separated by ,: ')
        packs = packs.split(',')
        packs_list = []
        for pack in packs:
            pack = pack.split('(')
            pack = pack[0].split('<')
            pack = pack[0].split('|')
            pack = pack[0].replace('/', '_or_').replace('+', '_').replace('>', '').replace('"', '').replace("'", "") \
                          .replace('~', '').replace('.', '_').strip().replace(' ', '_').replace('&', '_and_')
            packs_list.append('url:'+pack)
        packs = ', '.join(packs_list)
        query += 'SELECT ?possible_conflicts\n'
        query += 'WHERE {\n'
        query += '\t?p a url:debianPackage.\n'
        query += '\t?p url:conflicts ?possible_conflicts.\n'
        query += '\tFILTER(?p in ('+packs+')).\n'
        query += '}'
        query_file = open('query_temp_conflict_multiple', 'w+')
        query_file_name = 'query_temp_conflict_multiple'
        query_file.write(query)
        query_file.close()
        correct_action = True

    else:
        print(' Invalid option! Your answer should be between 1 and 8.')
        action = input(' Option: ')
output_file = input(' Output file: ')
try:
    if platform.system() == 'Windows':
        command = "./pellet.bat query -v -input-format "+onto_type+" -q "
        command += file_path+"/"+query_file_name+" "+file_path+"/"+r_file.strip()
        command += " > "+file_path+"/"+output_file
    else:
        command = "./pellet.sh query -v -input-format "+onto_type+" -q "
        command += file_path+"/"+query_file_name+" "+file_path+"/"+r_file.strip()
        command += " > "+file_path+"/"+output_file
    print(' Executing command: '+command)
    print(' Be patient this process takes a while.')
    print('----------------------------------------------------------------------------')
    os.chdir(path)
    os.system(command)
except OSError as e:
    print(e)