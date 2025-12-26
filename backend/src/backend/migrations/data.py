from quart_db import Connection


async def execute(connection: Connection) -> None:
    await connection.execute(
        """INSERT INTO members (email, password_hash)
                VALUES ('member@tozo.dev',
                        '$argon2id$v=19$m=65536,t=3,p=4$WgK+UFbvbwN8fC1WsnooSw$22COuZv9O43uvgSpYOl18K0uUnT7pp0pRfILIfTHr/c'
           )"""
    )
    await connection.execute(
        """INSERT INTO todos (member_id, task)
                VALUES (1, 'Test Task')"""
    )
