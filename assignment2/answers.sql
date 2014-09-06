-- Problem 1
-- Question a:
SELECT COUNT(*) FROM Frequency WHERE docid = '10398_txt_earn';

-- Question b:
SELECT COUNT(*) FROM Frequency WHERE docid = '10398_txt_earn' AND count = 1;

-- Question c:
SELECT COUNT(*) FROM (SELECT term FROM Frequency WHERE docid = '10398_txt_earn' AND count = 1 UNION SELECT term FROM Frequency WHERE docid = '925_txt_trade' AND count = 1);

-- Question d:
SELECT COUNT(*) FROM (SELECT * FROM frequency WHERE term='parliament');

-- Question e:
SELECT COUNT(*) FROM (SELECT COUNT(docid) FROM Frequency GROUP BY docid HAVING SUM(count) > 300);

-- Question f:
SELECT COUNT(a.docid) FROM Frequency a, Frequency b WHERE a.docid = b.docid AND a.term = 'transactions' AND b.term = 'world' ORDER BY a.docid DESC;

-- Problem 2
-- Question g:
SELECT row_num, col_num, SUM(val) FROM (SELECT a.row_num, b.col_num, a.value*b.value AS val FROM a,b ON a.col_num = b.row_num) WHERE row_num = 2 AND col_num = 3 GROUP BY row_num, col_num;

-- Problem 3
-- Question h:
CREATE TEMP VIEW docsubset AS
SELECT * FROM Frequency
WHERE docid='10080_txt_crude' OR docid='17035_txt_earn';

SELECT d1, d2, SUM(score) FROM
(SELECT doc1.docid AS d1, doc2.docid AS d2, doc1.count * doc2.count AS score
FROM docsubset AS doc1, docsubset AS doc2
WHERE doc1.term = doc2.term
AND doc1.docid < doc2.docid)
GROUP BY d1, d2;

-- Question i:
CREATE TEMP VIEW docsubset AS
SELECT * FROM Frequency
UNION SELECT 'q' as docid, 'washington' as term, 1 as count
UNION SELECT 'q' as docid, 'taxes' as term, 1 as count
UNION SELECT 'q' as docid, 'treasury' as term, 1 as count;

SELECT d1, d2, SUM(score) FROM
(SELECT doc1.docid AS d1, doc2.docid AS d2, doc1.count * doc2.count AS score
FROM docsubset AS doc1, docsubset AS doc2
WHERE doc1.term = doc2.term
AND doc1.docid='q')
GROUP BY d1, d2
ORDER BY SUM(score) ASC;








