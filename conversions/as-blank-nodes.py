import getopt, sys
from rdflib import Graph, URIRef, BNode
from rdflib.namespace import RDF

def main():
    try:
        # Remove 1st argument from the list of command line arguments
        arguments = sys.argv[1:]

        # Define options
        short_options = "f:t:"
        long_options = ["File=", "Type="]

        # Parsing argument
        args, values = getopt.getopt(arguments, short_options, long_options)
        f = None
        t = None
        for arg, value in args:
            if arg in ("-f", "--File"):
                f = value
            elif arg in ("-t", "--Type"):
                t = value
        if (t is None):
            raise Exception("No type provided to match the main subject with. Please pass a type using -t \"<uri>\"")
        if (f is None):
            f = sys.stdin

        # Create a Graph
        g = Graph()

        # Parse in an RDF file local or hosted on the Internet
        g.parse(f)

        # Find main subject
        target = g.value(None, RDF.type, URIRef(t))
        if (target is None):
            raise Exception(f'No named node found with type {t}')

        # Create blank node mapping for all other named node subjects
        d = {}
        for s in g.subjects():
            if (s != target):
                d[s]=BNode()

        # For each triple (s, p, o), map named node in subject and object position
        # (if not mapping found for the subject or object just keep it)
        gg = Graph()
        for s, p, o in g:
            gg.add((d.get(s,s),p,d.get(o,o)))

        # Print out the entire Graph in the RDF Turtle format
        print(gg.serialize(format="turtle"))
    except Exception as e:
        print(f"{e}")
        quit()

def quit():
    sys.exit(0)

if __name__ == "__main__":
    main()
