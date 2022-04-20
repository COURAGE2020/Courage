# Constants
ENV = '{ENV}'
REGION = '{REGION}'
PROJECT = '{PROJECT}'
ACCOUNT = '{ACCOUNT}'
ACCOUNT_ENV = '{ACCOUNT_ENV}'
APP = '{APP}'
BASE = '{BASE}'


def _replace_str(source_str, pattern, value):
    return source_str.replace(pattern, value)


def replace_region(source_str, value):
    return _replace_str(source_str, REGION, value)


def replace_env(source_str, value):
    return _replace_str(source_str, ENV, value)


def replace_account_env(source_str, value):
    return _replace_str(source_str, ACCOUNT_ENV, value)


def replace_account(source_str, value):
    return _replace_str(source_str, ACCOUNT, value)


def replace_project(source_str, value):
    return _replace_str(source_str, PROJECT, value)


def replace_app(source_str, value):
    return _replace_str(source_str, APP, value)


def replace_base(source_str, value):
    return _replace_str(source_str, BASE, value)
