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
        self.start_notation3()
        self.declare_object_properties()
        self.declare_data_type_properties()
        self.declare_classes()
        self.file = open(self.output_file, 'w+')
        self.file.write(self.n3)
        self.file.write(self.o_property)
        self.file.write(self.dt_property)
        self.file.write(self.classes)

    def start_notation3(self):
        """
        Start the notation3 ontology
        :return:
        """
        self.n3 += '@prefix ' + self.namespace + ': ' \
                                                 '<http://www.semanticweb.org/ontologies/2015/3/' + self.namespace + '.owl#> .\n'
        self.n3 += '@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .\n'
        self.n3 += '@prefix owl: <http://www.w3.org/2002/07/owl#> .\n'
        self.n3 += '@prefix : <http://www.w3.org/2002/07/owl#> .\n'
        self.n3 += '@prefix xml: <http://www.w3.org/XML/1998/namespace> .\n'
        self.n3 += '@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .\n'
        self.n3 += '@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .\n'
        self.n3 += '@base <http://www.semanticweb.org/ontologies/2015/3/' + self.namespace + '.owl> .\n\n'
        self.n3 += '<http://www.semanticweb.org/ontologies/2015/3/' + self.namespace + '.owl> rdf:type owl:Ontology .\n\n\n\n'

    def end_notation3(self):
        """
        :return:
        """
        self.file.close()
        print('Notation 3 ontology file generated!')

    def new_object_property(self, prop, d, r, t='', sub_prop=''):
        """
        Create a new object property for the ontology
        :param prop: the property to be created
        :param d: list of domains
        :param r: list of ranges
        :param t: type of the property (functional, transitive)
        :param sub_prop: if prop is a sub property of another property, add the name of this property here
        """
        self.o_property += '###  http://www.semanticweb.org/ontologies/2015/3/' + self.namespace + '.owl#' + prop + '\n\n'
        if t == '':
            self.o_property += self.namespace + ':' + prop + ' rdf:type owl:ObjectProperty ;\n\n'
        else:
            self.o_property += self.namespace + ':' + prop + ' rdf:type owl:' + t + ' ,\n'
            self.o_property += '\t\t\t\t\t\t\towl:ObjectProperty ;\n\n'
        amount_r = len(r)
        j = 1
        if sub_prop != '':
            self.o_property += '\trdfs:subPropertyOf ' + self.namespace + ':' + sub_prop + ' ;\n\n'
        for dom in d:
            self.o_property += '\trdfs:domain ' + self.namespace + ':' + dom + ' ;\n\n'
        for rang in r:
            """
            rdfs:range [ rdf:type owl:Class ;
                                       owl:unionOf ( Ontology1428188787135:architecture
                                                     Ontology1428188787135:maintainer
                                                   )
                                     ] .

            """
            if amount_r == 1:
                self.o_property += '\trdfs:range ' + self.namespace + ':' + rang + ' .\n\n\n\n'
            elif j == 1:
                self.o_property += '\trdfs:range [ rdf:type owl:Class ;\n'
                self.o_property += '\t\t\t\t\towl:unionOf ( '+self.namespace+':'+rang+'\n'
            else:
                self.o_property += '\t\t\t\t\t\t\t'+self.namespace+':'+rang
            if j == amount_r and amount_r != 1:
                self.o_property += '\t\t\t\t\t)\n'
                self.o_property += '\t\t] .\n\n\n\n'
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

    def new_data_type_property(self, data_prop, d, r, t=''):
        """
        Create a new data property for the ontology
        :param data_prop: the data type property to be created
        :param d: list of domains
        :param r: list of ranges
        :param t: type of the property (functional)
        """
        self.dt_property += '###  http://www.semanticweb.org/ontologies/2015/3/' + self.namespace + '.owl#' + data_prop + '\n\n'
        if t == '':
            self.dt_property += self.namespace + ':' + data_prop + ' rdf:type owl:DatatypeProperty ;\n\n'
        else:
            self.dt_property += self.namespace + ':' + data_prop + ' rdf:type owl:DatatypeProperty ,\n'
            self.dt_property += '\t\t\t\t\t\t\towl:' + t + ' ;\n\n'
        amount_r = len(r)
        j = 1
        for dom in d:
            self.dt_property += '\trdfs:domain ' + self.namespace + ':' + dom + ' ;\n\n'
        for rang in r:
            if j < amount_r:
                self.dt_property += '\trdfs:range ' + self.namespace + ':' + rang + ' ;\n\n'
            else:
                self.dt_property += '\trdfs:range xsd:' + rang + ' .\n\n\n\n'
            j += 1

    def declare_data_type_properties(self):
        """
        Declare the data type properties of the ontology
        """
        dt_properties = [['description', ['genericPackage'], ['string'], 'FunctionalProperty'],
                         ['email', ['maintainer'], ['string'], ''],
                         ['version', ['genericPackage'], ['string'], 'FunctionalProperty']]
        for d in dt_properties:
            self.new_data_type_property(d[0], d[1], d[2], d[3])
        return

    def new_class(self, c, sub_class_of, disjoint):
        """
        Add a new class on the ontology
        """
        self.classes += '###  http://www.semanticweb.org/ontologies/2015/3/' + self.namespace + '.owl#' + c + '\n\n'
        self.classes += self.namespace + ':' + c + ' rdf:type owl:Class ;\n'
        i = 1
        sc_amount = len(sub_class_of)
        j = 1
        disj_amount = len(disjoint)
        for sc in sub_class_of:
            if i == 1:
                self.classes += '\t\trdfs:subClassOf '
            else:
                self.classes += '\t\t\t\t\t\t '
            if 'restriction' not in sc:
                self.classes += self.namespace + ':' + sc['sub_class'] + ' '
            else:
                rest = sc['restriction']
                self.classes += '[ rdf:type owl:Restriction ;\n'
                self.classes += '\t\t\t\towl:onProperty ' + self.namespace + ':' + rest[0] + ' ;\n'
                if rest[1] == 'some':
                    if rest[2] == 'class':
                        self.classes += '\t\t\t\towl:someValuesFrom ' + self.namespace + ':' + rest[3] + '\n'
                    if rest[2] == 'data_type':
                        self.classes += '\t\t\t\towl:someValuesFrom rdfs:' + rest[3] + '\n'
                elif rest[1] == 'all':
                    if rest[2] == 'class':
                        self.classes += '\t\t\t\towl:allValuesFrom ' + self.namespace + ':' + rest[3] + '\n'
                    if rest[2] == 'data_type':
                        self.classes += '\t\t\t\towl:allValuesFrom rdfs:' + rest[3] + '\n'

                elif rest[1] == 'cardinality':
                    self.classes += '\t\t\t\towl:cardinality "' + rest[3] + '"^^xsd:nonNegativeInteger\n'
                self.classes += '\t\t]'
            if i == sc_amount and disj_amount == 0:
                self.classes += '.\n\n\n'
            elif i == sc_amount:
                self.classes += ';\n'
            else:
                self.classes += ',\n'
            i += 1
        for disj in disjoint:
            if j == 1:
                self.classes += '\t\towl:disjointWith ' + self.namespace + ':' + disj + ' '
            else:
                self.classes += '\t\t\t\t\t\t ' + self.namespace + ':' + disj + ' '
            if j < disj_amount:
                self.classes += ',\n'
            else:
                self.classes += '.\n\n\n'
            j += 1

    def declare_classes(self):
        """
        Declare the pre defined classes for the ontology using RDF
        :return:
        """
        classes = [['architecture', [], ['genericPackage', 'maintainer']],
                   ['debianCommunity', [{'restrictionType': 'subClassOf', 'sub_class': 'debianPackage'}], []],
                   ['debianPackage', [{'restrictionType': 'subClassOf', 'sub_class': 'genericPackage'},
                                      {'restrictionType': 'subClassOf',
                                       'restriction': ['conflicts', 'some', 'class', 'debianPackage']},
                                      {'restrictionType': 'subClassOf',
                                       'restriction': ['provides', 'some', 'class', 'debianPackage']},
                                      {'restrictionType': 'subClassOf',
                                       'restriction': ['recommends', 'some', 'class', 'debianPackage']},
                                      {'restrictionType': 'subClassOf',
                                       'restriction': ['suggests', 'some', 'class', 'debianPackage']},
                                      {'restrictionType': 'subClassOf',
                                       'restriction': ['hasMaintainer', 'some', 'class', 'maintainer']},
                                      {'restrictionType': 'subClassOf',
                                       'restriction': ['hasArchitecture', 'some', 'class', 'architecture']}
                   ], []
                   ],
                   ['genericPackage',
                    [{'restrictionType': 'subClassOf', 'restriction': ['depends', 'some', 'class', 'genericPackage']},
                     {'restrictionType': 'subClassOf', 'restriction': ['description', 'all', 'data_type', 'Literal']},
                     {'restrictionType': 'subClassOf', 'restriction': ['version', 'cardinality', '', '1']}
                    ], ['maintainer']
                   ],
                   ['maintainer',
                    [{'restrictionType': 'subClassOf', 'restriction': ['email', 'some', 'data_type', 'Literal']}], []],
                   ['windowManager', [{'restrictionType': 'subClassOf', 'sub_class': 'debianPackage'}], []]
        ]
        for c in classes:
            self.new_class(c[0], c[1], c[2])

    def new_named_individual(self, ind, t, props):
        """
        :return:
        """
        ind = ind.split('(')
        ind = ind[0].split('<')
        ind = ind[0].split('|')
        ind = ind[0].replace('/', '_or_').replace('+', '_').replace('"', '').replace("'", "") \
            .replace('~', '').replace('.', '_').strip().replace(' ', '_').replace('&', '_and_')
        ind = ind.replace('\u00a1', 'a').replace('\u00b1', '').replace('\u00c3', 'n')
        if ind == '':
            return
        named_individual = '###  http://www.semanticweb.org/ontologies/2015/3/' + self.namespace + '.owl#' + ind + '\n\n'
        named_individual += self.namespace + ':' + ind + ' rdf:type ' + self.namespace + ':' + t + ' ,\n'
        named_individual += '\t\t\t\t\t\towl:NamedIndividual '
        if len(props) > 0:
            named_individual += ';\n\n'
        else:
            named_individual += '.\n\n\n'
        j = 1
        amount_props = len(props)
        for p in props:
            # properties should be a list of the type:
            # [name_prop, prop_type(resource or datatype), [val], datatype_type(optional)]
            name = p[0]
            prop_type = p[1]
            values = p[2]
            values_amount = len(values)
            i = 1
            for v in values:
                val = v.split('(')
                val = val[0].split('<')
                val = val[0].split('|')
                val = val[0].replace('/', '_or_').replace('+', '_').replace('"', '').replace("'", "") \
                    .replace('~', '').replace('.', '_').strip().replace(' ', '_').replace('&', '_and_')
                val = val.replace('\u00a1', 'a').replace('\u00b1', '').replace('\u00c3', 'n')
                if prop_type == 'resource':
                    if i == 1:
                        named_individual += self.namespace + ':' + name + ' ' + self.namespace + ':' + val + ' '
                    else:
                        named_individual += '\t\t\t\t\t\t' + self.namespace + ':' + val + ' '
                else:
                    if i == 1:
                        named_individual += self.namespace + ':' + name + ' "' + val + '"^^xsd:' + p[3] + ' '
                    else:
                        named_individual += '\t\t\t\t\t\t"' + val + '"^^xsd:' + p[3] + ' '
                if i != values_amount:
                    named_individual += ',\n'
                elif j == amount_props:
                    named_individual += '.\n\n\n'
                else:
                    named_individual += ';\n'
                i += 1
            j += 1

        self.file.write(named_individual)