import uuid

from sqlalchemy.dialects.postgresql import UUID, ENUM
import sqlalchemy as sa


metadata = sa.MetaData(schema="bet_maker_content")

NUMBERS_TO_EVENT_STATES_MAPPING = {
    1: 'NEW',
    2: 'FINISHED_WIN',
    3: 'FINISHED_LOOSE',
}

EVENT_STATES_TO_NUMBERS_MAPPING = {
    'NEW': 1,
    'FINISHED_WIN': 2,
    'FINISHED_LOOSE': 3
}


bet_table = sa.Table(
    'bet', metadata,
    sa.Column('id', UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
    sa.Column('event_id', UUID(as_uuid=True)),
    sa.Column('value', sa.Integer),  # При расчётах нужно делить на 100
    sa.CheckConstraint('value > 0', name='check_value_is_positive'),
)

event_table = sa.Table(
    'event', metadata,
    sa.Column('id', UUID(as_uuid=True), primary_key=True),
    sa.Column('state', ENUM('NEW', 'FINISHED_WIN', 'FINISHED_LOOSE', name='event_state')),
    sa.Column('deadline', sa.INTEGER)
)
