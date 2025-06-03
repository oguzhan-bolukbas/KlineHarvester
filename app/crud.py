from sqlalchemy.orm import Session
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.exc import SQLAlchemyError
from models import Kline
from datetime import datetime, timezone

def insert_klines(session: Session, symbol: str, interval: str, klines: list, batch_size: int = 5000):
    rows = []
    for k in klines:
        rows.append({
            'symbol': symbol,
            'interval': interval,
            'open_time': datetime.fromtimestamp(k[0]/1000.0, tz=timezone.utc),
            'open': k[1],
            'high': k[2],
            'low': k[3],
            'close': k[4],
            'volume': k[5],
            'close_time': datetime.fromtimestamp(k[6]/1000.0, tz=timezone.utc),
            'quote_asset_volume': k[7],
            'number_of_trades': k[8],
            'taker_buy_base_asset_volume': k[9],
            'taker_buy_quote_asset_volume': k[10],
        })
    if not rows:
        return
    try:
        for i in range(0, len(rows), batch_size):
            batch = rows[i:i+batch_size]
            stmt = pg_insert(Kline.__table__).values(batch)
            stmt = stmt.on_conflict_do_nothing(index_elements=['symbol', 'interval', 'open_time'])
            session.execute(stmt)
            session.commit()
    except SQLAlchemyError as e:
        session.rollback()
        print(f"DB insert error: {e}")
