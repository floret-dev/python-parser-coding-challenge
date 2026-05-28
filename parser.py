from trp import Document
from trp.trp2 import TDocumentSchema, TDocument
from handlers import date, distributor, fee, number, retailer, total, type
from common import store
import argparse
import json
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
    document_data = {}

    for page in trp_doc.pages:
        document_data['distributor'] = distributor.parse(page)
        document_data['invoiceNumber'] = number.parse(page)
        document_data['invoiceDate'] = date.parse(page)
        document_data['invoiceTotal'] = total.parse(page)
        document_data['invoiceFee'] = fee.parse(page)
        document_data['retailer'] = retailer.parse(page)
        document_data['type'] = type.parse(page)

    return document_data


def invoke(folder_name):
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
          prog='parser.py',
          description='This utility program generates textract fixtures using the textract expense and document api'
      )

    argument_parser.add_argument('testfile_directory', help='The directory containing the test file to process')
    arguments = argument_parser.parse_args()
    directories = arguments.testfile_directory.split(',')
    for directory in directories:
        store.set_object('current_directory', directory)
        results = invoke(directory)
        output_path = f'test-files/{directory}/parser-output.json'
        with open(output_path, 'w') as output:
            output.write(json.dumps(results, indent=4))