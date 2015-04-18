__author__ = 'Maira'


class Notation3:
    """
    This class defines an ontology on the Notation3 format using the sub format turtle from Protege
    """
    def __init__(self, namespace, output_file):
        self.namespace = namespace
        self.output_file = output_file
        self.n3 = ''
        self.o_property = ''
        self.dt_property = ''
        self.classes = ''
        self.named_individual = ''
        self.start_notation3()
        self.declare_object_properties()

    def start_notation3(self):
        """
        Start the notation3 ontology
        :return:
        """
        self.n3 += '@prefix '+self.namespace+': ' \
                   '<http://www.semanticweb.org/ontologies/2015/3/'+self.namespace+'.owl#> .\n'
        self.n3 += '@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .\n'
        self.n3 += '@prefix owl: <http://www.w3.org/2002/07/owl#> .\n'
        self.n3 += '@prefix : <http://www.w3.org/2002/07/owl#> .\n'
        self.n3 += '@prefix xml: <http://www.w3.org/XML/1998/namespace> .\n'
        self.n3 += '@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .\n'
        self.n3 += '@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .\n'
        self.n3 += '@base <http://www.semanticweb.org/ontologies/2015/3/'+self.namespace+'.owl> .\n\n'
        self.n3 += '<http://www.semanticweb.org/ontologies/2015/3/'+self.namespace+'.owl> rdf:type owl:Ontology .\n\n\n\n'

    def end_notation3(self):
        """

        :return:
        """
        print('generating OWL ontology file...')
        file = open(self.output_file, 'w+')
        file.write(self.n3)
        file.write(self.o_property)
        file.write(self.dt_property)
        file.write(self.classes)
        file.write(self.named_individual)
        file.close()
        print('Notation 3 ontology file generated!')
        return

    def new_object_property(self, prop, d, r, t='', sub_prop=''):
        """

                                         owl:TransitiveProperty ;
        :param prop:
        :param d:
        :param r:
        :return:
        """
        self.o_property += '###  http://www.semanticweb.org/ontologies/2015/3/'+self.namespace+'.owl#'+prop+'\n\n'
        if t == '':
            self.o_property += self.namespace+':'+prop+' rdf:type owl:ObjectProperty ;\n\n'
        else:
            self.o_property += self.namespace+':'+prop+' rdf:type owl:'+t+' ,\n\n'
            self.o_property += '\t\t\t\t\t\t\t\towl:ObjectProperty ;\n\n'
        amount_r = len(r)
        j = 1
        if sub_prop != '':
            self.o_property += '\trdfs:subPropertyOf '+self.namespace+':'+sub_prop+' ;\n\n'
        for dom in d:
            self.o_property += '\trdfs:domain '+self.namespace+':'+dom+' ;\n\n'
        for rang in r:
            if j < amount_r:
                self.o_property += '\trdfs:range '+self.namespace+':'+rang+' ,\n\n'
            else:
                self.o_property += '\trdfs:range '+self.namespace+':'+rang+' .\n\n\n\n'
            j += 1

    def declare_object_properties(self):
        """
        Declare the object properties ont he ontology
        """
        object_properties = [['conflicts', ['debianPackage'], ['debianPackage'], 'TransitiveProperty', ''],
                             ['depends', ['genericPackage'], ['genericPackage'], 'TransitiveProperty', ''],
                             ['has', ['debianPackage'], ['architecture', 'maintainer'], '', ''],
                             ['hasArchitecture', ['debianPackage'], ['architecture'], 'FunctionalProperty', 'has'],
                             ['hasMaintainer', ['debianPackage'], ['maintainer'], 'FunctionalProperty', 'has'],
                             ['provides', ['debianPackage'], ['debianPackage'], '', ''],
                             ['recommends', ['debianPackage'], ['debianPackage'], '', ''],
                             ['suggests', ['debianPackage'], ['debianPackage'], '', '']]
        for ob in object_properties:
            self.new_object_property(ob[0], ob[1], ob[2], ob[3], ob[4])