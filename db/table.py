import sqlalchemy

metadata = sqlalchemy.MetaData()

users = sqlalchemy.Table(
    "users",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.String,unique=True, primary_key=True),
    sqlalchemy.Column("username", sqlalchemy.String, unique=True, primary_key=True),
    sqlalchemy.Column("email", sqlalchemy.String),
    sqlalchemy.Column("password", sqlalchemy.String),
    sqlalchemy.Column("confirm_password", sqlalchemy.String),
    sqlalchemy.Column("dateofbirth", sqlalchemy.String),
    sqlalchemy.Column("first_name", sqlalchemy.String),
    sqlalchemy.Column("last_name", sqlalchemy.String),
    sqlalchemy.Column("phone", sqlalchemy.String),
    sqlalchemy.Column("created_at", sqlalchemy.String),
    sqlalchemy.Column("status", sqlalchemy.String)
)
