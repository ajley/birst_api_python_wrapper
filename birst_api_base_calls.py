#!/usr/local/bin/python3

"""Birst API - Basic Calls - work in progress
This file contains wrappers for the basic api calls at CommandWebServer.asmx

To call Birst apis this uses the Zeep library.
contact a@ley.io to let me know of issues or tell me that I'm doing things wrong.
"""

from zeep import Client
import logging
# from logging.handlers import TimedRotatingFileHandler

# Set up logging info
# TODO: add in rotating logs

log_file = 'birst_api.log'

logging.basicConfig(
    filename=log_file,
    level=logging.ERROR,
    format="%(asctime)s:%(levelname)s:%(message)s"
)


def login(client, user, passwd):
    """log in to provided client and return the access token to perform further api calls"""
    logging.debug("Attempting to log in as '{}'".format(user))
    try:
        login_token = client.service.Login(user, passwd)
        return login_token
    except Exception as e:
        logging.error("Error logging in:" + repr(e))


def logout(session):
    result = session.client.service.Logout(session.token)
    if result:
        return result
    else:
        return "You have logged out successfully"


def list_spaces(session):
    result = session.client.service.listSpaces(session.token)
    return result


def get_space_id(session, space_name):
    spaces = list_spaces(session)
    try:
        result = next(space['id'] for space in spaces if space['name'] == space_name)
        return result
    except Exception as e:
        logging.error("can't get space id for {}:".format(space_name) + repr(e))


def get_space_properties(session, space_id):
    properties = session.client.service.GetSpaceProperties(token=session.token, spaceID=space_id)
    return properties


def set_space_properties(session, space_id, space_properties):
    result = session.client.service.SetSpaceProperties(token=session.token, spaceID=space_id,
                                                       spaceProperties=space_properties)
    return result


def list_groups_in_space(session, space_id):
    try:
        result = session.client.service.listGroupsInSpace(token=session.token, spaceID=space_id)
        return result
    except Exception as e:
        Exception("Can't get groups for {}".format(space_id) + repr(e))


def list_custom_subject_areas(session, space_id):
    result = session.client.service.listCustomSubjectAreas(token=session.token, spaceID=space_id)
    return result


def get_subject_area(session, space_id, csa):
    csa = session.client.service.getSubjectAreaContent(token=session.token, spaceID=space_id, name=csa)
    return csa


def get_acls(session):
    result = session.client.service.getAvailableACLs(session.token)
    return result


def get_group_acls(session, space_id, group_name):
    result = session.client.service.listGroupAclsInSpace(token=session.token, spaceID=space_id, groupName=group_name)
    return result


def get_space_processing_engine_version(session, space_id):
    result = session.client.service.getSpaceProcessEngineVersion(token=session.token, spaceID=space_id)
    return result
