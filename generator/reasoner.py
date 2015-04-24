import os
import platform
import re
import sys


__author__ = 'Maira'


def parser_pack_name(pack):
    pack = pack.split('(')
    pack = pack[0].split('<')
    pack = pack[0].split('|')
    pack = pack[0].replace('/', '_or_').replace('+', '_').replace('>', '').replace('"', '').replace("'", "") \
                  .replace('~', '').replace('.', '_').strip().replace(' ', '_').replace('&', '_and_')
    return pack


def get_query(t, packs=''):
    query = 'PREFIX url: <'+url+'>\n'
    f_name = ''
    if t == 'debian_community':
        query += 'SELECT ?debian_community_packages\n'
        query += 'WHERE {\n'
        query += '\t?debian_community_packages a url:debianCommunity.\n'
        query += '}'
        f_name = 'query_temp_debian_community'
    elif t == 'window_manager':
        query += 'SELECT ?window_manager_packages\n'
        query += 'WHERE {\n'
        query += '\t?window_manager_packages a url:windowManager.\n'
        query += '}'
        f_name = 'query_temp_window_manager'
    elif t == 'conflicts_single_pack':
        p_name = parser_pack_name(packs)
        query += 'SELECT ?conflicts\n'
        query += 'WHERE {\n'
        query += '\turl:'+p_name+' a url:debianPackage.\n'
        query += '\turl:'+p_name+' url:conflicts ?conflicts.\n'
        query += '}'
        f_name = 'query_temp_conflicts'
    elif t == 'pack_dependencies':
        p_name = parser_pack_name(packs)
        query += 'SELECT ?dependencies\n'
        query += 'WHERE {\n'
        query += '\t?dependencies a url:debianPackage.\n'
        query += '\turl:'+p_name+' url:depends ?dependencies.\n'
        query += '}'
        f_name = 'query_temp_depends'
    elif t == 'pack_suggestions':
        p_name = parser_pack_name(packs)
        query += 'SELECT ?suggestions\n'
        query += 'WHERE {\n'
        query += '\turl:'+p_name+' a url:debianPackage.\n'
        query += '\turl:'+p_name+' url:suggests ?suggestions.\n'
        query += '}'
        f_name = 'query_temp_suggests'
    elif t == 'pack_recommendations':
        p_name = parser_pack_name(packs)
        query += 'SELECT ?recommendations\n'
        query += 'WHERE {\n'
        query += '\turl:'+p_name+' a url:debianPackage.\n'
        query += '\turl:'+p_name+' url:recommends ?recommendations.\n'
        query += '}'
        f_name = 'query_temp_recommends'
    elif t == 'pack_provides':
        p_name = parser_pack_name(packs)
        query += 'SELECT ?provided_packages\n'
        query += 'WHERE {\n'
        query += '\turl:'+p_name+' a url:debianPackage.\n'
        query += '\turl:'+p_name+' url:provides ?provided_packages.\n'
        query += '}'
        f_name = 'query_temp_provides'
    elif t == 'conflicts_list_of_packs':
        packs = packs.split(',')
        packs_list = []
        for p_name in packs:
            p_name = parser_pack_name(p_name)
            packs_list.append('url:'+p_name)
        packs = ', '.join(packs_list)
        query += 'SELECT DISTINCT ?pack1 ?pack2\n'
        query += 'WHERE {\n'
        query += '\t?pack1 a url:debianPackage.\n'
        query += '\t?pack2 a url:debianPackage.\n'
        query += '\t?pack1 url:conflicts ?pack2.\n'
        query += '\tFILTER(?pack1 in ('+packs+') && ?pack2 in ('+packs+')).\n'
        query += '}'
        f_name = 'query_temp_conflict_multiple'
    query_file = open(f_name, 'w+')
    query_file.write(query)
    query_file.close()
    return f_name

file_path = os.path.abspath(os.path.dirname(__file__))
path = file_path+'/pellet-2.3.1'
query_type = ''
if len(sys.argv) == 1:
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
    print(' 4) Get the list of DEPENDENCIES of a package')
    print(' 5) Get the SUGGESTIONS of a given package')
    print(' 6) Get the RECOMMENDATIONS of a given package')
    print(' 7) Get the packages PROVIDED by a given package')
    print(' 8) Get the list of the conflicts given a list of packages to install')
    action = input(' Option: ')
    correct_action = False
    while not correct_action:
        action = int(action)
        if action < 1 or action > 8:
            print(' Invalid option! Your answer should be between 1 and 8.')
            action = input(' Option: ')
        else:
            correct_action = True
            packs_var = ''
            if action == 1:
                query_type = 'debian_community'
            elif action == 2:
                query_type = 'window_manager'
            elif action == 3:
                query_type = 'conflicts_single_pack'
                packs_var = input(' Package to extract the Conflicts from: ')
            elif action == 4:
                query_type = 'pack_dependencies'
                packs_var = input(' Package to extract the Dependencies from: ')
            elif action == 5:
                query_type = 'pack_suggestions'
                packs_var = input(' Package to extract the Suggestions from: ')
            elif action == 6:
                query_type = 'pack_recommendations'
                packs_var = input(' Package to extract the Recommendations from: ')
            elif action == 7:
                query_type = 'pack_provides'
                packs_var = input(' Package to extract the provided packages from: ')
            elif action == 8:
                query_type = 'conflicts_list_of_packs'
                packs_var = input(' Give the list of packages to extract the conflicts from separated by ,: ')
            query_file_name = get_query(query_type, packs_var)
    output_file = input(' Output file: ')
else:
    args = sys.argv
    correct_use = 'python reasoner.py -of <ontology_file> -q <query_type> -qo <query_options> -ot <output_file>'
    help_command = 'python reasoner.py -h'
    if ('-of' not in args or '-q' not in args or '-ot' not in args) and ('-h' not in args):
        print('Wrong arguments instantiation: '+correct_use)
        sys.exit()
    if '-h' in args:
        print(' Usage: '+correct_use)
        print(' \t-of: ontology_file (with extension .owl or .ttl)')
        print(' \t-q: query_type: should have one of these values: ')
        print(' \t\t\t- debian_community,')
        print(' \t\t\t- window_manager,')
        print(' \t\t\t- conflicts_single_pack,')
        print(' \t\t\t- pack_dependencies,')
        print(' \t\t\t- pack_suggestions,')
        print(' \t\t\t- pack_recommendations,')
        print(' \t\t\t- pack_provides,')
        print(' \t\t\t- conflicts_list_of_packs')
        print(' \t-qo: query_options:')
        print(' \t\t\t- If query_type is debian_community or window_manager this option is not needed.')
        print(' \t\t\t- If query_type is conflicts_single_pack, depends_on_pack, suggests_pack or pack_provides')
        print(' \t\t\t  this option should be one package name.')
        print(' \t\t\t- If query_type is conflicts_list_of_packs this option should be a list of packages separated by comma')
        print(' \t-ot: output_file: the name of the output file')
        sys.exit()
    of_index = args.index('-of')
    ontology_file = args[of_index+1]
    ot_index = args.index('-ot')
    output_file = args[ot_index+1]
    url = ''
    query_file_name = ''
    onto_type = ''
    f = open(ontology_file.strip())
    for i, line in enumerate(f):
        if i == 0 and '@prefix' not in line and '<?xml version="1.0"?>' not in line:
            break
        if '@prefix' in line:
            pattern = re.compile(r'<(.+?)>', flags=re.DOTALL)
            results = pattern.findall(line)
            url = results[0]
            onto_type = 'Turtle'
            break
        elif '<!ENTITY '+ontology_file.strip().replace('.owl', '') in line:
            pattern = re.compile(r'\"(.+?)\"', flags=re.DOTALL)
            results = pattern.findall(line)
            url = results[0]
            onto_type = 'RDF/XML'
            break
    if url == '':
        print(' Problem with the ontology file. It was not possible to determine the '
              ' ontology URL. Please check the file (-of option).')
        sys.exit()
    q_index = args.index('-q')
    query_type = args[q_index+1]
    query = 'PREFIX url: <'+url+'>\n'
    possible_types = ['debian_community',
                      'window_manager',
                      'conflicts_single_pack',
                      'pack_dependencies',
                      'pack_suggestions',
                      'pack_recommendations',
                      'pack_provides',
                      'conflicts_list_of_packs']
    if query_type not in possible_types:
        print('Incorrect query type (-q option)! Use -h for help.')
        sys.exit()
    elif query_type not in ('debian_community', 'window_manager'):
        if '-qo' not in args:
            print('-qo parameter queried! Use -h for help')
            sys.exit()
        qo_index = args.index('-qo')
        query_option = args[qo_index+1]
        query_file_name = get_query(query_type, query_option)
    else:
        query_file_name = get_query(query_type, '')
    r_file = ontology_file
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
    #os.system('clear')
    f = open(file_path+"/"+output_file, 'r')
    output = ''
    result_packs = []
    for i, l in enumerate(f):
        output += l
    print(output)
    f.close()
except OSError as e:
    print(e)