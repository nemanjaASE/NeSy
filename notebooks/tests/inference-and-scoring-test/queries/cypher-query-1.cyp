MATCH (d:Disease)-[rel:n4sch__SCO_RESTRICTION]->(s:Symptom)
WHERE rel.onPropertyURI = $has_symptom
    AND s.n4sch__label[0] IN $symptoms

WITH d,
    collect(DISTINCT s.n4sch__label[0]) AS matched_symptoms,
    count(DISTINCT s)                   AS match_count,
    sum(coalesce(s.weight, 0.0))        AS total_score

WHERE match_count >= $min_match

RETURN d.n4sch__label[0] AS disease,
       matched_symptoms,
       match_count,
       total_score
ORDER BY total_score DESC