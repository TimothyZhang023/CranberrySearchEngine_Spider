#!/usr/bin/python
#-*-coding:utf-8-*-

"""
    This file is for initiate mongodb situation
    
    When you want to save book file in file system,then you don't need sharding cluster,that the database design is:
    database:books_fs
    collections:book_detail
    fields:
        book_detail:
            book_name
            alias_name:vector
            author:vector
            book_description:string
            book_covor_image_path:string
            book_covor_image_url:string
            book_download:vector
            book_file_url:string
            book_file:string
            original_url:string
            update_time:datetime
    index:
        book_name
        alias_name
        author

    So what this do is to delete books_fs is it has existed,and create index for it.
"""

import types
from pymongo import MongoClient
from pymongo import ASCENDING, DESCENDING

DATABASE_NAME = "html"
client = None
DATABASE_HOST = "localhost"
DATABASE_PORT = 27017
INDEX = { \
    #collection
    'html_detail': \
        { \
            'docId': {'name': 'docId', 'unique': True},
            'url': {'name': 'url'},
            'update_time': {'name': 'update_time'},
        } \
    }


def drop_database(name_or_database):
    if name_or_database and client:
        client.drop_database(name_or_database)


def create_index():
    """
        create index for books_fs.book_detail
    """
    for k, v in INDEX.items():
        for key, kwargs in v.items():
            client[DATABASE_NAME][k].ensure_index(list(key) if type(key) == types.TupleType else key, **kwargs)


def create_test_data():
    html_detail = {
        'docId': "123456",
        'url': "http://www.zts1993.com",
        'content': "http://www.zts1993.com",
        'encoding': "http://www.zts1993.com",
        'update_time': "http://www.zts1993.com",
    }
    result = client[DATABASE_NAME]['html_detail'].insert_one(html_detail)
    print result

    client[DATABASE_NAME]['html_detail'].delete_one({'docId': "123456"})

    html_detail = {
        'docId': "123456",
        'url': "http://www.zts1993.com",
        'content': "http://www.zts1993.com",
        'encoding': "http://www.zts1993.com",
        'update_time': "http://www.zts1993.com",
    }
    result = client[DATABASE_NAME]['html_detail'].insert_one(html_detail)
    print result


if __name__ == "__main__":
    client = MongoClient(DATABASE_HOST, DATABASE_PORT)
    drop_database(DATABASE_NAME)
    create_index()
    create_test_data()
