DROP TABLE IF EXISTS raw_data.c40_country_name_lookup;

CREATE TABLE raw_data.c40_country_name_lookup AS
SELECT * FROM (
  SELECT 'Turkey' AS country, 'TR' AS iso_code
  UNION
  SELECT 'Nigeria', 'NG'
  UNION
  SELECT 'The Netherlands', 'NL'
  UNION
  SELECT 'Bangladesh', 'BD'
  UNION
  SELECT 'Ecuador', 'EC'
  UNION
  SELECT 'Italy', 'IT'
  UNION
  SELECT 'New Zealand', 'NZ'
  UNION
  SELECT 'Sweden', 'SE'
  UNION
  SELECT 'Norway', 'NO'
  UNION
  SELECT 'USA', 'US'
  UNION
  SELECT 'United Kingdom', 'GB'
  UNION
  SELECT 'Netherlands', 'NL'
  UNION
  SELECT 'Brazil', 'BR'
  UNION
  SELECT 'Jordan', 'JO'
  UNION
  SELECT 'Australia', 'AU'
  UNION
  SELECT 'Germany', 'DE'
  UNION
  SELECT 'Côte d’Ivoire', 'CI'
  UNION
  SELECT 'Canada', 'CA'
  UNION
  SELECT 'Ethiopia', 'ET'
  UNION
  SELECT 'South Korea', 'KR'
  UNION
  SELECT 'Portugal', 'PT'
  UNION
  SELECT 'Argentina', 'AR'
  UNION
  SELECT 'Spain', 'ES'
  UNION
  SELECT 'Colombia', 'CO'
  UNION
  SELECT 'United Arab Emirates', 'AE'
  UNION
  SELECT 'Greece', 'GR'
  UNION
  SELECT 'India', 'IN'
  UNION
  SELECT 'Chile', 'CL'
  UNION
  SELECT 'France', 'FR'
  UNION
  SELECT 'Vietnam', 'VN'
  UNION
  SELECT 'Israel', 'IL'
  UNION
  SELECT 'Mexico', 'MX'
  UNION
  SELECT 'South Africa', 'ZA'
  UNION
  SELECT 'Peru', 'PE'
  UNION
  SELECT 'Kenya', 'KE'
  UNION
  SELECT 'Malaysia', 'MY'
  UNION
  SELECT 'Senegal', 'SN'
  UNION
  SELECT 'Ghana', 'GH'
  UNION
  SELECT 'Poland', 'PL'
  UNION
  SELECT 'Japan', 'JP'
  UNION
  SELECT 'Sierra Leone', 'SL'
  UNION
  SELECT 'Denmark', 'DK'
  UNION
  SELECT 'Philippines', 'PH'
  UNION
  SELECT 'Thailand', 'TH'
)