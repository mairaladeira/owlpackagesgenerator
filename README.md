OWL and Semantic Web : lab work
===============================

Laboratory work for the DMKM course: Ontology and semantic web 2015.

Functionality:
--------------
This project:
   * generates and populates a Packages ontology in rdf and notation 3 (turtle).
   * Reasoners on the ontology in order to determine:
      * Debian Community Packages
      * Window Manager Packages
      * The *Conflicts* of an input package
      * The *Dependencies* of an input package
      * The *Suggestions* of an input package
      * The *Recommendations* of an input package

How to use:
-----------
To run the ontology_generator.py file:
```
python ontology_generator.py -p <Packages_file> -t <rdf_or_n3> -o <Output_file>
```
Where *Packages_file* is the file that contains the linux files supposed to populate the ontology
*rdf_or_n3* is the type of file to be generated (Should be replaced by rdf or n3)
*Output_file* is the file to be generated, *without* the extension. (The program generates .owl files for RDF and .ttf for Notation 3)

To run the reasoner.py file:
```
python reasoner.py
```
and follow the instructions.