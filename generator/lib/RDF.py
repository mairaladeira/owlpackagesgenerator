__author__ = 'Maira'


class RDF:
    """
    This class has all the functionality to create and populate the RDF ontology
    """
    def __init__(self, namespace, output_file):
        self.namespace = namespace
        self.output_file = output_file
        self.url = 'http://www.semanticweb.org/ontologies/2015/3/'
        self.rdf = ''
        self.o_property = ''
        self.dt_property = ''
        self.classes = ''
        self.named_individual = ''
        self.start_rdf()
        self.start_ontology()
        self.declare_object_properties()
        self.declare_data_type_property()
        self.declare_classes()


    def start_rdf(self):
        """
        Start the RDF ontology
        :return:
        """
        self.rdf += '<?xml version="1.0"?>\n\n\n'
        self.rdf += '<!DOCTYPE rdf:RDF [\n'
        self.rdf += '\t<!ENTITY xsd "http://www.w3.org/2001/XMLSchema#" >\n'
        self.rdf += '\t<!ENTITY rdfs "http://www.w3.org/2000/01/rdf-schema#" >\n'
        self.rdf += '\t<!ENTITY rdf "http://www.w3.org/1999/02/22-rdf-syntax-ns#" >\n'
        self.rdf += '\t<!ENTITY '+self.namespace+' "'+self.url+self.namespace+'.owl#" >\n'
        self.rdf += ']>\n\n\n'

    def start_ontology(self):
        self.rdf += '<rdf:RDF xmlns="http://www.w3.org/2002/07/owl#"\n'
        self.rdf += '\txml:base="http://www.w3.org/2002/07/owl"\n'
        self.rdf += '\txmlns:'+self.namespace+'="'+self.url+self.namespace+'.owl#"\n'
        self.rdf += '\txmlns:rdfs="http://www.w3.org/2000/01/rdf-schema#"\n'
        self.rdf += '\txmlns:xsd="http://www.w3.org/2001/XMLSchema#"\n'
        self.rdf += '\txmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">\n'
        self.rdf += '\t<Ontology rdf:about="http://www.semanticweb.org/ontologies/2015/3/'+self.namespace+'.owl"/>\n\n\n\n'

    def end_rdf(self):
        """
        Ends the ontology and saves it on the output file
        """
        print('generating OWL ontology file...')
        file = open(self.output_file, 'w+')
        file.write(self.rdf)
        file.write(self.o_property)
        file.write(self.dt_property)
        file.write(self.classes)
        file.write(self.named_individual)
        file.write('</rdf:RDF>')
        file.close()
        print('RDF ontology file generated!')
        return

    def new_object_property(self, prop, d, r, t='', sub_obj_prop='', union_d=False, union_r=False, sub_prop=False):
        """
        Declare a new object property on the RDF ontology
        :param prop: object property
        :param d: domain (might be a list)
        :param r: range (might be a list)
        :param sub_obj_prop: object property parent
        :param union_d:  is the domain composed of an union
        :param union_r: is the range composed of an union
        :param sub_prop: is the property a sub property
        """
        self.o_property += '\t<!-- '+self.url+self.namespace+'.owl#'+prop+' -->\n\n'
        self.o_property += '\t<ObjectProperty rdf:about="&'+self.namespace+';'+prop+'">\n'
        if t != '':
            self.o_property += '\t\t<rdf:type rdf:resource="http://www.w3.org/2002/07/owl#'+t+'Property"/>\n'
        if not union_d:
            self.o_property += '\t\t<rdfs:domain rdf:resource="&'+self.namespace+';'+d+'"/>\n'
        else:
            self.o_property += '\t\t<rdfs:domain>\n'
            self.o_property += '\t\t\t<Class>\n'
            self.o_property += '\t\t\t\t<unionOf rdf:parseType="Collection">\n'
            for dom in d:
                self.o_property += '\t\t\t\t\t<rdf:Description rdf:about="&'+self.namespace+';'+dom+'"/>\n'
            self.o_property += '\t\t\t\t</unionOf>\n'
            self.o_property += '\t\t\t</Class>\n'
            self.o_property += '\t\t</rdfs:domain>\n'
        if not union_r:
            self.o_property += '\t\t<rdfs:range rdf:resource="&'+self.namespace+';'+r+'"/>\n'
        else:
            self.o_property += '\t\t<rdfs:range>\n'
            self.o_property += '\t\t\t<Class>\n'
            self.o_property += '\t\t\t\t<unionOf rdf:parseType="Collection">\n'
            for rang in r:
                self.o_property += '\t\t\t\t\t<rdf:Description rdf:about="&'+self.namespace+';'+rang+'"/>\n'
            self.o_property += '\t\t\t\t</unionOf>\n'
            self.o_property += '\t\t\t</Class>\n'
            self.o_property += '\t\t</rdfs:range>\n'
        if sub_prop:
            self.o_property += '<rdfs:subPropertyOf rdf:resource="&'+self.namespace+';'+sub_obj_prop+'"/>'
        self.o_property += '\t</ObjectProperty>\n\n\n'

    def declare_object_properties(self):
        """
        Declare the object properties for the RDF ontology
        """
        object_properties = [['conflicts', 'debianPackage', 'debianPackage', 'Transitive', '', False, False, False],
                             ['depends', 'genericPackage', 'genericPackage', 'Transitive', '', False, False, False],
                             ['has', 'debianPackage', ['architecture', 'maintainer'], '', '', False, True, False],
                             ['hasArchitecture', 'debianPackage', 'architecture', 'Functional', 'has', False, False, True],
                             ['hasMaintainer', 'debianPackage', 'maintainer', 'Functional', 'has', False, False, True],
                             ['provides', 'debianPackage', 'debianPackage', '', '', False, False, False],
                             ['recommends', 'debianPackage', 'debianPackage', '', '', False, False, False],
                             ['suggests', 'debianPackage', 'debianPackage', '', '', False, False, False]]
        for obj_prop in object_properties:
            self.new_object_property(obj_prop[0], obj_prop[1], obj_prop[2], obj_prop[3], obj_prop[4],
                                     obj_prop[5], obj_prop[6], obj_prop[7])

    def new_data_type_property(self, dtp, is_functional, d, r):
        """
        Add a new Data type Properties on the RDF ontology
        :param dtp: Data type property
        :param is_functional: is a functional data type property
        :param d: domain
        :param r: range
        """
        self.dt_property += '\t<!-- '+self.url+self.namespace+'.owl#'+dtp+' -->\n\n'
        self.dt_property += '\t<DatatypeProperty rdf:about="&'+self.namespace+';'+dtp+'">\n'
        if is_functional:
            self.dt_property += '\t\t<rdf:type rdf:resource="http://www.w3.org/2002/07/owl#FunctionalProperty"/>\n'
        self.dt_property += '\t\t<rdfs:domain rdf:resource="&'+self.namespace+';'+d+'"/>\n'
        self.dt_property += '\t\t<rdfs:range rdf:resource="&xsd;'+r+'"/>\n'
        self.dt_property += '\t</DatatypeProperty>\n\n\n'

    def declare_data_type_property(self):
        """
        Declare the data type properties for the ontology
        """
        data_type_properties = [['description', True, 'genericPackage', 'string'],
                                ['email', False, 'maintainer', 'string'],
                                ['version', True, 'genericPackage', 'string']]
        for dtp in data_type_properties:
            self.new_data_type_property(dtp[0], dtp[1], dtp[2], dtp[3])

    def new_class(self, c, restrictions):
        """
        Add a new class on the RDF ontology
        :param c:
        :param restrictions:
        """
        self.classes += '\t<!-- '+self.url+self.namespace+'.owl#'+c+' -->\n\n'
        if len(restrictions) == 0:
            self.classes += '\t<Class rdf:about="&'+self.namespace+';'+c+'"/>\n'
        else:
            self.classes += '\t<Class rdf:about="&'+self.namespace+';'+c+'">\n'
            for r in restrictions:
                if 'restrictionType' in r and r['restrictionType'] == 'subClassOf':
                    if 'restriction' not in r:
                        self.classes += '\t\t<rdfs:subClassOf rdf:resource="&'+self.namespace+';'+r['sub_class']+'"/>\n'
                    else:
                        rest = r['restriction']
                        self.classes += '\t\t<rdfs:subClassOf>\n'
                        self.classes += '\t\t\t<Restriction>\n'
                        self.classes += '\t\t\t\t<onProperty rdf:resource="&'+self.namespace+';'+rest[0]+'"/>\n'
                        if rest[1] == 'some':
                            if rest[2] == 'class':
                                self.classes += '\t\t\t\t<someValuesFrom rdf:resource="&'+self.namespace+';'+rest[3]+'"/>\n'
                            if rest[2] == 'data_type':
                                self.classes += '\t\t\t\t<someValuesFrom rdf:resource="&rdfs;'+rest[3]+'"/>\n'
                        elif rest[1] == 'all':
                            if rest[2] == 'class':
                                self.classes += '\t\t\t\t<allValuesFrom rdf:resource="&'+self.namespace+';'+rest[3]+'"/>\n'
                            if rest[2] == 'data_type':
                                self.classes += '\t\t\t\t<allValuesFrom rdf:resource="&rdfs;'+rest[3]+'"/>\n'

                        elif rest[1] == 'cardinality':
                            self.classes += '\t\t\t\t<cardinality rdf:datatype="&xsd;nonNegativeInteger">'+rest[3]+'</cardinality>\n'
                        self.classes += '\t\t\t</Restriction>\n'
                        self.classes += '\t\t</rdfs:subClassOf>\n'
                elif 'restrictionType' in r and r['restrictionType'] == 'equivalentClass':
                    self.classes += '\t\t<equivalentClass rdf:resource="&'+self.namespace+';'+r['equiv_class']+'"/>\n'
                elif 'restrictionType' in r and r['restrictionType'] == 'disjointWith':
                    self.classes += '\t\t<disjointWith rdf:resource="&'+self.namespace+';'+r['class']+'"/>\n'

            self.classes += '\t</Class>\n\n\n'

    def declare_classes(self):
        """
        Declare the pre defined classes for the ontology using RDF
        :return:
        """
        classes = [['architecture', [{'restrictionType': 'disjointWith', 'class': 'genericPackage'},
                                     {'restrictionType': 'disjointWith', 'class': 'maintainer'}]],
                   ['debianCommunity', [{'restrictionType': 'subClassOf', 'sub_class': 'debianPackage'}]],
                   ['debianPackage', [{'restrictionType': 'subClassOf', 'sub_class': 'genericPackage'},
                             {'restrictionType': 'subClassOf', 'restriction': ['conflicts', 'some', 'class', 'debianPackage']},
                             {'restrictionType': 'subClassOf', 'restriction': ['provides', 'some', 'class', 'debianPackage']},
                             {'restrictionType': 'subClassOf', 'restriction': ['recommends', 'some', 'class', 'debianPackage']},
                             {'restrictionType': 'subClassOf', 'restriction': ['suggests', 'some', 'class', 'debianPackage']},
                             {'restrictionType': 'subClassOf', 'restriction': ['hasMaintainer', 'some', 'class', 'maintainer']},
                             {'restrictionType': 'subClassOf', 'restriction': ['hasArchitecture', 'some', 'class', 'architecture']}
                         ]
                   ],
                   ['genericPackage',
                        [{'restrictionType': 'subClassOf', 'restriction': ['depends', 'some', 'class', 'genericPackage']},
                             {'restrictionType': 'subClassOf', 'restriction': ['description', 'all', 'data_type', 'Literal']},
                             {'restrictionType': 'subClassOf', 'restriction': ['version', 'cardinality', '', '1']},
                             {'restrictionType': 'disjointWith', 'class': 'maintainer'}
                        ]
                   ],
                   ['maintainer', [{'restrictionType': 'subClassOf', 'restriction': ['email', 'some', 'data_type', 'Literal']}]],
                   ['windowManager', [{'restrictionType': 'subClassOf', 'sub_class': 'debianPackage'}]]
                  ]
        for c in classes:
            self.new_class(c[0], c[1])

    def new_named_individual(self, ind, t, props):
        """
        Insert a named individual on the ontology
        :return:
        """
        ind = ind.split('(')
        ind = ind[0].split('<')
        ind = ind[0].split('|')
        ind = ind[0].replace('<', '&lt;')
        ind = ind.replace('>', '&gt;')
        ind = ind.replace(' ', '_')
        self.named_individual += '\t<!-- '+self.url+self.namespace+'.owl#'+ind+' -->\n\n\n'
        self.named_individual += '\t<NamedIndividual rdf:about="&'+self.namespace+';'+ind+'">\n'
        self.named_individual += '\t\t<rdf:type rdf:resource="&'+self.namespace+';'+t+'"/>\n'
        for p in props:
            #properties should be a list of the type:
            # [name_prop, type(resource or datatype), val, datatype_type(optional)]
            name = p[0].split('(')
            name = name[0].split('<')
            name = name[0].split('|')
            name = name[0].replace('<', '&lt;').replace('&', '&amp;').replace('>', '&gt;').strip().replace(' ', '_')
            val = p[2].split('(')
            val = val[0].split('<')
            val = val[0].split('|')
            val = val[0].replace('<', '&lt;').replace('&', '&amp;').replace('>', '&gt;').strip().replace(' ', '_')
            if p[1] == 'datatype':
                self.named_individual += '\t\t<'+self.namespace+':'+name+' ' \
                                         'rdf:datatype="&xsd;'+p[3]+'">'+val+'</'+self.namespace+':'+name+'>\n'
            if p[1] == 'resource':
                self.named_individual += '\t\t<'+self.namespace+':'+name+' ' \
                                         'rdf:resource="&'+self.namespace+';'+val+'"/>\n'
        self.named_individual += '\t</NamedIndividual>\n\n\n'