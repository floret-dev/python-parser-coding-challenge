import importlib

from common import constants, store

irregulars = ['unfi_chargeback']
irregular_modules = {x: importlib.import_module('handlers.irregular_files.'+x) for x in irregulars}

def is_irregular_file(document=None):
    if store.contains_object(constants.store_key.file_type):
        file_type = store.get_object(constants.store_key.file_type)
        if file_type:
            return True
        return False

    for elem in irregulars:
        if irregular_modules[elem].matches(document):
            file_type = elem
            store.set_object(constants.store_key.file_type, file_type)
            return True
    store.set_object(constants.store_key.file_type, False)
    return False


def get_file_type():
    if store.contains_object(constants.store_key.file_type):
        return store.get_object(constants.store_key.file_type)


def get_irregular_invoice_number(first_page):
    file_type = store.get_object(constants.store_key.file_type)
    if file_type:
        return irregular_modules[file_type].get_invoice_number(first_page)


def get_irregular_invoice_date(first_page):
    file_type = store.get_object(constants.store_key.file_type)
    if file_type:
        return irregular_modules[file_type].get_invoice_date(first_page)


def get_irregular_invoice_total(first_page):
    file_type = store.get_object(constants.store_key.file_type)
    if file_type:
        return irregular_modules[file_type].get_invoice_total(first_page)


def get_irregular_distributor(first_page):
    file_type = store.get_object(constants.store_key.file_type)
    if file_type:
        return irregular_modules[file_type].get_distributor(first_page)


def get_irregular_issue_type(first_page):
    file_type = store.get_object(constants.store_key.file_type)
    if file_type:
        return irregular_modules[file_type].get_issue_type(first_page)
