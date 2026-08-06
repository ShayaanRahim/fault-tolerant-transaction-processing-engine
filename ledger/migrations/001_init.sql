
-- ==== 001_init.sql - full schema for idempotent ledger =====
-- ===========================================================

-- account classification, it creates a system for account types
-- to be one of three string types, this makes it so that 
-- we have a sign convention for our balance, and represent
-- a funding source

CREATE TYPE account_type as ENUM ('asset', 'liability', 'equity');

CREATE TYPE transaction_status as ENUM ('pending', 'committed', 'failed'); -- only three types of transactions

-- this is the accounts table. has no balance column so that 
-- there isn't diverging sources of truth because ledger also
-- keeps track of transactions. Balance is from storing 
-- ledger entries
CREATE TABLE accounts (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(), -- automatically generates random UUID that is secure 
    name        TEXT NOT NULL, -- mandates you put text
    type        account_type NOT NULL DEFAULT 'liability', -- default account type is liability since most accounts are user accounts
    created_at  TIMESTAMPTZ NOT NULL DEFAULT now() -- timestamp with time zone
);

-- this is the transactions table responsible for stopping
-- dual entries or double requests for the same transaction
CREATE TABLE transactions (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    idempotency_key TEXT UNIQUE NOT NULL,
    status          transaction_status NOT NULL DEFAULT 'pending',
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- ledger entries
-- source of truth for transactions. every transaction produces two or
-- more rows whose amounts sum to exactly zero.
-- NUMERIC(19, 4) -- dont use FLOAT for money.
CREATE TABLE ledger_entries (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    transaction_id  UUID NOT NULL REFERENCES transactions(id),
    account_id      UUID NOT NULL REFERENCES accounts(id),
    amount          NUMERIC(19,4) NOT NULL CHECK (amount <> 0),
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- balance queries filter by account_id
CREATE INDEX idx_ledger_entries_account ON ledger_entries(account_id);
CREATE INDEX idx_ledger_entries_txn     ON ledger_entries(transaction_id);

-- idempotency requests
-- caches response for a given key so a retry returns 
-- original result instead of re-executing
CREATE TABLE idempotency_requests (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    key             TEXT UNIQUE NOT NULL,
    endpoint        TEXT NOT NULL,
    request_hash    TEXT NOT NULL,
    repsonse_status INT,
    response_body   JSONB,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- outbox events
-- written inside the same db transaction as the ledger entries
-- then drained by separate worker
CREATE TABLE outbox_events (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    transaction_id  UUID NOT NULL REFERENCES transactions(id),
    event_type      TEXT NOT NULL,
    payload         JSONB NOT NULL,
    published       BOOLEAN NOT NULL DEFAULT FALSE,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX idx_outbox_unpublishd ON outbox_events(published, created_at)
    WHERE published = FALSE;

