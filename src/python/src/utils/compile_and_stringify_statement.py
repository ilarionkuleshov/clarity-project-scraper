from sqlalchemy.dialects import mysql


def compile_and_stringify_statement(stmt):
    return str(
        stmt.compile(
            compile_kwargs={"literal_binds": True},
            dialect=mysql.dialect()
        )
    )
