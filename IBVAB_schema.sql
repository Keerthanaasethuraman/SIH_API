CREATE EXTENSION IF NOT EXISTS "pgcrypto";

CREATE TABLE IF NOT EXISTS persons (
    person_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    full_name VARCHAR(150) NOT NULL,
    person_code VARCHAR(50) UNIQUE NOT NULL,
    person_type VARCHAR(30) NOT NULL DEFAULT 'AUTHORIZED',
    status VARCHAR(20) NOT NULL DEFAULT 'ACTIVE',
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT persons_type_check
        CHECK (person_type IN ('AUTHORIZED', 'UNAUTHORIZED')),
    CONSTRAINT persons_status_check
        CHECK (status IN ('ACTIVE', 'INACTIVE'))
);

CREATE TABLE IF NOT EXISTS cameras (
    camera_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    camera_name VARCHAR(100) NOT NULL,
    camera_code VARCHAR(50) UNIQUE NOT NULL,
    location VARCHAR(255),
    status VARCHAR(20) NOT NULL DEFAULT 'ACTIVE',
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT cameras_status_check
        CHECK (status IN ('ACTIVE', 'INACTIVE'))
);

CREATE TABLE IF NOT EXISTS detections (
    detection_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    person_id UUID REFERENCES persons(person_id),
    camera_id UUID NOT NULL REFERENCES cameras(camera_id),
    classification VARCHAR(30) NOT NULL,
    confidence DECIMAL(5,2),
    detected_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT detections_confidence_check
        CHECK (confidence >= 0 AND confidence <= 100)
);

CREATE TABLE IF NOT EXISTS person_images (
    image_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    person_id UUID REFERENCES persons(person_id) ON DELETE SET NULL,
    detection_id UUID REFERENCES detections(detection_id) ON DELETE SET NULL,
    image_path TEXT NOT NULL,
    image_type VARCHAR(30) NOT NULL,
    mime_type VARCHAR(50) NOT NULL DEFAULT 'image/jpeg',
    file_size_bytes BIGINT,
    sha256_hash CHAR(64),
    captured_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT person_images_type_check
        CHECK (
            image_type IN (
                'REFERENCE',
                'DETECTION_FACE',
                'DETECTION_FRAME',
                'EVIDENCE'
            )
        )
);

CREATE TABLE IF NOT EXISTS ocr_results (
    ocr_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    detection_id UUID NOT NULL
        REFERENCES detections(detection_id) ON DELETE CASCADE,
    image_id UUID NOT NULL
        REFERENCES person_images(image_id) ON DELETE CASCADE,
    plate_number VARCHAR(20),
    raw_text TEXT,
    confidence DECIMAL(5,2),
    is_verified BOOLEAN NOT NULL DEFAULT FALSE,
    verified_plate_number VARCHAR(20),
    processed_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT ocr_confidence_check
        CHECK (confidence >= 0 AND confidence <= 100)
);

CREATE INDEX IF NOT EXISTS idx_detections_camera_time
ON detections(camera_id, detected_at DESC);

CREATE INDEX IF NOT EXISTS idx_detections_classification_time
ON detections(classification, detected_at DESC);

CREATE INDEX IF NOT EXISTS idx_detections_person_time
ON detections(person_id, detected_at DESC);

CREATE INDEX IF NOT EXISTS idx_person_images_captured_at
ON person_images(captured_at DESC);

CREATE INDEX IF NOT EXISTS idx_person_images_detection
ON person_images(detection_id);

CREATE INDEX IF NOT EXISTS idx_person_images_person
ON person_images(person_id);

CREATE INDEX IF NOT EXISTS idx_ocr_results_detection
ON ocr_results(detection_id);

CREATE INDEX IF NOT EXISTS idx_ocr_results_image
ON ocr_results(image_id);

CREATE INDEX IF NOT EXISTS idx_ocr_results_plate_number
ON ocr_results(plate_number);

CREATE INDEX IF NOT EXISTS idx_ocr_results_processed_at
ON ocr_results(processed_at DESC);