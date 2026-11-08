
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