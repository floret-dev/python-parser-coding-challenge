from common import store
from trp import Document
from trp.trp2 import TDocumentSchema, TDocument
from handlers import irregulars
import argparse
import json
import re
import sys

def prune_rotation_angle(textract_output):
    '''
    # A textract update caused amazon trp package to be out of date.
    # This function is a band-aid until such time that we can remove our
    # dependency on the trp library. We should do that *soon*
    '''
    for block in textract_output['Blocks']:
        if 'RotationAngle' in block['Geometry']:
            del block['Geometry']['RotationAngle']


def parse_trp_doc(textract_output):
    prune_rotation_angle(textract_output)
    t_doc: TDocument = TDocumentSchema().load(textract_output)
    trp_doc = Document(TDocumentSchema().dump(t_doc))
    return trp_doc


def process_analysis(textract_output):
    trp_doc = parse_trp_doc(textract_output) # Don't worry about this part
    first_page = trp_doc.pages[0]
    document_data = {}

    if irregulars.is_irregular_file(trp_doc):
        document_data['distributor'] = irregulars.get_irregular_distributor(first_page)
        document_data['invoiceNumber'] = irregulars.get_irregular_invoice_number(first_page)
        document_data['invoiceDate'] = irregulars.get_irregular_invoice_date(first_page)
        document_data['invoiceTotal'] = irregulars.get_irregular_invoice_total(first_page)
        document_data['type'] = irregulars.get_irregular_issue_type(first_page)
    else:
        # Imagine this is where the rest of the parser goes
        pass

    return [document_data]


def invoke(folder_name):
    store.clear()
    input_path = f'test-files/{folder_name}/textract-output.json'
    textract_output = None
    with open(input_path) as f:
        textract_output = json.load(f)

    if textract_output is None:
        print(f'CRITICAL: No deduction file could be found with filename {folder_name}')
        sys.exit(1)

    document_data = process_analysis(textract_output)

    return {'document': document_data}


if __name__ == '__main__':
    argument_parser = argparse.ArgumentParser(
          prog='generate.py',
          description='This utility program generates textract fixtures using the textract expense and document api'
      )

    argument_parser.add_argument('filename')
    arguments = argument_parser.parse_args()
    extless_filename = arguments.filename.split('.')[0]
    invoke(extless_filename)