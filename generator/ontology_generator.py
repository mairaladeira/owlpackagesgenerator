__author__ = 'Maira'
import re
from RDF import RDF
from Notation3 import Notation3
import time
import sys


def process_package(package):
    package = re.sub('\n +', ' ', package)
    packs = package.split('\n')
    packages_data = dict()
    wanted_properties = ['Version',
                         'Architecture',
                         'Recommends',
                         'Section',
                         'Package',
                         'Priority',
                         'Maintainer',
                         'Suggests',
                         'Description',
                         'Depends',
                         'Replaces',
                         'Conflicts',
                         'Provides',
                         'Breaks']
    for pac in packs:
        t1 = re.split('\n*:', pac)
        if len(t1) > 1 and t1[0] in wanted_properties:
            packages_data[t1[0]] = t1[1].strip()
    return packages_data


def read_package(f_obj):
    print('reading packages file...')
    content = f_obj.read()
    f_obj.close()
    packages = content.split('\n\n')
    packages_d = dict()
    print('processing packages...')
    for p in packages:
        d = process_package(p)
        if len(d) > 1:
            packages_d[d['Package']] = d
    return packages_d


def create_packages_instances(f_obj, owl_obj, t, limit):
    pkgs = read_package(f_obj)
    print(str(len(pkgs))+' packages generated')
    print('creating ontology instances...')
    maintainers = dict()
    architectures = set()
    i = 1
    packages = set()
    used_packages = set()
    for p in pkgs:
        if i < limit:
            print('processing pack: '+str(i))
            i += 1
            packages.add(p)
            package_properties = []
            p_content = pkgs[p]
            p_type = ['debianPackage']
            if 'Maintainer' in p_content:
                maintainers_list = format_maintainer(p_content['Maintainer'])
                debian_community = True
                if t == 'n3':
                    package_maintainers = []
                for m in maintainers_list:
                    m_name = m[0]
                    m_email = m[1]
                    if not re.search('debian(.+?)team', m_name.lower()) and not re.search('debian', m_email.lower()):
                        debian_community = False
                    else:
                        m_name = 'Debian Community'
                        debian_community = False
                    if t == 'n3':
                        package_maintainers.append(m_name)
                    if m_name not in maintainers:
                        maintainers[m_name] = set()
                        if m_email != '':
                            maintainers[m_name].add(m_email)
                    elif m_email != '':
                        maintainers[m_name].add(m_email)
                    if t == 'rdf':
                        package_properties.append(['hasMaintainer', 'resource', m_name])
                if debian_community:
                    p_type.append('debianCommunity')
                if t == 'n3':
                    package_properties.append(['hasMaintainer', 'resource', package_maintainers])
            if 'Architecture' in p_content:
                architectures.add(p_content['Architecture'])
                if t == 'rdf':
                    arch = p_content['Architecture']
                else:
                    arch = [p_content['Architecture']]
                package_properties.append(['hasArchitecture', 'resource', arch])
            if 'Description' in p_content:
                test = re.search('window(.+?)manager', p_content['Description'].lower())
                if test:
                    #p_type.append('windowManager')
                    p_content['Description'] = 'Window Manager'
                    print('----------------')
                    print(p)
                    print('----------------')
                if t == 'rdf':
                    desc = p_content['Description']
                else:
                    desc = [p_content['Description']]
                package_properties.append(['description', 'datatype', desc, 'string'])
            if 'Version' in p_content:
                if t == 'rdf':
                    ver = p_content['Version']
                else:
                    ver = [p_content['Version']]
                package_properties.append(['version', 'datatype', ver, 'string'])
            if 'Conflicts' in p_content:
                conflicts = get_content(p_content['Conflicts'])
                if t == 'n3':
                    package_properties.append(['conflicts', 'resource', conflicts])
                for c in conflicts:
                    if t == 'rdf':
                        package_properties.append(['conflicts', 'resource', c])
                    used_packages.add(c)
            if 'Depends' in p_content:
                depends = get_content(p_content['Depends'])
                if t == 'n3':
                    package_properties.append(['depends', 'resource', depends])
                for d in depends:
                    if t == 'rdf':
                        package_properties.append(['depends', 'resource', d])
                    used_packages.add(d)
            if 'Provides' in p_content:
                provides = get_content(p_content['Provides'])
                if t == 'n3':
                    package_properties.append(['provides', 'resource', provides])
                for pr in provides:
                    if t == 'rdf':
                        package_properties.append(['provides', 'resource', pr])
                    used_packages.add(pr)
            if 'Recommends' in p_content:
                recommends = get_content(p_content['Recommends'])
                if t == 'n3':
                    package_properties.append(['recommends', 'resource', recommends])
                for r in recommends:
                    if t == 'rdf':
                        package_properties.append(['recommends', 'resource', r])
                    used_packages.add(r)
            if 'Suggests' in p_content:
                suggests = get_content(p_content['Suggests'])
                if t == 'n3':
                    package_properties.append(['suggests', 'resource', suggests])
                for s in suggests:
                    if t == 'rdf':
                        package_properties.append(['suggests', 'resource', s])
                    used_packages.add(s)
            if len(p_type) > 1:
                p_type.remove('debianPackage')
            for pt in p_type:
                owl_obj.new_named_individual(p, pt, package_properties)
        else:
            break

    for a in architectures:
        owl_obj.new_named_individual(a, 'architecture', [])
    print(str(len(used_packages))+' used packages')
    print(str(len(packages))+' declared packages')
    for p in used_packages:
        if p not in packages:
            package_properties = []
            p_type = ['debianPackage']
            try:
                p_content = pkgs[p]
                if 'Maintainer' in p_content:
                    maintainers_list = format_maintainer(p_content['Maintainer'])
                    debian_community = True
                    if t == 'n3':
                        package_maintainers = []
                    for m in maintainers_list:
                        m_name = m[0]
                        m_email = m[1]
                        if not re.search('debian(.+?)team', m_name.lower()) and not re.search('debian', m_email.lower()):
                            debian_community = False
                        else:
                            m_name = 'Debian Community'
                            debian_community = False
                        if t == 'n3':
                            package_maintainers.append(m_name)
                        if m_name not in maintainers:
                            maintainers[m_name] = set()
                            if m_email != '':
                                maintainers[m_name].add(m_email)
                        elif m_email != '':
                            maintainers[m_name].add(m_email)
                        if t == 'rdf':
                            package_properties.append(['hasMaintainer', 'resource', m_name])
                    if debian_community:
                        p_type.append('debianCommunity')
                    if t == 'n3':
                        package_properties.append(['hasMaintainer', 'resource', package_maintainers])
                architectures.add(p_content['Architecture'])
                if t == 'rdf':
                    arch = p_content['Architecture']
                else:
                    arch = [p_content['Architecture']]
                package_properties.append(['hasArchitecture', 'resource', arch])
                wm = re.search('window(.+?)manager', p_content['Description'].lower())
                if wm:
                    #p_type.append('windowManager')
                    p_content['Description'] = 'Window Manager'
                    print('----------------')
                    print(p)
                    print('----------------')
                if t == 'rdf':
                    desc = p_content['Description']
                else:
                    desc = [p_content['Description']]
                package_properties.append(['description', 'datatype', desc, 'string'])
                if t == 'rdf':
                    ver = p_content['Version']
                else:
                    ver = [p_content['Version']]
                package_properties.append(['version', 'datatype', ver, 'string'])
            except:
                print('Package '+str(p)+' does not exist!')
                owl_obj.new_named_individual(p, 'debianPackage', package_properties)
                continue
            for pt in p_type:
                owl_obj.new_named_individual(p, pt, package_properties)
    for m in maintainers:
        print('Processing maintainer: '+m)
        maintainers_props = []
        if t == 'rdf':
            for m_email in maintainers[m]:
                maintainers_props.append(['email', 'datatype', m_email, 'string'])
        else:
            if len(maintainers[m]) > 1:
                maintainers_props.append(['email', 'datatype', maintainers[m], 'string'])
        owl_obj.new_named_individual(m, 'maintainer', maintainers_props)


def add_maintainer(maintainer, emails, owl_obj):
    owl_obj.declare_named_individual(maintainer)
    owl_obj.add_class_assertion('maintainer', maintainer)
    for e in emails:
        m_email = e.replace('>', '')
        owl_obj.new_data_property_assertion('email', maintainer, m_email)


def get_content(name):
    names = name.split(',')
    names_list = set()
    for n in names:
        packs_or = n.split('|')
        for p in packs_or:
            p = p.split('<')
            p = p[0].split('(')
            p = p[0].strip().replace(' ', '_')
            names_list.add(p)
    return names_list


def format_maintainer(maintainer):
    maintainers_list = []
    maintainers = maintainer.split(',')
    if len(maintainers) == 1:
        maintainers = maintainers[0].split('|')
    for maintainer in maintainers:
        m = maintainer.split('<')
        m_name = m[0].split('(')
        m_name = m_name[0].strip()
        if len(m) > 1:
            m_email = m[1].replace('>', '')
        else:
            m_email = ''
        maintainers_list.append([m_name, m_email])
    return maintainers_list


def main(f_obj, file_type, result_file, l=100000000):
    start_time = time.time()
    if file_type == 1:
        rdf_structure = RDF(result_file, result_file+'.owl')
        create_packages_instances(f_obj, rdf_structure, 'rdf', l)
        rdf_structure.end_rdf()
    elif file_type == 2:
        n3_structure = Notation3(result_file, result_file+'.ttl')
        create_packages_instances(f_obj, n3_structure, 'n3', l)
        n3_structure.end_notation3()
    print("--- %s seconds ---" % (time.time() - start_time))

if __name__ == "__main__":
    limit = 100000000
    if len(sys.argv) == 1:
        print('-----------------------------------------------------------------')
        print('-----------------------------------------------------------------')
        print(' Welcome to the Ontology package\'s generator.')
        print(' Please inform the name of your Packages\' file with its path.')
        print(' It is really important to have the correct path for your file.')
        file_path = input(" Packages' file: ")
        correct_file = False
        while not correct_file:
            try:
                f = open(file_path)
                correct_file = True
            except:
                print(' File not found! Try again!')
                file_path = input(" Path to the file:\n")
        print(' What type of owl file do you want to generate? 1 - RDF, 2 - Notation 3 (turtle)')
        f_type = input(" Type of file: ")
        correct_type = False
        while not correct_type:
            try:
                if int(f_type) == 1 or int(f_type) == 2:
                    correct_type = True
                else:
                    print(' File type not available! Possible options: 1 - RDF, 2 - Notation 3 (turtle). Try Again..')
                    f_type = input(" Type of file: ")
            except:
                print(' File type not available! Possible options: 1 - RDF, 2 - Notation 3 (turtle). Try Again..')
                f_type = input(" Type of file: ")

        output_file = input(' Name of output file (the extension will be generated automatically): ')
        print('-----------------------------------------------------------------')
        print('-----------------------------------------------------------------')
    else:
        args = sys.argv
        if args[1] != '-p' or args[3] != '-t' or args[5] != '-o':
            print(' Wrong arguments instantiation.')
            print(' Correct use: python ontology_generator.py -p <Packages_file> -t <rdf_or_n3> -o <Output_file> -l <Limit_of_Packages>')
            sys.exit()
        try:
            f = open(args[2])
        except:
            print(' Packages file not found! Check if the path is correct.')
            sys.exit()
        if args[4].lower() == 'rdf':
            f_type = 1
        elif args[4].lower() == 'n3':
            f_type = 2
        else:
            print(' Wrong type for output file! Possible values: rdf or n3.')
            sys.exit()
        try:
            output_file = args[6]
        except:
            print(' Output file is mandatory!')
            print(' Correct use: python ontology_generator.py -p <Packages_file> -t <rdf_or_n3> -o <Output_file>')
            sys.exit()
        if '-l' in args:

            l_index = args.index('-l')+1
            limit = args[l_index]
    main(f, int(f_type), output_file, limit)