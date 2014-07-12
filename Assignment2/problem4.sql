select d1.docid, d2.docid, sum(d1.count*d2.count)
from Frequency D1, Frequency D2
where D1.term = D2.term
and D1.docid = '10080_txt_crude' AND D2.docid = '17035_txt_earn' 
group by d1.docid, d2.docid

