__author__ = 'Maira'


class OWL:
    def __init__(self, namespace, output_file):
        self.namespace = namespace
        self.output_file = output_file
        self.owl = ''
        self.declarations = ''
        self.subclasses = ''
        self.class_assertions = ''
        self.obj_prop_assertion = ''
        self.data_prop_assertion = ''
        self.sub_object_properties = ''
        self.obj_prop_domain = ''
        self.obj_prop_range = ''
        self.func_data_prop = ''
        self.data_prop_domain = ''
        self.data_prop_range = ''
        self.start_owl()
        self.start_ontology()
        self.declare_classes()
        self.declare_object_properties()
        self.declare_subclasses()
        self.declare_obj_restrictions_subclass()
        self.declare_data_restrictions_subclass()
        self.declare_sub_object_properties()
        self.declare_object_prop_range()
        self.declare_func_data_prop()
        self.declare_data_prop_domain()
        self.declare_data_prop_range()

    def start_owl(self):
        """
        Starts the owl file with version and doctype
        """
        self.owl = '<?xml version="1.0"?>\n\n' \
                   '<!DOCTYPE Ontology [\n' \
                   '\t<!ENTITY xsd "http://www.w3.org/2001/XMLSchema#" >\n' \
                   '\t<!ENTITY xml "http://www.w3.org/XML/1998/namespace" >\n' \
                   '\t<!ENTITY rdfs "http://www.w3.org/2000/01/rdf-schema#" >\n' \
                   '\t<!ENTITY rdf "http://www.w3.org/1999/02/22-rdf-syntax-ns#" >\n' \
                   ']>\n'
        return

    def start_ontology(self):
        """
        Start the ontology tag from the OWL
        """
        self.owl += '<Ontology xmlns="http://www.w3.org/2002/07/owl#"\n' \
                    '\txml:base="http://www.semanticweb.org/ontologies/2015/3/'+self.namespace+'.owl"\n' \
                    '\txmlns:rdfs="http://www.w3.org/2000/01/rdf-schema#"\n' \
                    '\txmlns:xsd="http://www.w3.org/2001/XMLSchema#"\n' \
                    '\txmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"\n' \
                    '\txmlns:xml="http://www.w3.org/XML/1998/namespace"\n' \
                    '\tontologyIRI="http://www.semanticweb.org/ontologies/2015/3/'+self.namespace+'.owl">\n' \
                    '\t<Prefix name="'+self.namespace+'" IRI="http://www.semanticweb.org/ontologies/2015/3/'+self.namespace+'.owl#"/>\n' \
                    '\t<Prefix name="xsd" IRI="http://www.w3.org/2001/XMLSchema#"/>\n' \
                    '\t<Prefix name="" IRI="http://www.w3.org/2002/07/owl#"/>\n' \
                    '\t<Prefix name="rdf" IRI="http://www.w3.org/1999/02/22-rdf-syntax-ns#"/>\n' \
                    '\t<Prefix name="rdfs" IRI="http://www.w3.org/2000/01/rdf-schema#"/>\n' \
                    '\t<Prefix name="owl" IRI="http://www.w3.org/2002/07/owl#"/>\n'

    def end_ontology(self):
        """
        Ends the ontology tag from the owl
        """
        print('generating OWL ontology file...')
        file = open(self.output_file, 'w+')
        file.write(self.owl)
        file.write(self.declarations)
        file.write(self.subclasses)
        file.write(self.class_assertions)
        file.write(self.obj_prop_assertion)
        file.write(self.data_prop_assertion)
        file.write(self.sub_object_properties)
        file.write(self.obj_prop_domain)
        file.write(self.obj_prop_range)
        file.write(self.func_data_prop)
        file.write(self.data_prop_domain)
        file.write(self.data_prop_range)
        file.write('</Ontology>')
        file.close()
        print('OWL ontology file generated!')

    def generate_owl_file(self):
        print('generating ontology file...')
        file = open(self.output_file, 'w+')
        file.write(self.owl)
        file.close()
        print('ontology file generated!')

    def new_declaration(self, obj, declaration_type):
        """
        Add a new declaration to the ontology
        :param obj: object to be declared
        :param declaration_type: Class or ObjectProperty or DataProperty or NamedIndividual
        """
        obj = obj.replace('<', '&lt;')
        obj = obj.replace('>', '&gt;')
        obj = obj.replace(' ', '_')
        self.declarations += '\t<Declaration>\n'
        self.declarations += '\t\t<'+declaration_type+' IRI="#'+obj+'"/>\n'
        self.declarations += '\t</Declaration>\n'

    def declare_classes(self):
        """
        Declare the classes of the ontology
        """
        classes = ['architecture',
                   'debianCommunity',
                   'debianPackage',
                   'genericPackage',
                   'maintainer',
                   #'priority',
                   #'section',
                   'windowManager']
        for c in classes:
            self.new_declaration(c, 'Class')

    def declare_object_properties(self):
        """
        Declare the object properties of the ontology
        """
        objects_properties = [  #'breaks',
                              'conflicts',
                              'depends',
                              'has',
                              'hasArchitecture',
                              'hasMaintainer',
                              #'hasPriority',
                              #'hasSection',
                              'provides',
                              'recommends',
                              #'replaces',
                              'suggests']
        for obj in objects_properties:
            self.new_declaration(obj, 'ObjectProperty')

    def declare_data_properties(self):
        """
        Declare the data properties of the ontology
        """
        data_properties = ['description',
                           'email',
                           'version']
        for data in data_properties:
            self.new_declaration(data, 'DataProperty')

    def declare_named_individual(self, name):
        """
        Add a named individual to the ontology (called on the loop of the packages)
        """
        self.new_declaration(name, 'NamedIndividual')


    def new_subclass_of_class(self, child, parent):
        child = child.replace('<', '&lt;')
        child = child.replace('>', '&gt;')
        child = child.replace(' ', '_')
        parent = parent.replace('<', '&lt;')
        parent = parent.replace('>', '&gt;')
        parent = parent.replace(' ', '_')
        self.subclasses += '\t<SubClassOf>\n'
        self.subclasses += '\t\t<Class IRI="#'+child+'"/>\n'
        self.subclasses += '\t\t<Class IRI="#'+parent+'"/>\n'
        self.subclasses += '\t</SubClassOf>\n'

    def new_obj_restriction_subclass(self, class1, t, class2):
        """
        create a new object restriction for the ontology
        """
        class1 = class1.replace('<', '&lt;')
        class1 = class1.replace('>', '&gt;')
        class1 = class1.replace(' ', '_')
        t = t.replace('<', '&lt;')
        t = t.replace('>', '&gt;')
        t = t.replace(' ', '_')
        class2 = class2.replace('<', '&lt;')
        class2 = class2.replace('>', '&gt;')
        class2 = class2.replace(' ', '_')
        self.subclasses += '\t<SubClassOf>\n'
        self.subclasses += '\t\t<Class IRI="#'+class1+'"/>\n'
        self.subclasses += '\t\t<ObjectSomeValuesFrom>>\n'
        self.subclasses += '\t\t\t<ObjectProperty IRI="#'+t+'"/>\n'
        self.subclasses += '\t\t\t<Class IRI="#'+class2+'"/>\n'
        self.subclasses += '\t\t</ObjectSomeValuesFrom>>\n'
        self.subclasses += '\t</SubClassOf>\n'

    def new_data_restriction_subclass(self, c, t, p, v):
        """
       create a new data restriction for the ontology.
       The restriction types can be: all, cardinality or some.

        """
        c = c.replace('<', '&lt;')
        c = c.replace('>', '&gt;')
        c = c.replace(' ', '_')
        p = p.replace('<', '&lt;')
        p = p.replace('>', '&gt;')
        p = p.replace(' ', '_')
        v = v.replace('<', '&lt;')
        v = v.replace('>', '&gt;')
        v = v.replace(' ', '_')
        self.subclasses += '\t<SubClassOf>\n'
        self.subclasses += '\t\t<Class IRI="#'+c+'"/>\n'
        if t == 'all':
            self.subclasses += '\t\t<DataAllValuesFrom>\n'
            self.subclasses += '\t\t\t<DataProperty IRI="#'+p+'"/>\n'
            self.subclasses += '\t\t\t<Datatype abbreviatedIRI="rdfs:'+v+'"/>\n'
            self.subclasses += '\t\t</DataAllValuesFrom>\n'
        elif t == 'cardinality':
            self.subclasses += '\t\t<DataExactCardinality cardinality="'+v+'">\n'
            self.subclasses += '\t\t\t<DataProperty IRI="#'+p+'"/>\n'
            self.subclasses += '\t\t</DataExactCardinality>\n'
        elif t == 'some':
            self.subclasses += '\t\t<DataSomeValuesFrom>\n'
            self.subclasses += '\t\t\t<DataProperty IRI="#'+p+'"/>\n'
            self.subclasses += '\t\t\t<Datatype abbreviatedIRI="rdfs:'+v+'"/>\n'
            self.subclasses += '\t\t</DataSomeValuesFrom>\n'
        self.subclasses += '\t</SubClassOf>\n'

    def declare_subclasses(self):
        """
        Initialize the subclasses of the ontology
        """
        subclasses = [['debianCommunity', 'debianPackage'],
                      ['debianPackage','genericPackage'],
                      ['windowManager','debianPackage']]
        for subclass in subclasses:
            self.new_subclass_of_class(subclass[0], subclass[1])

    def declare_obj_restrictions_subclass(self):
        """
        Initialize the subclasses restrictions for the ontology
        Section, Priority, Breaks, Replaces
        """
        restrictions = [  #['debianPackage', 'breaks', 'debianPackage'],
                        ['debianPackage', 'conflicts', 'debianPackage'],
                        ['debianPackage', 'hasArchitecture', 'architecture'],
                        ['debianPackage', 'hasMaintainer', 'maintainer'],
                        #['debianPackage', 'hasPriority', 'priority'],
                        #['debianPackage', 'hasSection', 'section'],
                        ['debianPackage', 'provides', 'debianPackage'],
                        ['debianPackage', 'recommends', 'debianPackage'],
                        #['debianPackage', 'replaces', 'debianPackage'],
                        ['debianPackage', 'suggests', 'debianPackage'],
                        ['genericPackage', 'depends', 'genericPackage']]
        for r in restrictions:
            self.new_obj_restriction_subclass(r[0], r[1], r[2])

    def declare_data_restrictions_subclass(self):
        restrictions = [['genericPackage', 'all', 'description', 'string'],
                        ['genericPackage', 'cardinality', 'version', '1'],
                        ['maintainer', 'some', 'email', 'string']]
        for r in restrictions:
            self.new_data_restriction_subclass(r[0], r[1], r[2], r[3])

    def add_class_assertion(self, c, ind):
        """
        Add an individual ind to a class c
        :param c: class of the individual
        :param ind: name of the individual
        :return:
        """
        c = c.replace('<', '&lt;')
        c = c.replace('>', '&gt;')
        c = c.replace(' ', '_')
        ind = ind.replace('<', '&lt;')
        ind = ind.replace('>', '&gt;')
        ind = ind.replace(' ', '_')
        self.class_assertions += '\t<ClassAssertion>\n'
        self.class_assertions += '\t\t<Class IRI="#'+c+'"/>\n'
        self.class_assertions += '\t\t<NamedIndividual IRI="#'+ind+'"/>\n'
        self.class_assertions += '\t</ClassAssertion>\n'

    def new_obj_property_assertion(self, p, c1, c2):
        """
        Create a new object property assertion for the ontology
        """
        p = p.replace('<', '&lt;')
        p = p.replace('>', '&gt;')
        p = p.replace(' ', '_')
        c1 = c1.replace('<', '&lt;')
        c1 = c1.replace('>', '&gt;')
        c1 = c1.replace(' ', '_')
        c2 = c2.replace('<', '&lt;')
        c2 = c2.replace('>', '&gt;')
        c2 = c2.replace(' ', '_')
        self.obj_prop_assertion += '\t<ObjectPropertyAssertion>\n'
        self.obj_prop_assertion += '\t\t<ObjectProperty IRI="#'+p+'"/>\n'
        self.obj_prop_assertion += '\t\t<NamedIndividual IRI="#'+c1+'"/>\n'
        self.obj_prop_assertion += '\t\t<NamedIndividual IRI="#'+c2+'"/>\n'
        self.obj_prop_assertion += '\t</ObjectPropertyAssertion>\n'

    def new_data_property_assertion(self, dp, ind, data):
        """
        Create a new data property assertion for the ontology
        """
        dp = dp.replace('<', '&lt;')
        dp = dp.replace('>', '&gt;')
        dp = dp.replace(' ', '_')
        ind = ind.replace('<', '&lt;')
        ind = ind.replace('>', '&gt;')
        ind = ind.replace(' ', '_')
        data = data.replace('<', '&lt;')
        data = data.replace('>', '&gt;')
        data = data.replace(' ', '_')
        self.data_prop_assertion += '\t<DataPropertyAssertion>\n'
        self.data_prop_assertion += '\t\t<DataProperty IRI="#'+dp+'"/>\n'
        self.data_prop_assertion += '\t\t<NamedIndividual IRI="#'+ind+'"/>\n'
        self.data_prop_assertion += '\t\t<Literal datatypeIRI="&xsd;string">'+data+'</Literal>\n'
        self.data_prop_assertion += '\t</DataPropertyAssertion>\n'

    def new_sub_object_property(self, prop, parent):
        """
        Create a new sub object property for the ontology
        """
        prop = prop.replace('<', '&lt;')
        prop = prop.replace('>', '&gt;')
        prop = prop.replace(' ', '_')
        parent = parent.replace('<', '&lt;')
        parent = parent.replace('>', '&gt;')
        parent = parent.replace(' ', '_')
        self.sub_object_properties += '\t<SubObjectPropertyOf>\n'
        self.sub_object_properties += '\t\t<ObjectProperty IRI="#'+prop+'"/>\n'
        self.sub_object_properties += '\t\t<ObjectProperty IRI="#'+parent+'"/>\n'
        self.sub_object_properties += '\t</SubObjectPropertyOf>\n'

    def declare_sub_object_properties(self):
        """

        :return:
        """
        sub_obj_prop = [['hasArchitecture', 'has'],
                        ['hasMaintainer', 'has']]
                        #['hasPriority', 'has'],
                        #['hasSection', 'has']]
        for prop in sub_obj_prop:
            self.new_sub_object_property(prop[0], prop[1])

    def new_object_prop_domain(self, prop, domain):
        """
        Set the domains for the object properties
        :param obj:
        :param domain:
        :return:
        """
        prop = prop.replace('<', '&lt;')
        prop = prop.replace('>', '&gt;')
        prop = prop.replace(' ', '_')
        domain = domain.replace('<', '&lt;')
        domain = domain.replace('>', '&gt;')
        domain = domain.replace(' ', '_')
        self.obj_prop_domain += '\t<ObjectPropertyDomain>\n'
        self.obj_prop_domain += '\t\t<ObjectProperty IRI="#'+prop+'"/>\n'
        self.obj_prop_domain += '\t\t<Class IRI="#'+domain+'"/>\n'
        self.obj_prop_domain += '\t</ObjectPropertyDomain>\n'

    def declare_object_prop_domain(self):
        """
        Declare the object properties domains
        :return:
        """
        obj_props_domains = [  #['breaks', 'debianPackage'],
                             ['conflicts', 'debianPackage'],
                             ['depends', 'genericPackage'],
                             ['has', 'debianPackage'],
                             ['hasArchitecture', 'debianPackage'],
                             ['hasMaintainer', 'debianPackage'],
                             #['hasPriority', 'debianPackage'],
                             #['hasSection', 'debianPackage'],
                             ['provides', 'debianPackage'],
                             ['recommends', 'debianPackage'],
                             #['replaces', 'debianPackage'],
                             ['suggests', 'debianPackage']]
        for obj_prop_d in obj_props_domains:
            self.new_object_prop_domain(obj_prop_d[0], obj_prop_d[1])

    def new_object_prop_range(self, prop, rang, union=False):
        """
        define the objects properties ranges on the ontology
        """
        prop = prop.replace('<', '&lt;')
        prop = prop.replace('>', '&gt;')
        prop = prop.replace(' ', '_')
        self.obj_prop_range += '\t<ObjectPropertyRange>\n'
        self.obj_prop_range += '\t\t<ObjectProperty IRI="#'+prop+'"/>\n'
        if not union:
            rang = rang.replace('<', '&lt;')
            rang = rang.replace('>', '&gt;')
            rang = rang.replace(' ', '_')
            self.obj_prop_range += '\t\t<Class IRI="#'+rang+'"/>\n'
        else:
            self.obj_prop_range += '\t\t<ObjectUnionOf>\n'
            for r in rang:
                r = r.replace('<', '&lt;')
                r = r.replace('>', '&gt;')
                r = r.replace(' ', '_')
                self.obj_prop_range += '\t\t\t<Class IRI="#'+r+'"/>\n'
            self.obj_prop_range += '\t\t</ObjectUnionOf>\n'
        self.obj_prop_range += '\t</ObjectPropertyRange>\n'

    def declare_object_prop_range(self):
        """
        declare the object properties ranges
        """
        obj_props_ranges = [  #['breaks', 'debianPackage', False],
                            ['conflicts', 'debianPackage', False],
                            ['depends', 'genericPackage', False],
                            ['has', ['architecture', 'maintainer'], True],
                            ['hasArchitecture', 'architecture', False],
                            ['hasMaintainer', 'maintainer', False],
                            #['hasPriority', 'priority', False],
                            #['hasSection', 'section', False],
                            ['provides', 'debianPackage', False],
                            ['recommends', 'debianPackage', False],
                            #['replaces', 'debianPackage', False],
                            ['suggests', 'debianPackage', False]]
        for opr in obj_props_ranges:
            self.new_object_prop_range(opr[0], opr[1], opr[2])

    def new_func_data_prop(self, data):
        """


        :return:
        """
        data = data.replace('<', '&lt;')
        data = data.replace('>', '&gt;')
        data = data.replace(' ', '_')
        self.func_data_prop += '\t<FunctionalDataProperty>\n'
        self.func_data_prop += '\t\t<DataProperty IRI="#'+data+'"/>\n'
        self.func_data_prop += '\t</FunctionalDataProperty>\n'

    def declare_func_data_prop(self):
        """

        :return:
        """
        func_data_props = ['description', 'version']
        for fdp in func_data_props:
            self.new_func_data_prop(fdp)

    def new_data_prop_domain(self, data, domain):
        """

        :return:
        """
        data = data.replace('<', '&lt;')
        data = data.replace('>', '&gt;')
        data = data.replace(' ', '_')
        domain = domain.replace('<', '&lt;')
        domain = domain.replace('>', '&gt;')
        domain = domain.replace(' ', '_')
        self.data_prop_domain += '\t<DataPropertyDomain>\n'
        self.data_prop_domain += '\t\t<DataProperty IRI="#'+data+'"/>\n'
        self.data_prop_domain += '\t\t<Class IRI="#'+domain+'"/>\n'
        self.data_prop_domain += '\t</DataPropertyDomain>\n'

    def declare_data_prop_domain(self):
        data_props_domains = [['description', 'genericPackage'],
                              ['email', 'maintainer'],
                              ['version', 'genericPackage']]
        for dpd in data_props_domains:
            self.new_data_prop_domain(dpd[0], dpd[1])

    def new_data_prop_range(self, data, r):
        """

        :return:
        """
        data = data.replace('<', '&lt;')
        data = data.replace('>', '&gt;')
        data = data.replace(' ', '_')
        r = r.replace('<', '&lt;')
        r = r.replace('>', '&gt;')
        r = r.replace(' ', '_')
        self.data_prop_domain += '\t<DataPropertyRange>\n'
        self.data_prop_domain += '\t\t<DataProperty IRI="#'+data+'"/>\n'
        self.data_prop_domain += '\t\t<Datatype abbreviatedIRI="xsd:'+r+'"/>\n'
        self.data_prop_domain += '\t</DataPropertyRange>\n'

    def declare_data_prop_range(self):
        data_props_range = [['description', 'string'],
                            ['email', 'string'],
                            ['version', 'string']]
        for dpd in data_props_range:
            self.new_data_prop_range(dpd[0], dpd[1])