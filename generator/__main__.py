__author__ = 'Maira'
import re
from generator.lib.OWL import OWL
from generator.lib.RDF import RDF
import time


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


def read_package(file):
    print('reading packages file...')
    with open(file) as f:
        content = f.read()
        f.close()
    packages = content.split('\n\n')
    packages_d = dict()
    print('processing packages...')
    for p in packages:
        d = process_package(p)
        if len(d) > 1:
            packages_d[d['Package']] = d
    return packages_d


def create_package_owl_instance(owl_obj):
    pkgs = read_package('Packages')
    print(str(len(pkgs))+' packages generated')
    print('creating ontology instances...')
    maintainers = dict()
    architectures = set()
    i = 1
    packages = set()
    used_packages = set()
    for p in pkgs:
        if i < 100:
            print(i)
            i += 1
            packages.add(p)
            p_content = pkgs[p]
            owl_obj.declare_named_individual(p)
            owl_obj.add_class_assertion('debianPackage', p)
            try:
                if 'Maintainer' in p_content:
                    [m_name, m_email] = format_maintainer(p_content['Maintainer'])
                    owl_obj.new_obj_property_assertion('hasMaintainer', p, m_name)
                    if m_name not in maintainers:
                        maintainers[m_name] = set()
                        if m_email != '':
                            maintainers[m_name].add(m_email)
                    elif m_email != '':
                        maintainers[m_name].add(m_email)
                if 'Architecture' in p_content:
                    architectures.add(p_content['Architecture'])
                    owl_obj.new_obj_property_assertion('hasArchitecture', p, p_content['Architecture'])

                if 'Conflicts' in p_content:
                    conflicts = get_content(p_content['Conflicts'])
                    for c in conflicts:
                        owl_obj.new_obj_property_assertion('conflicts', p, c)
                        used_packages.add(c)
                if 'Depends' in p_content:
                    dependencies = get_content(p_content['Depends'])
                    for dep in dependencies:
                        owl_obj.new_obj_property_assertion('depends', p, dep)
                        used_packages.add(dep)
                if 'Provides' in p_content:
                    provides = get_content(p_content['Provides'])
                    for pr in provides:
                        owl_obj.new_obj_property_assertion('provides', p, pr)
                        used_packages.add(pr)
                if 'Recommends' in p_content:
                    recommends = get_content(p_content['Recommends'])
                    for r in recommends:
                        owl_obj.new_obj_property_assertion('recommends', p, r)
                        used_packages.add(r)
                if 'Suggests' in p_content:
                    suggests = get_content(p_content['Suggests'])
                    for s in suggests:
                        owl_obj.new_obj_property_assertion('suggests', p, s)
                        used_packages.add(s)
                if 'Description' in p_content:
                    owl_obj.new_data_property_assertion('description', p, p_content['Description'])
                if 'Version' in p_content:
                    owl_obj.new_data_property_assertion('version', p, p_content['Version'])
            except Exception as e:
                print(e)
                print('problems')
        else:
            break

    for a in architectures:
        owl_obj.declare_named_individual(a)
        owl_obj.add_class_assertion('architecture', a)
    for p in used_packages:
        if p not in packages:
            owl_obj.declare_named_individual(p)
            owl_obj.add_class_assertion('debianPackage', p)
            try:
                p_content = pkgs[p]
            except:
                print('Package '+str(p)+' does not exist!')
                continue
            if 'Maintainer' in p_content:
                [m_name, m_email] = format_maintainer(p_content['Maintainer'])
                if m_name not in maintainers:
                    maintainers[m_name] = set()
                    if m_email != '':
                        maintainers[m_name].add(m_email)
                elif m_email != '':
                    maintainers[m_name].add(m_email)
                owl_obj.new_obj_property_assertion('hasMaintainer', p, m_name)
                architectures.add(p_content['Architecture'])
                owl_obj.new_obj_property_assertion('hasArchitecture', p, p_content['Architecture'])
                owl_obj.new_data_property_assertion('description', p, p_content['Description'])
                owl_obj.new_data_property_assertion('version', p, p_content['Version'])
    for m in maintainers:
        add_maintainer(m, maintainers[m], owl_obj)


def create_package_rdf_instance(rdf_obj):
    pkgs = read_package('Packages')
    print(str(len(pkgs))+' packages generated')
    print('creating ontology instances...')
    maintainers = dict()
    architectures = set()
    i = 1
    packages = set()
    used_packages = set()
    for p in pkgs:
        if i < 10000000:
            print(i)
            i += 1
            packages.add(p)
            package_properties = []
            p_content = pkgs[p]
            p_type = 'debianPackage'
            if 'Maintainer' in p_content:
                [m_name, m_email] = format_maintainer(p_content['Maintainer'])
                if m_name not in maintainers:
                    maintainers[m_name] = set()
                    if m_email != '':
                        maintainers[m_name].add(m_email)
                elif m_email != '':
                    maintainers[m_name].add(m_email)
                if 'debian' in m_name.lower():
                    p_type = 'debianCommunity'
                package_properties.append(['hasMaintainer', 'resource', m_name])
            if 'Architecture' in p_content:
                architectures.add(p_content['Architecture'])
                package_properties.append(['hasArchitecture', 'resource', p_content['Architecture']])
            if 'Description' in p_content:
                if 'window manager' in p_content['Description'].lower():
                    p_type = 'windowManager'
                package_properties.append(['description', 'datatype', p_content['Description'], 'string'])
            if 'Version' in p_content:
                package_properties.append(['version', 'datatype', p_content['Version'], 'string'])
            if 'Conflicts' in p_content:
                conflicts = get_content(p_content['Conflicts'])
                for c in conflicts:
                    package_properties.append(['conflicts', 'resource', c])
                    used_packages.add(c)
            if 'Depends' in p_content:
                depends = get_content(p_content['Depends'])
                for d in depends:
                    package_properties.append(['depends', 'resource', d])
                    used_packages.add(d)
            if 'Provides' in p_content:
                provides = get_content(p_content['Provides'])
                for pr in provides:
                    package_properties.append(['provides', 'resource', pr])
                    used_packages.add(pr)
            if 'Recommends' in p_content:
                recommends = get_content(p_content['Recommends'])
                for r in recommends:
                    package_properties.append(['recommends', 'resource', r])
                    used_packages.add(r)
            if 'Suggests' in p_content:
                suggests = get_content(p_content['Suggests'])
                for s in suggests:
                    package_properties.append(['suggests', 'resource', s])
                    used_packages.add(s)
            rdf_obj.new_named_individual(p, p_type, package_properties)
        else:
            break

    for a in architectures:
        rdf_obj.new_named_individual(a, 'architecture', [])
    for p in used_packages:
        if p not in packages:
            package_properties = []
            p_type = 'debianPackage'
            try:
                p_content = pkgs[p]
            except:
                print('Package '+str(p)+' does not exist!')
                rdf_obj.new_named_individual(p, 'debianPackage', package_properties)
            if 'Maintainer' in p_content:
                [m_name, m_email] = format_maintainer(p_content['Maintainer'])
                if m_name not in maintainers:
                    maintainers[m_name] = set()
                    if m_email != '':
                        maintainers[m_name].add(m_email)
                elif m_email != '':
                    maintainers[m_name].add(m_email)
                if 'debian' in m_name.lower():
                    p_type = 'debianCommunity'
                package_properties.append(['hasMaintainer', 'resource', m_name])
            architectures.add(p_content['Architecture'])
            package_properties.append(['hasArchitecture', 'resource', p_content['Architecture']])
            package_properties.append(['description', 'datatype', p_content['Description'], 'string'])
            if 'window manager' in p_content['Description'].lower():
                p_type = 'windowManager'
            package_properties.append(['version', 'datatype', p_content['Version'], 'string'])
            rdf_obj.new_named_individual(p, p_type, package_properties)
    for m in maintainers:
        print('Processing maintainer: '+m)
        maintainers_props = []
        for m_email in maintainers[m]:
            maintainers_props.append(['email', 'datatype', m_email, 'string'])
        rdf_obj.new_named_individual(m, 'maintainer', maintainers_props)


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
        n = n.split('<')
        n = n[0].split('(')
        n = n[0].split('|')
        n = n[0].strip().replace(' ', '_')
        names_list.add(n)
    return names_list


def format_maintainer(maintainer):
    m = maintainer.split('<')
    m_name = m[0].split('(')
    m_name = m_name[0].strip()
    if len(m) > 1:
        m_email = m[1].replace('>', '')
    else:
        m_email = ''
    return [m_name, m_email]


def main(file_type):
    start_time = time.time()
    if file_type == 'owl':
        owl_structure = OWL('owl_ontology_final', 'owl_ontology_final.owl')
        create_package_owl_instance(owl_structure)
        owl_structure.end_ontology()
    elif file_type == 'rdf':
        rdf_structure = RDF('rdf_ontology', 'rdf_ontology.owl')
        create_package_rdf_instance(rdf_structure)
        rdf_structure.end_rdf()
    print("--- %s seconds ---" % (time.time() - start_time))

if __name__ == "__main__":
    f_type = input("type of file: \n")
    main(f_type)