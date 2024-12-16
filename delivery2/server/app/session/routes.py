# api path: /api/v1/sessions/ 
from . import session_bp
from flask import request, jsonify, current_app, abort
from server.organizations_db.organizations_db import OrganizationsDB
from utils.session import decapsulate_session_data, encapsulate_session_data

@session_bp.route('/roles', methods=['POST'])
def assume_session_role():
    plaintext, organization_name, username, msg_id, session_id, derived_key_hex = decapsulate_session_data(request.get_json(), current_app.sessions)

    # Update session msg_id
    msg_id += 1
    current_app.sessions[session_id]['msg_id'] = msg_id

    ############################## Check Active User ##############################
    user_data = current_app.organization_db.retrieve_subject(organization_name, username)
    
    if user_data['state'] != 'active':
        response = {'error': 'User is not active'}
        data = encapsulate_session_data(response, session_id, derived_key_hex, msg_id)
        return jsonify(data), 403
    
    ############################ Logic of the endpoint ############################
    plaintext_role = plaintext.get('role')

    # Check in the database if the username has that role in that organization
    has_role = current_app.organization_db.check_user_role(organization_name, username, plaintext_role)

    if has_role == False:
        response = {'error': 'User does not have the role in the organization'}
    else:    
        current_app.sessions[session_id]['roles'] = [plaintext_role]

        response = {
            'state': f'Role "{plaintext_role}" assumed successfully'
        }

    ###############################################################################

    data = encapsulate_session_data(
        response,
        session_id,
        derived_key_hex,
        msg_id
    )

    return jsonify(data), 200 if has_role else 403

@session_bp.route('/roles', methods=['DELETE'])
def drop_session_role():
    plaintext, organization_name, username, msg_id, session_id, derived_key_hex = decapsulate_session_data(request.get_json(), current_app.sessions)

    # Update session msg_id
    msg_id += 1
    current_app.sessions[session_id]['msg_id'] = msg_id

    ############################## Check Active User ##############################
    user_data = current_app.organization_db.retrieve_subject(organization_name, username)
    
    if user_data['state'] != 'active':
        response = {'error': 'User is not active'}
        data = encapsulate_session_data(response, session_id, derived_key_hex, msg_id)
        return jsonify(data), 403
    
    ############################ Logic of the endpoint ############################
    plaintext_role = plaintext.get('role')

    # Check the existence of the role within the current session
    has_role = plaintext_role in current_app.sessions[session_id].get('roles')

    if has_role == False:
        response = {'error': 'User does not have the role in the organization'}
    else:
        current_app.sessions[session_id]['roles'].remove(plaintext_role)

        response = {
            'state': f'Role "{plaintext_role}" dropped successfully'
        }

    ###############################################################################

    data = encapsulate_session_data(
        response,
        session_id,
        derived_key_hex,
        msg_id
    )

    return jsonify(data), 200 if has_role else 403


@session_bp.route('/roles', methods=['GET'])
def list_session_roles():
    # TODO: Logic to list session roles
    plaintext, organization_name, username, msg_id, session_id, derived_key_hex = decapsulate_session_data(request.get_json(), current_app.sessions)

    # Update session msg_id
    msg_id += 1
    current_app.sessions[session_id]['msg_id'] = msg_id

    ############################## Check Active User ##############################
    user_data = current_app.organization_db.retrieve_subject(organization_name, username)
    
    if user_data['state'] != 'active':
        response = {'error': 'User is not active'}
        data = encapsulate_session_data(response, session_id, derived_key_hex, msg_id)
        return jsonify(data), 403
    
    ############################ Logic of the endpoint ############################
    roles = current_app.sessions[session_id].get('roles')

    current_app.logger.info(f'Roles in session: {roles}')

    response = {
        'roles': roles
    }

    ###############################################################################

    data = encapsulate_session_data(
        response,
        session_id,
        derived_key_hex,
        msg_id
    )

    return jsonify(data), 200


# @session_bp.route('/roles', methods=['DELETE'])
# def refresh_session_keys():
#     # TODO: Logic to release session roles
#     ...
