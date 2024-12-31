from .database import get_session
from .models import Order


def create_order(
    client_id,
    coinbase_id,
    transaction_type,
    product,
    price,
    time_of_order,
    base_currency_balance_before_order,
    quote_currency_balance_before_order,
    base_currency_balance_after_order,
    quote_currency_balance_after_order,
    additional_info,
):
    with get_session() as session:
        order = Order(
            client_id=client_id,
            coinbase_id=coinbase_id,
            transaction_type=transaction_type,
            product=product,
            price=price,
            time_of_order=time_of_order,
            base_currency_balance_before_order=base_currency_balance_before_order,
            quote_currency_balance_before_order=quote_currency_balance_before_order,
            base_currency_balance_after_order=base_currency_balance_after_order,
            quote_currency_balance_after_order=quote_currency_balance_after_order,
            additional_info=additional_info,
        )
        session.add(order)
        session.commit()
        order_id = order.id

    return order_id


def get_order(id):
    with get_session() as session:
        query = session.query(Order).get(id)

    return query


def get_latest_order():
    session = get_session()
    res = session.query(Order).order_by(Order.time_of_order.desc()).first()
    return res
