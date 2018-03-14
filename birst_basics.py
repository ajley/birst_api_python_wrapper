#!/usr/local/bin/python3

"""This file builds functions on top of the 'birst_api_base_calsl' file and performs basic actions against
 Birst's CommandWebService.asmx

Start by calling get_session with appropriate url (<birst_server>/CommandWebService.asmx?wsdl) with valid
admin credentials. It will return a namedtuple containing a Zeep Client object and security token

contact a@ley.io to let me know of issues or tell me that I'm doing things wrong.
"""

from birst_api_base_calls import *
from collections import namedtuple
import getpass

# set up 'new_session' named tuple
new_session = namedtuple('new_session', 'client token')


def get_session(uri, user, passwd=''):
    """takes in the uri to wsdl, username, and password and returns a session namedtuple that can then be used by
    other functions. Password is optionally, if it's not present, user will be asked to enter it"""
    if not passwd:
        passwd = getpass.getpass("Enter admin password: ")
    try:
        client = Client(uri)
    except Exception as e:
        logging.error("Couldn't get wsdl:" + repr(e))
        return 1
    try:
        sec_token = login(client, user, passwd)
        if not sec_token:
            raise Exception('token not returned correctly')
        session = new_session(client, sec_token)
        return session
    except Exception as e:
        logging.error(repr(e))
        return 1


def update_space_properties(session, space_id, **kargs):
    """generic way to update the space properties available. Tested against UsageTracking and UseNewDashboards
    properties"""
    if kargs is None:
        return "you need to specify the properties to set"
    try:
        properties = get_space_properties(session, space_id=space_id)
    except Exception as e:
        logging.error("Can't get the space properties for {}".format(space_id) + repr(e))
    try:
        for k, v in kargs.items():
            if k in properties:
                properties[k] = v
            else:
                logging.error("Property '{}' does't exist. you sent: {}".format(k, kargs))
                return "property '{}' doesn't exist. you sent: {}".format(k, kargs)
        result = set_space_properties(session, space_id=space_id, space_properties=properties)
        return result
    except Exception as e:
        logging.error("Can't set the space properties for {}".format(space_id) + repr(e))
        exit(1)


def update_group_acls(session, space_id, group_name, *args):
    try:
        available_acls = get_acls(session)
    except Exception as e:
        logging.error("Can't get available acls : {}".format(repr(e)))
        return 1
    if args is not None:
        for arg in args:
                if arg not in available_acls:
                    logging.error("You sent an ACL that doesn't exist: {}".format(arg))
                    return 1
    try:
        logging.info("getting current acls for group: {}".format(group_name))
        current_acls = get_group_acls(session, space_id, group_name)
    except Exception as e:
        logging.error("error getting current acls for {}: ".format(group_name) + repr(e))
        return 1
    try:
        if args is None and current_acls is None:
            logging.info("group {} didn't have any acls, and you sent None in the call"
                         ", no change was made".format(group_name))
        elif args is None:
            for acl in current_acls:
                remove_acl_from_group(session, space_id, group_name, acl)
                logging.info("all acls removed from {}".format(group_name))
        elif current_acls is None:
            for acl in args:
                add_acl_to_group(session, space_id, group_name, acl)
        else:
            for acl in current_acls:
                if acl not in args:
                    remove_acl_from_group(session, space_id, group_name, acl)
            for acl in args:
                if acl not in current_acls:
                    add_acl_to_group(session, space_id, group_name, acl)
        logging.info("acls updated to {} fro group: {}".format(args, group_name))
        return
    except Exception as e:
        logging.error("Couldn't update acls for group: {}:  current acls: {}, acls to set"
                      ": {} : {}".format(group_name, current_acls, args, repr(e)))
        return 1



