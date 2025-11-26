CREATE TABLE areas (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    type TEXT,
    avg_price_per_sqm NUMERIC(12,2),
    past_growth_rate NUMERIC(5,2),
    rental_yield_min NUMERIC(5,2),
    rental_yield_max NUMERIC(5,2),
    liquidity_score NUMERIC(5,2),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE developers (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    tier SMALLINT,
    track_record_score NUMERIC(5,2),
    projects_completed INT,
    on_time_completion_rate NUMERIC(5,2)
);

CREATE TABLE projects (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    area_id INT REFERENCES areas(id),
    developer_id INT REFERENCES developers(id),
    launch_year INT,
    unit_type TEXT,
    status TEXT CHECK (status IN ('off_plan','under_construction','completed')),
    base_price NUMERIC(14,2),
    avg_unit_size_sqm NUMERIC(8,2),
    handover_date DATE
);

CREATE TABLE market_history (
    id SERIAL PRIMARY KEY,
    area_id INT REFERENCES areas(id),
    year INT,
    avg_price_per_sqm NUMERIC(12,2),
    growth_rate NUMERIC(5,2),
    avg_rent_per_sqm NUMERIC(12,2)
);

CREATE TABLE deals (
    id SERIAL PRIMARY KEY,
    project_id INT REFERENCES projects(id),
    unit_type TEXT,
    booking_price NUMERIC(14,2),
    expected_flip_price NUMERIC(14,2),
    strategy TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    planned_exit_date DATE
);

CREATE TABLE payment_plans (
    id SERIAL PRIMARY KEY,
    deal_id INT REFERENCES deals(id),
    due_date DATE,
    amount NUMERIC(14,2),
    payment_type TEXT CHECK (payment_type IN ('booking','installment','handover','fees','other')),
    is_paid BOOLEAN DEFAULT FALSE
);
