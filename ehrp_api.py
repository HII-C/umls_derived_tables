'''
Biomedical text processing API for EHR Phenotyping
'''

from __future__ import print_function

import argparse

from flask import Flask, jsonify
from flask_restful import Api, Resource, reqparse
from ehrp_utils import load_resources, extract_concepts, load_grammars, BioMedConcept
from unitex import init_log_system
from unitex.config import UnitexConfig
import yaml

class Extract(Resource):
    '''Extract API for extracting Biomedical named entities and their respective concept IDs'''
    def post(self):
        '''POST method'''
        print("POST - Extract")     # for debugging
        reqparser = reqparse.RequestParser()
        reqparser.add_argument('text', type=str, required=True, location='json',
                               help="text for extracting entities and concept ids")
        reqargs = reqparser.parse_args()
        print(reqargs['text'])              # for debugging
        text = reqargs['text']
        concepts = extract_concepts(text, OPTIONS)
        return jsonify(concepts)

class Lookup(Resource):
    '''Lookup API for finding the relevant concept ID'''
    def get(self):
        '''GET method'''
        print("GET - Lookup")         # for debugging
        reqparser = reqparse.RequestParser()
        reqparser.add_argument('text', type=str, required=True, location='args',
                               help="text for finding concept id")
        reqargs = reqparser.parse_args()
        print(reqargs['text'])              # for debugging
        text = reqargs['text']
        concepts = extract_concepts(text, OPTIONS)
        # for indx in range(0, min(len(text)-5, 25), 4):
        #     concept = BioMedConcept(text[indx], text[indx+1], text[indx+2], text[indx+3])
        #     concepts.append(concept.serialize())
        return jsonify(concepts)

def main():
    '''Main method : parse arguments and start API'''
    global OPTIONS
    parser = argparse.ArgumentParser()
    # RESOURCE LOCATIONS
    parser.add_argument('--conf', type=str, default='resources/unitex-med.yaml',
                        help="Path to yaml file")
    parser.add_argument('--drug_fst', type=str, default='resources/drug.fst2',
                        help="Path to drug grammar fst2 file")
    parser.add_argument('--dis_fst', type=str, default='resources/dis.fst2',
                        help="Path to disease grammar fst2 file")
    # API SETTINGS
    parser.add_argument('--host', type=str, default='localhost',
                        help="Host name (default: localhost)")
    parser.add_argument('--port', type=int, default='8020', help="Port (default: 8020)")
    parser.add_argument('--path', type=str, default='/ehrp', help="Path (default: /ehrp)")
    args = parser.parse_args()

    # Load resources
    config = None
    with open(args.conf, "r") as c_file:
        config = yaml.load(c_file)
    OPTIONS = UnitexConfig(config)
    init_log_system(OPTIONS["verbose"], OPTIONS["debug"], OPTIONS["log"])
    load_resources(OPTIONS)
    load_grammars(OPTIONS)

    print("Starting app . . .")
    app = Flask(__name__)
    api = Api(app)

    @app.errorhandler(404)
    def page_not_found(error):
        '''Error message for page not found'''
        return "page not found : " + error

    @app.errorhandler(500)
    def raise_error(error):
        '''Error message for resource not found'''
        return error

    api.add_resource(Extract, args.path+'/extract')
    api.add_resource(Lookup, args.path+'/lookup')
    app.run(host=args.host, port=args.port)

    # Free resources
    # free_resources(options)


if __name__ == '__main__':
    main()
