from uuid import UUID
from fastapi import APIRouter, HTTPException
from app.db import get_conn
from app.schemas import AccountCreate, AccountOut

router = APIRouter(prefix="/accounts", tags=["accounts"])

BALANCE_SQL = """
    SELECT COALESCE(SUM(amount), 0) AS balance
    FROM ledger_entries
    WHERE account_id = %s
"""

# takes a validated request body, inserts new row into accounts
# and returns it back to the client with a starting balance of 0 
@router.post("", response_model=AccountOut, status_code=201)
def create_account(payload: AccountCreate):
    with get_conn() as conn:
        row = conn.execute(
            """
            INSERT INTO accounts (name, type)
            VALUES (%s, %s)
            RETURNING id, name, type::text, created_at
            """,
            (payload.name, payload.type),
        ).fetchone()
    return AccountOut(**row, balance=0)

# looks up once specific accoungt by its ID, returns
# a 404 if it doesnt exist, else computes its real balance from
# the ledger and returns the full account
@router.get("/{account_id}", response_model=AccountOut)
def get_account(account_id: UUID):
    with get_conn() as conn:
        acct = conn.execute(
            "SELECT id, name, type::text, created_at FROM accounts WHERE id = %s",
            (account_id,),
        ).fetchone()

        if acct is None:
            raise HTTPException(status_code=404, detail="account not found")

        bal = conn.execute(BALANCE_SQL, (account_id,)).fetchone()

    return AccountOut(**acct, balance=bal["balance"])

# returns every account along with its balance, 
# computed efficiently in a single database query rather than
# one query per account
@router.get("", response_model=list[AccountOut])
def list_accounts():
    with get_conn() as conn:
        rows = conn.execute(
            """
            SELECT  a.id,
                    a.name,
                    a.type::text,
                    a.created_at,
                    COALESCE(SUM(le.amount), 0) AS balance
            FROM accounts a 
            LEFT JOIN ledger_entries le ON le.account_id = a.id
            GROUP BY a.id
            ORDER BY a.created_at DESC
            """
        ).fetchall()
    return [AccountOut(**r) for r in rows]

        