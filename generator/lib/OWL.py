__author__ = 'Maira'


class OWL:
    def __init__(self, namespace, output_file):
        self.namespace = namespace
        self.output_file = output_file
        self.owl = ''
        self.declarations = ''
        self.subclasses = ''
        self.class_assertions = ''
        self.start_owl()
        self.start_ontology()
        self.declare_classes()
        self.declare_object_properties()
        self.declare_subclasses()
        self.declare_obj_restrictions_subclass()
        self.declare_data_restrictions_subclass()

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
        self.owl += self.declarations
        self.owl += self.subclasses
        self.owl += self.class_assertions
        self.owl += '</Ontology>'
        print('ontology created!')

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
                   'priority',
                   'section',
                   'windowManager']
        for c in classes:
            self.new_declaration(c, 'Class')

    def declare_object_properties(self):
        """
        Declare the object properties of the ontology
        """
        objects_properties = ['breaks',
                              'conflicts',
                              'depends',
                              'has',
                              'hasArchitecture',
                              'hasMaintainer',
                              'hasPriority',
                              'hasSection',
                              'provides',
                              'recommends',
                              'replaces',
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
        self.subclasses += '\t<SubClassOf>\n'
        self.subclasses += '\t\t<Class IRI="'+child+'"/>\n'
        self.subclasses += '\t\t<Class IRI="'+parent+'"/>\n'
        self.subclasses += '\t</SubClassOf>\n'

    def new_obj_restriction_subclass(self, class1, t, class2):
        """
        create a new object restriction for the ontology
        """
        self.subclasses += '\t<SubClassOf>\n'
        self.subclasses += '\t\t<Class IRI="'+class1+'"/>\n'
        self.subclasses += '\t\t<ObjectSomeValuesFrom>>\n'
        self.subclasses += '\t\t\t<ObjectProperty IRI="#'+t+'">>\n'
        self.subclasses += '\t\t\t<Class IRI="'+class2+'"/>\n'
        self.subclasses += '\t\t</ObjectSomeValuesFrom>>\n'
        self.subclasses += '\t</SubClassOf>\n'

    def new_data_restriction_subclass(self, c, t, p, v):
        """
       create a new data restriction for the ontology.
       The restriction types can be: all, cardinality or some.

        """
        self.subclasses += '\t<SubClassOf>\n'
        self.subclasses += '\t\t<Class IRI="'+c+'"/>\n'
        if t == 'all':
            self.subclasses += '\t\t<DataAllValuesFrom>\n'
            self.subclasses += '\t\t\t<DataProperty IRI="#'+p+'"/>\n'
            self.subclasses += '\t\t\t<Datatype abbreviatedIRI="rdfs:'+v+'"/>\n'
            self.subclasses += '\t\t</DataAllValuesFrom>\n'
        elif t == 'cardinality':
            self.subclasses += '\t\t<DataExactCardinality cardinality="'+v+'">\n'
            self.subclasses += '\t\t\t<DataProperty IRI="#'+v+'"/>\n'
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
        """
        restrictions = [['debianPackage', 'breaks', 'debianPackage'],
                        ['debianPackage', 'conflicts', 'debianPackage'],
                        ['debianPackage', 'hasArchitecture', 'architecture'],
                        ['debianPackage', 'hasMaintainer', 'maintainer'],
                        ['debianPackage', 'hasPriority', 'priority'],
                        ['debianPackage', 'hasSection', 'section'],
                        ['debianPackage', 'provides', 'debianPackage'],
                        ['debianPackage', 'recommends', 'debianPackage'],
                        ['debianPackage', 'replaces', 'debianPackage'],
                        ['debianPackage', 'suggests', 'debianPackage'],
                        ['genericPackage', 'depends', 'genericPackage']]
        for r in restrictions:
            self.new_obj_restriction_subclass(r[0], r[1], r[2])

    def declare_data_restrictions_subclass(self):
        restrictions = [['genericPackage', 'all', 'description', 'Literal'],
                        ['genericPackage', 'cardinality', 'version', '1'],
                        ['maintainer', 'some', 'email', 'Literal']]
        for r in restrictions:
            self.new_data_restriction_subclass(r[0], r[1], r[2], r[3])

    def add_class_assertion(self, c, ind):
        """
        Add an individual ind to a class c
        :param c: class of the individual
        :param ind: name of the individual
        :return:
        """
        self.class_assertions += '\t<ClassAssertion>\n'
        self.class_assertions += '\t\t<Class IRI="#'+c+'"/>\n'
        self.class_assertions += '\t\t<NamedIndividual IRI="#'+ind+'"/>\n'
        self.class_assertions += '\t</ClassAssertion>\n'



