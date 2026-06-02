-- Geography Dimension - Continents
-- geography_dim_type_code: CON (Continent)
-- All continents are top-level entries (parent_geography_dimension_uid IS NULL)

INSERT INTO geography_dimension (
    geography_dimension_uid,
    created_at,
    created_by,
    name_fa,
    name_en,
    description_fa,
    description_en,
    valid_start_at,
    valid_end_at,
    geography_dim_type_code,
    state_type_code,
    parent_geography_dimension_uid
) VALUES
    ('019df753-5e15-7542-81c0-c387081f4f19', NOW(), 'system', 'آفریقا', 'Africa', 'قاره آفریقا', 'African continent', NOW(), NULL, 'CON', NULL, NULL),
    ('019df753-5e15-7542-81c0-c3883773a9e9', NOW(), 'system', 'جنوبگان', 'Antarctica', 'قاره جنوبگان (قاره قطب جنوب)', 'Antarctic continent', NOW(), NULL, 'CON', NULL, NULL),
    ('019df753-5e15-7542-81c0-c389975de37f', NOW(), 'system', 'آسیا', 'Asia', 'قاره آسیا', 'Asian continent', NOW(), NULL, 'CON', NULL, NULL),
    ('019df753-5e15-7542-81c0-c38a6f4276e1', NOW(), 'system', 'اروپا', 'Europe', 'قاره اروپا', 'European continent', NOW(), NULL, 'CON', NULL, NULL),
    ('019df753-5e15-7542-81c0-c38b71908300', NOW(), 'system', 'آمریکای شمالی', 'North America', 'قاره آمریکای شمالی', 'North American continent', NOW(), NULL, 'CON', NULL, NULL),
    ('019df753-5e15-7542-81c0-c38c95584f8a', NOW(), 'system', 'اقیانوسیه', 'Oceania', 'قاره اقیانوسیه (استرالیا و جزایر اقیانوس آرام)', 'Oceania continent (Australia and Pacific islands)', NOW(), NULL, 'CON', NULL, NULL),
    ('019df753-5e15-7542-81c0-c38d09301c51', NOW(), 'system', 'آمریکای جنوبی', 'South America', 'قاره آمریکای جنوبی', 'South American continent', NOW(), NULL, 'CON', NULL, NULL);
