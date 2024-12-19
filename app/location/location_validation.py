import re

from marshmallow import Schema, fields, validates, ValidationError, validates_schema
from passlib.handlers.pbkdf2 import pbkdf2_sha256

from db_connection import database_connect_mongo

ALPHABET_ERROR_MESSAGE = "Please enter alphabet only for name field"
name_check = "^[a-zA-Z\s]*\S$"
password_check = "^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$"


class CountryRegistrationSchema(Schema):
    status = fields.Str(required=True)
    created_at = fields.DateTime(format="%Y-%m-%d %H:%M:%S", required=True)
    updated_at = fields.DateTime(format="%Y-%m-%d %H:%M:%S", allow_none=True)
    password = fields.Str(required=True)
    country = fields.Str(required=True)
    email_id = fields.Email(required=True)

    @validates('country')
    def validate_country(self, value):
        db = database_connect_mongo()
        db1 = db["location"]
        if db1.count_documents({"country": {"$eq": value}}, collation={"locale": "en", "strength": 2}) > 0:
            raise ValidationError("This country already added")

        if not re.match(name_check, value):
            raise ValidationError(ALPHABET_ERROR_MESSAGE)

    @validates('password')
    def validate_password(self, value):
        if not re.match(password_check, value):
            raise ValidationError("Please enter Minimum eight characters, at least one letter, one number and one "
                                  "special character for password field")

    @validates('email_id')
    def validate_email_id(self, value):
        db = database_connect_mongo()
        db1 = db["location"]
        db2 = db["employee_registration"]
        if db1.count_documents({"email_id": {"$eq": value}}, collation={"locale": "en", "strength": 2}) > 0:
            raise ValidationError("Email already exists")
        if db2.count_documents({"email_id": {"$eq": value}}, collation={"locale": "en", "strength": 2}) > 0:
            raise ValidationError("An employee with this email already exists")


class RegionRegistrationSchema(Schema):
    status = fields.Str(required=True)
    created_at = fields.DateTime(format="%Y-%m-%d %H:%M:%S", required=True)
    updated_at = fields.DateTime(format="%Y-%m-%d %H:%M:%S", allow_none=True)
    password = fields.Str(required=True)
    country = fields.Str(required=True)
    region = fields.Str(required=True)
    email_id = fields.Email(required=True)

    @validates_schema
    def validate_region(self, data, **kwargs):
        db = database_connect_mongo()
        db1 = db["location"]
        if db1.count_documents({"country": data['country'], "region": data['region']}):
            raise ValidationError({"region": ["This region already added under this country"]})

        if not re.match(name_check, data['region']):
            raise ValidationError(ALPHABET_ERROR_MESSAGE)

    @validates('email_id')
    def validate_email_id(self, value):
        db = database_connect_mongo()
        db1 = db["location"]
        db2 = db["employee_registration"]
        if db1.count_documents({"email_id": {"$eq": value}}, collation={"locale": "en", "strength": 2}) > 0:
            raise ValidationError("Email already exists")
        if db2.count_documents({"email_id": {"$eq": value}}, collation={"locale": "en", "strength": 2}) > 0:
            raise ValidationError("An employee with this email already exists")

    @validates('password')
    def validate_password(self, value):
        if not re.match(password_check, value):
            raise ValidationError(
                "Please enter Minimum eight characters, at least one letter, one number and one special character for "
                "password field")

    @validates('country')
    def validate_country(self, value):
        db = database_connect_mongo()
        db1 = db["location"]
        if db1.count_documents({"country": {"$eq": value}}, collation={"locale": "en", "strength": 2}) == 0:
            raise ValidationError("Country not found")


class SubRegionRegistrationSchema(Schema):
    status = fields.Str(required=True)
    created_at = fields.DateTime(format="%Y-%m-%d %H:%M:%S", required=True)
    updated_at = fields.DateTime(format="%Y-%m-%d %H:%M:%S", allow_none=True)
    password = fields.Str(required=True)
    country = fields.Str(required=True)
    region = fields.Str(required=True)
    sub_region = fields.Str(required=True)
    email_id = fields.Email(required=True)

    @validates_schema
    def validate_sub_region(self, data, **kwargs):
        db = database_connect_mongo()
        db1 = db["location"]
        if db1.count_documents(
                {"country": data['country'], "region": data['region'], "sub_region": data['sub_region']}):
            raise ValidationError({"sub_region": ["This sub-region already added under this region"]})

        if not re.match(name_check, data['sub_region']):
            raise ValidationError(ALPHABET_ERROR_MESSAGE)

    @validates('password')
    def validate_password(self, value):
        if not re.match(password_check, value):
            raise ValidationError(
                "Please enter Minimum eight characters, at least one letter, one number and one special character for "
                "password field")

    @validates('email_id')
    def validate_email_id(self, value):
        db = database_connect_mongo()
        db1 = db["location"]
        db2 = db["employee_registration"]
        if db1.count_documents({"email_id": {"$eq": value}}, collation={"locale": "en", "strength": 2}) > 0:
            raise ValidationError("Email already exists")
        if db2.count_documents({"email_id": {"$eq": value}}, collation={"locale": "en", "strength": 2}) > 0:
            raise ValidationError("An employee with this email already exists")

    @validates('country')
    def validate_country(self, value):
        db = database_connect_mongo()
        db1 = db["location"]
        if db1.count_documents({"country": {"$eq": value}}, collation={"locale": "en", "strength": 2}) == 0:
            raise ValidationError("Country not found")

    @validates('region')
    def validate_region(self, value):
        db = database_connect_mongo()
        db1 = db["location"]
        if db1.count_documents({"region": {"$eq": value}}, collation={"locale": "en", "strength": 2}) == 0:
            raise ValidationError("Region not found")

    @validates_schema
    def validate_region(self, data, **kwargs):
        db = database_connect_mongo()
        db1 = db["location"]
        if db1.count_documents({"country": data['country'], "region": data['region']}) == 0:
            raise ValidationError({"region": ["This region not added under this country"]})


class LoginSchema(Schema):
    email_id = fields.Email(required=True)
    password = fields.Str(required=True)

    @validates_schema
    def validate_login(self, data, **kwargs):
        db = database_connect_mongo()
        db1 = db["location"]
        employee = db1.find_one({"email_id": {"$eq": data['email_id']}}, collation={"locale": "en", "strength": 2})

        if employee is not None:
            if not pbkdf2_sha256.verify(data['password'], employee['password']):
                raise ValidationError("Incorrect password")

        else:
            raise ValidationError({"email_id": ["Email does not exist"]})


country_registration_schema = CountryRegistrationSchema()
region_registration_schema = RegionRegistrationSchema()
sub_region_registration_schema = SubRegionRegistrationSchema()
login_schema = LoginSchema()