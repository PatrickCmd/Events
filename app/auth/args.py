from webargs import fields, validate

user_reg_args = {
    # Reguired arguments and validations
    'email': fields.Str(required=True),
    'password': fields.Str(required=True, validate=validate.Length(6)),
    'first_name': fields.Str(required=True, validate=validate.Length(3)),
    'last_name': fields.Str(required=True, validate=validate.Length(3)),
    'location': fields.Str(required=True),
    'gender': fields.Str(required=True),
    'date_of_birth': fields.Str()
}

login_args = {
    'email': fields.Str(required=True),
    'password': fields.Str(required=True, validate=validate.Length(6))
}
