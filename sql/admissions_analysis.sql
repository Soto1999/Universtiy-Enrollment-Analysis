
-- Take in all admissions data
SELECT * FROM admissions;

-- Get total applications and admissions by category
SELECT
    category, applicants, admitted
FROM admissions
WHERE category != 'Total';

-- Group total applications by gender
SELECT
    category,
    SUM(applicants) AS total_applications,
    SUM(admitted) AS total_admitted
FROM admissions
WHERE category != 'Total'
GROUP BY category
ORDER BY total_applications DESC;

SELECT
    category,
    applicants, 
    admitted,
    ROUND( admitted * 100.0 / nullif(applicants, 0) , 2) AS calculated_admission_rate
FROM admissions
WHERE category != 'Total';

SELECT
    category,
    admission_rate AS stored_rate,
    ROUND( admitted * 100.0 / nullif(applicants, 0) , 2) AS calculated_admission_rate
FROM admissions
WHERE category != 'Total';

CREATE VIEW IF NOT EXISTS admissions_report AS
SELECT
    category,
    applicants,
    admitted,
    ROUND (admitted * 100.0 / nullif(applicants, 0), 2) AS admission_rate
FROM admissions;

SELECT
    category,
    admission_rate
FROM admissions_report
WHERE category != 'Total'
ORDER BY admission_rate DESC;