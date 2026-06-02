-- Iran Dade Service - Gregorian Calendar Time Dimension
-- Centuries 0-21 (Years 0-2199)
-- date_value and datetime_value represent July 2 of the middle year


INSERT INTO time_dimension (
  time_dimension_uid, created_at, created_by, name, description, century_value, year_value, date_value, datetime_value, calendar_type_code, time_dimension_type_code, parent_time_dimension_uid
) VALUES
  ('019df840-a16e-72e1-b336-d3ffe102a121', NOW(), 'system', 'Century 0', 'Years 0-99', 0, 50, '0050-07-02', '0050-07-02 00:00:00+00', 'GRG', 'CEN', NULL),
  ('019df840-a16e-72e1-b336-d4008f1248f5', NOW(), 'system', 'Century 1', 'Years 100-199', 1, 150, '0150-07-02', '0150-07-02 00:00:00+00', 'GRG', 'CEN', NULL),
  ('019df840-a16e-72e1-b336-d40142ba31de', NOW(), 'system', 'Century 2', 'Years 200-299', 2, 250, '0250-07-02', '0250-07-02 00:00:00+00', 'GRG', 'CEN', NULL),
  ('019df840-a16e-72e1-b336-d402b5870a89', NOW(), 'system', 'Century 3', 'Years 300-399', 3, 350, '0350-07-02', '0350-07-02 00:00:00+00', 'GRG', 'CEN', NULL),
  ('019df840-a16e-72e1-b336-d4033386e33b', NOW(), 'system', 'Century 4', 'Years 400-499', 4, 450, '0450-07-02', '0450-07-02 00:00:00+00', 'GRG', 'CEN', NULL),
  ('019df840-a16e-72e1-b336-d404862faa2b', NOW(), 'system', 'Century 5', 'Years 500-599', 5, 550, '0550-07-02', '0550-07-02 00:00:00+00', 'GRG', 'CEN', NULL),
  ('019df840-a16e-72e1-b336-d405b70aea31', NOW(), 'system', 'Century 6', 'Years 600-699', 6, 650, '0650-07-02', '0650-07-02 00:00:00+00', 'GRG', 'CEN', NULL),
  ('019df840-a16e-72e1-b336-d4061544813e', NOW(), 'system', 'Century 7', 'Years 700-799', 7, 750, '0750-07-02', '0750-07-02 00:00:00+00', 'GRG', 'CEN', NULL),
  ('019df840-a16e-72e1-b336-d407c4d63e9a', NOW(), 'system', 'Century 8', 'Years 800-899', 8, 850, '0850-07-02', '0850-07-02 00:00:00+00', 'GRG', 'CEN', NULL),
  ('019df840-a16e-72e1-b336-d40868319fb8', NOW(), 'system', 'Century 9', 'Years 900-999', 9, 950, '0950-07-02', '0950-07-02 00:00:00+00', 'GRG', 'CEN', NULL),
  ('019df840-a16e-72e1-b336-d40957f19528', NOW(), 'system', 'Century 10', 'Years 1000-1099', 10, 1050, '1050-07-02', '1050-07-02 00:00:00+00', 'GRG', 'CEN', NULL),
  ('019df840-a16e-72e1-b336-d40ad77ed51b', NOW(), 'system', 'Century 11', 'Years 1100-1199', 11, 1150, '1150-07-02', '1150-07-02 00:00:00+00', 'GRG', 'CEN', NULL),
  ('019df840-a16e-72e1-b336-d40bd4d1d295', NOW(), 'system', 'Century 12', 'Years 1200-1299', 12, 1250, '1250-07-02', '1250-07-02 00:00:00+00', 'GRG', 'CEN', NULL),
  ('019df840-a16e-72e1-b336-d40c604a965a', NOW(), 'system', 'Century 13', 'Years 1300-1399', 13, 1350, '1350-07-02', '1350-07-02 00:00:00+00', 'GRG', 'CEN', NULL),
  ('019df840-a16e-72e1-b336-d40d6ab2fe22', NOW(), 'system', 'Century 14', 'Years 1400-1499', 14, 1450, '1450-07-02', '1450-07-02 00:00:00+00', 'GRG', 'CEN', NULL),
  ('019df840-a16e-72e1-b336-d40eefbd9f0b', NOW(), 'system', 'Century 15', 'Years 1500-1599', 15, 1550, '1550-07-02', '1550-07-02 00:00:00+00', 'GRG', 'CEN', NULL),
  ('019df840-a16e-72e1-b336-d40f6d12ca0c', NOW(), 'system', 'Century 16', 'Years 1600-1699', 16, 1650, '1650-07-02', '1650-07-02 00:00:00+00', 'GRG', 'CEN', NULL),
  ('019df840-a16e-72e1-b336-d410040cce3a', NOW(), 'system', 'Century 17', 'Years 1700-1799', 17, 1750, '1750-07-02', '1750-07-02 00:00:00+00', 'GRG', 'CEN', NULL),
  ('019df840-a16e-72e1-b336-d411d7feea5f', NOW(), 'system', 'Century 18', 'Years 1800-1899', 18, 1850, '1850-07-02', '1850-07-02 00:00:00+00', 'GRG', 'CEN', NULL),
  ('019df840-a16e-72e1-b336-d412120fb027', NOW(), 'system', 'Century 19', 'Years 1900-1999', 19, 1950, '1950-07-02', '1950-07-02 00:00:00+00', 'GRG', 'CEN', NULL),
  ('019df840-a16e-72e1-b336-d4133addc816', NOW(), 'system', 'Century 20', 'Years 2000-2099', 20, 2050, '2050-07-02', '2050-07-02 00:00:00+00', 'GRG', 'CEN', NULL),
  ('019df840-a16e-72e1-b336-d41464df2b47', NOW(), 'system', 'Century 21', 'Years 2100-2199', 21, 2150, '2150-07-02', '2150-07-02 00:00:00+00', 'GRG', 'CEN', NULL)
;