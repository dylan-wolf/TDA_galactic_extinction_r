-- First Search

SELECT TOP 500000
  s.ra, s.dec, s.z AS redshift, p.extinction_r
FROM SpecObj AS s
JOIN PhotoObj AS p ON s.bestObjID = p.objID
WHERE s.ra BETWEEN 150 AND 210
  AND s.dec BETWEEN 0 AND 10
  AND s.class = 'GALAXY'
  AND s.z BETWEEN 0.01 AND 0.3
ORDER BY p.extinction_r DESC

-- Second Search

SELECT TOP 500000
  s.ra, s.dec, s.z AS redshift, p.extinction_r
FROM SpecObj AS s
JOIN PhotoObj AS p ON s.bestObjID = p.objID
WHERE s.ra BETWEEN 100 AND 150
  AND s.dec BETWEEN 10 AND 25
  AND s.class = 'GALAXY'
  AND s.z BETWEEN 0.3 AND 0.6
ORDER BY p.extinction_r DESC

-- Third Search


SELECT TOP 500000
  s.ra, s.dec, s.z AS redshift, p.extinction_r
FROM SpecObj AS s
JOIN PhotoObj AS p ON s.bestObjID = p.objID
WHERE s.ra BETWEEN 210 AND 1260
  AND s.dec BETWEEN 10 AND 25
  AND s.class = 'GALAXY'
  AND s.z BETWEEN 0.01 AND 0.3
