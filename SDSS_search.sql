SELECT TOP 500000
  s.ra, s.dec, s.z AS redshift, p.extinction_r
FROM SpecObj AS s
JOIN PhotoObj AS p ON s.bestObjID = p.objID
WHERE s.ra BETWEEN 150 AND 210
  AND s.dec BETWEEN 0 AND 10
  AND s.class = 'GALAXY'
  AND s.z BETWEEN 0.01 AND 0.3
ORDER BY p.extinction_r DESC
