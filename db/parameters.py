
from db.firebase import db

# Define a function to accept a param_id and return the corresponding parameter value
def get_param(param_id):
    # Get the parameter value from the Firestore database
    param = db.collection('PARAMETER').where('param_id', '==', param_id).get()[0].to_dict()
    return param['value']

# Define a function to set a value for a parameter
def set_param(param_id, value):
    # Update the parameter value in the Firestore database
    param_ref = db.collection('PARAMETER').where('param_id', '==', param_id).get()[0].reference
    param_ref.update({'value': value})

# Add a new parameter to the database
def add_param(param_id, value):
    # Add a new parameter to the Firestore database using param_id as document name
    db.collection('PARAMETER').document(param_id).set({
        'param_id': param_id,
        'value': value
    })

# A function which creates or updates a parameter
def create_or_update_param(param_id, value):
    # Check if the parameter already exists
    param_ref = db.collection('PARAMETER').where('param_id', '==', param_id)
    existing_params = param_ref.get()
    if existing_params:
        # Update the parameter value
        set_param(param_id, value)
    else:
        # Add a new parameter
        add_param(param_id, value)