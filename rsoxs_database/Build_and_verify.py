import jsonschema, json
from datetime import datetime
import os

my_path = os.path.abspath(os.path.dirname(__file__))
path = os.path.join(my_path, "schema")

with open(os.path.join(path, 'RSoXS_User.json')) as json_data:
    user_schema = json.load(json_data)
with open(os.path.join(path, 'RSoXS_Acquisition.json')) as json_data:
    acquisition_schema = json.load(json_data)
with open(os.path.join(path, 'RSoXS_Institution.json')) as json_data:
    institution_schema = json.load(json_data)
with open(os.path.join(path, 'RSoXS_Holder.json')) as json_data:
    holder_schema = json.load(json_data)
with open(os.path.join(path, 'RSoXS_Location.json')) as json_data:
    location_schema = json.load(json_data)
with open(os.path.join(path, 'RSoXS_Sample.json')) as json_data:
    sample_schema = json.load(json_data)


def build_and_verify_user(*,date_list=[],email='', first_name='User', institution_id=0,
                          last_checkin=datetime.now().strftime('%G-%m-%d-%I:%M:%S %p'), last_name='McUserface',
                          notes='', past_institutions=[], past_proposals=[], phone='555-555-5555',
                          proposal_id=0, user_id=0, username='CantFollowDirections', history=[]):

    user = {'date_checkin_list': date_list,
            'email': email,
            'first_name': first_name,
            'institution_id': institution_id,
            'last_checkin': last_checkin,
            'last_name': last_name,
            'notes': notes,
            'past_institutions': past_institutions,
            'past_proposals': past_proposals,
            'phone': phone,
            'proposal_id': proposal_id,
            'user_id': user_id,
            'username': username,
            'history': history}

    jsonschema.validate(user,user_schema)

    return user


def build_and_verify_sample(*, sample_name='test', sample_desc='testing',
                            date_created=datetime.now().strftime('%G-%m-%d-%I:%M:%S %p'), user_id=0,
                            project_name='testing', institution_id=0, composition=[], density=1, thickness=1,
                            notes='', state='fresh', current_bar_id=0, current_slot_name='blank',
                            past_bar_ids=[], location_id=0, requests=[], history=[]):

    sample = {"sample_name": sample_name,
              "sample_desc": sample_desc,
              "date_created": date_created,
              "user_id": user_id,
              "project_name": project_name,
              "institution_id": institution_id,
              "composition": composition,
              "density": density,
              "thickness": thickness,
              "notes": notes,
              "state": state,
              "current_bar_id": current_bar_id,
              "current_slot_name": current_slot_name,
              "past_bar_ids": past_bar_ids,
              "location_id": location_id,
              "requests": requests,
              "history": history
              }

    jsonschema.validate(sample,sample_schema)
    return sample


def build_and_verify_location(*,location_list=[],display='private', favorite=False,
                              creator_id=0, sample=False, config=False):

    location = {"location_list": location_list,
                "display": display,
                "favorite": favorite,
                "creator_ID": creator_id,
                "sample": sample,
                "config": config
                }

    jsonschema.validate(location,location_schema)
    return location


def build_and_verify_institution(*,institution_id=0, full_name='School of Hard Knocks', short_name='the_street',
                                 notes=''):

    institution = {
        "institution_id": institution_id,
        "full_name": full_name,
        "short_name": short_name,
        "notes": notes
    }

    jsonschema.validate(institution,institution_schema)
    return institution


def build_and_verify_holder(*, holder_id=0, holder_name='Default', primary_user_id=0, primary_institution_id=0,
                            primary_proposal_id=0, date_loaded_list=[datetime.now().strftime('%G-%m-%d-%I:%M:%S %p')],
                            notes='', slots=[], history=[]):

    holder = {
        "holder_id": holder_id,
        "holder_name": holder_name,
        "primary_user_id": primary_user_id,
        "primary_institution_id": primary_institution_id,
        "primary_proposal_id": primary_proposal_id,
        "date_loaded_list": date_loaded_list,
        "notes": notes,
        "slots": slots,
        'history': history
    }

    jsonschema.validate(holder,holder_schema)
    return holder


def build_and_verify_acquisition(*,plan_name='none',detectors=[], motors=[], positions=[], display='private',
                                 favorite=False, creator_id=0):

    acquisition = {
        "plan_name": plan_name,
        "detectors": detectors,
        "motors": motors,
        "positions": positions,
        "display": display,
        "favorite": favorite,
        "creator_id": creator_id
    }

    jsonschema.validate(acquisition,acquisition_schema)
    return acquisition
