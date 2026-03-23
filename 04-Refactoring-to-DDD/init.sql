-- Initial database schema for attendee registration application

CREATE TABLE IF NOT EXISTS attendees (
    id BIGSERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    street_address VARCHAR(255) NOT NULL,
    bus VARCHAR(50),
    postal_code VARCHAR(20) NOT NULL,
    town_or_municipality VARCHAR(100) NOT NULL,
    registration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(20) DEFAULT 'REGISTERED' CHECK (status IN ('REGISTERED', 'CONFIRMED', 'CANCELLED'))
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_attendees_email ON attendees(email);
CREATE INDEX IF NOT EXISTS idx_attendees_registration_date ON attendees(registration_date);
CREATE INDEX IF NOT EXISTS idx_attendees_status ON attendees(status);

-- Insert some sample data for testing
INSERT INTO attendees (email, first_name, last_name, street_address, bus, postal_code, town_or_municipality, status) VALUES
('john.doe@example.com', 'John', 'Doe', '123 Main Street', 'Apt 4B', '12345', 'Springfield', 'REGISTERED'),
('jane.smith@example.com', 'Jane', 'Smith', '456 Oak Avenue', NULL, '67890', 'Shelbyville', 'CONFIRMED'),
('bob.johnson@example.com', 'Bob', 'Johnson', '789 Pine Road', 'Suite 100', '11111', 'Capital City', 'REGISTERED')
ON CONFLICT (email) DO NOTHING;