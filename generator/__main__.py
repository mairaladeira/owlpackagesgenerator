__author__ = 'Maira'
import re
from generator.lib.OWL import OWL
import time
start_time = time.time()


def process_package(package,owl_obj):
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


def read_package(file, owl_obj):
    print('reading packages file...')
    with open(file) as f:
        content = f.read()
        f.close()
    packages = content.split('\n\n')
    packages_d = dict()
    print('processing packages...')
    for p in packages:
        d = process_package(p, owl_obj)
        if len(d) > 1:
            packages_d[d['Package']] = d
    return packages_d


def create_package_owl_instance(owl_obj):
    pkgs = read_package('Packages', owl_obj)
    print(str(len(pkgs))+' packages generated')
    print('creating ontology instances...')
    maintainers = set()
    architectures = set()
    sections = set()
    priorities = set()
    for p in pkgs:
        p_content = pkgs[p]
        owl_obj.declare_named_individual(p)
        owl_obj.add_class_assertion('debianPackage', p)
        if 'Maintainer' in p_content:
            maintainers.add(p_content['Maintainer'])
        if 'Architecture' in p_content:
            architectures.add(p_content['Architecture'])
        if 'Section' in p_content:
            sections.add(p_content['Section'])
        if 'Priority' in p_content:
            priorities.add(p_content['Priority'])
    for m in maintainers:
        add_maintainer(m, owl_obj)
    for a in architectures:
        owl_obj.add_class_assertion('architecture', a)
    for s in sections:
        owl_obj.add_class_assertion('sections', s)
    for p in priorities:
        owl_obj.add_class_assertion('priority', p)


def add_maintainer(maintainer, owl_obj):
    m = maintainer.split('<')
    print(m)
    owl_obj.add_class_assertion('maintainer', m[0])


def format_restrictions(c, restriction, owl_obj, t):
    rest_list = restriction.split(',')
    for r in rest_list:
        rest = r.strip().split('(')
        owl_obj.restrictions_subclass(c, rest[0], t)


def main():
    owl_structure = OWL('test', 'owl_ontology.owl')
    create_package_owl_instance(owl_structure)
    owl_structure.end_ontology()
    owl_structure.generate_owl_file()
    print("--- %s seconds ---" % (time.time() - start_time))

main()