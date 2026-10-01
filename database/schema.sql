CREATE TABLE IF NOT EXISTS model_versions (
    id BIGSERIAL PRIMARY KEY,
    version VARCHAR(80) UNIQUE NOT NULL,
    dataset_hash VARCHAR(64) NOT NULL,
    hyperparameters JSONB NOT NULL,
    metrics JSONB NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS alerts (
    id BIGSERIAL PRIMARY KEY,
    symbol VARCHAR(30) NOT NULL,
    event_time TIMESTAMPTZ NOT NULL,
    anomaly_score DOUBLE PRECISION NOT NULL,
    confidence DOUBLE PRECISION NOT NULL,
    features JSONB NOT NULL,
    explanation JSONB NOT NULL,
    status VARCHAR(30) NOT NULL DEFAULT 'PENDING',
    model_version VARCHAR(80) NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_alerts_symbol_time
ON alerts(symbol, event_time DESC);

CREATE TABLE IF NOT EXISTS feedback (
    id BIGSERIAL PRIMARY KEY,
    alert_id BIGINT REFERENCES alerts(id),
    label VARCHAR(30) NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
