from sqlalchemy import update
from sqlalchemy.orm import aliased

# Assuming models TableA and TableB are defined with `actor_name` and `city_name` respectively

# Create an alias for TableB (optional for clarity)
TableBAlias = aliased(TableB)

# Update query
stmt = (
    update(TableA)
    .values(city_id=TableBAlias.city_id)
    .where(TableA.actor_name == TableBAlias.city_name)
    .execution_options(synchronize_session="fetch")
)

# Execute the query
with Session(engine) as session:
    session.execute(stmt)
    session.commit()

