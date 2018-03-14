'''
Utility file containing Unitex related utility methods
'''

from __future__ import print_function

import os
import sys
import random
import string

from unitex.resources import (free_persistent_alphabet,
                              free_persistent_dictionary, free_persistent_fst2,
                              load_persistent_alphabet,
                              load_persistent_dictionary, load_persistent_fst2)
from unitex.io import cp, ls, mv, rm, exists, rmdir, UnitexFile
from unitex.tools import UnitexConstants, normalize, locate, tokenize, dico, concord

class BioMedConcept(object):
    '''Basic BioMedicalConcept object'''
    def __init__(self, umid, label, onto, context):
        self.umid = umid
        self.label = label
        self.onto = onto
        self.context = context

    def serialize(self):
        '''returns serialized object'''
        return {'umid': self.umid, 'label': self.label,
                'onto': self.onto, 'context': self.context}

def load_resources(options):
    '''Loads all persistent resources'''
    print("Loading resources . . . ")
    if options["resources"]["alphabet"] is not None:
        alphabet = load_persistent_alphabet(options["resources"]["alphabet"])
        options["resources"]["alphabet"] = alphabet
    if options["resources"]["alphabet-sorted"] is not None:
        alphabet_sorted = load_persistent_alphabet(options["resources"]["alphabet-sorted"])
        options["resources"]["alphabet-sorted"] = alphabet_sorted
    if options["resources"]["dictionaries"] is not None:
        dictionaries = []
        for dictionary in options["resources"]["dictionaries"]:
            dictionary = load_persistent_dictionary(dictionary)
            dictionaries.append(dictionary)
        options["resources"]["dictionaries"] = dictionaries
    print("Loading resources . . . Done!!")

def load_grammars(options):
    '''Load persistent grammar'''
    print("Loading drug and disease grammars")
    # Load drug, dis from sentence, replace yaml variables for now
    # TO-DO Add variables to load custom graphs in python-unitex project
    if options["resources"]["sentence"] is not None:
        sentence = load_persistent_fst2(options["resources"]["sentence"])
        options["resources"]["sentence"] = sentence
    if options["resources"]["replace"] is not None:
        replace = load_persistent_fst2(options["resources"]["replace"])
        options["resources"]["replace"] = replace
    print("Loading resources . . . Done!!")

def free_resources(options):
    '''Frees all persistent resources'''
    if options["resources"]["alphabet"] is not None:
        free_persistent_alphabet(options["resources"]["alphabet"])
    if options["resources"]["alphabet-sorted"] is not None:
        free_persistent_alphabet(options["resources"]["alphabet-sorted"])
    if options["resources"]["dictionaries"] is not None:
        for dictionary in options["resources"]["dictionaries"]:
            free_persistent_dictionary(dictionary)

def random_filename(size=8, chars=string.ascii_uppercase + string.digits):
    '''Returns a random string'''
    return ''.join(random.choice(chars) for _ in range(size))

def extract_concepts(text, options):
    '''Extracts concepts from text'''
    print("Extracting concepts from text . . .")
    unifile = UnitexFile()
    name = random_filename()
    txt = "%s%s" % (UnitexConstants.VFS_PREFIX, name + ".txt")
    unifile.open(txt, mode='w')
    unifile.write(unicode(text))
    unifile.close()

    directory, _ = os.path.split(txt)
    snt = os.path.join(directory, "%s.snt" % name)
    snt = "%s%s" % (UnitexConstants.VFS_PREFIX, snt)
    dirc = os.path.join(directory, "%s_snt" % name)

    # Load Alphabet
    alphabet = options["resources"]["alphabet"]
    alphabet_sorted = options["resources"]["alphabet-sorted"]

    # Normalize the text
    kwargs = options["tools"]["normalize"]
    ret = normalize(txt, **kwargs)
    if ret is False:
        sys.stderr.write("[ERROR] Text normalization failed!\n")
        sys.exit(1)

    # Tokenize the text
    kwargs = options["tools"]["tokenize"]
    ret = tokenize(snt, alphabet, **kwargs)
    if ret is False:
        sys.stderr.write("[ERROR] Text tokenization failed!\n")
        sys.exit(1)

    # Apply dictionaries
    if options["resources"]["dictionaries"] is not None:
        dictionaries = options["resources"]["dictionaries"]
        kwargs = options["tools"]["dico"]
        ret = dico(dictionaries, snt, alphabet, **kwargs)
        if ret is False:
            sys.stderr.write("[ERROR] Dictionaries application failed!\n")
            sys.exit(1)

    drug_gram = options["resources"]["sentence"] # sentence = drug
    drug_concepts = get_concepts(dirc, options, snt, alphabet, alphabet_sorted, drug_gram)
    print("Found {} drug concepts".format(len(drug_concepts)))

    dis_gram = options["resources"]["replace"] # sentence = disorder
    dis_concepts = get_concepts(dirc, options, snt, alphabet, alphabet_sorted, dis_gram)
    print("Found {} disease concepts".format(len(dis_concepts)))

    # Clean the Unitex files
    print("Cleaning up files from " + dirc)
    for v_file in ls("%s%s" % (UnitexConstants.VFS_PREFIX, dirc)):
        rm(v_file)
    rm(snt)
    rm(txt)

    return drug_concepts + dis_concepts

def get_concepts(dirc, options, snt, alphabet, alphabet_sorted, grammar):
    '''Retrieve concepts given the text'''
    # Locate pattern
    kwargs = options["tools"]["locate"]
    ret = locate(grammar, snt, alphabet, **kwargs)
    index = "%s%s" % (UnitexConstants.VFS_PREFIX, os.path.join(dirc, "concord.ind"))
    if ret is False or exists(index) is False:
        sys.stderr.write("[ERROR] Locate failed!\n")
        sys.exit(1)

    # Build concordance
    kwargs = options["tools"]["concord"]
    ret = concord(index, alphabet_sorted, **kwargs)
    if ret is False:
        sys.stderr.write("[ERROR] Concord failed!\n")
        sys.exit(1)

    concepts = []
    # Get entities
    con_dict = {}
    onto_dict = {}
    filetr = "%s%s"%(UnitexConstants.VFS_PREFIX, os.path.join(dirc, "dlf"))
    entities = get_text(filetr)
    for entity in entities:
        label = entity.split(',')[0]
        cid = (entity.split(',')[-1]).split('.')[0]
        onto = (entity.split('.')[-1]).split('+')[2]
        con_dict[label.lower()] = cid
        onto_dict[label.lower()] = onto
    filetr = "%s%s"%(UnitexConstants.VFS_PREFIX, os.path.join(dirc, "dlc"))
    entities = get_text(filetr)
    for entity in entities:
        label = entity.split(',')[0]
        cid = (entity.split(',')[-1]).split('.')[0]
        onto = (entity.split('.')[-1]).split('+')[2]
        con_dict[label.lower()] = cid
        onto_dict[label.lower()] = onto
    # Get contexts
    filetr = "%s%s"%(UnitexConstants.VFS_PREFIX, os.path.join(dirc, "concord.txt"))
    contexts = get_text(filetr)
    for context in contexts:
        label = context.split('\t')[1]
        for conc in label.split('/'):
            try:
                onto = onto_dict[conc.lower()]
                bmc = BioMedConcept(con_dict[conc.lower()], conc, onto, context)
                concepts.append(bmc.serialize())
            except KeyError as kerror:
                print("Key Error : {}".format(kerror))
    return concepts

def get_text(filetr):
    '''Get text contents from a file'''
    if exists(filetr) is False:
        sys.stderr.write("[ERROR] File not found\n")
    unfile = UnitexFile()
    unfile.open(filetr, mode='r')
    unfile_txt = unfile.read()
    unfile.close()
    return unfile_txt.splitlines()
