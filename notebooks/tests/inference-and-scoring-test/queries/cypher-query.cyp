MATCH (d:Disease)-[rel_all:n4sch__SCO_RESTRICTION]->(all_s:Symptom)
WHERE rel_all.onPropertyURI = $has_symptom

WITH d, count(DISTINCT all_s) AS total_symptom_count,
     collect(DISTINCT all_s.n4sch__label[0]) AS all_symptoms

WITH d, total_symptom_count, all_symptoms,
     [s IN all_symptoms WHERE s IN $absent_symptoms] AS blocking_symptoms

WITH d, total_symptom_count, all_symptoms, blocking_symptoms,
     CASE WHEN size(blocking_symptoms) = 0 THEN true ELSE false END AS passed_filter

MATCH (d)-[rel:n4sch__SCO_RESTRICTION]->(s:Symptom)
WHERE rel.onPropertyURI = $has_symptom
  AND s.n4sch__label[0] IN $present_symptoms

WITH d, total_symptom_count, all_symptoms, blocking_symptoms, passed_filter,
     collect(DISTINCT s.n4sch__label[0]) AS matched_symptoms,
     count(DISTINCT s)                   AS match_count,
     sum(coalesce(s.weight, 0.0))        AS total_score

WHERE match_count >= $min_match

RETURN d.n4sch__label[0]                 AS disease,
       d.uri                             AS uri,
       passed_filter,
       blocking_symptoms,
       matched_symptoms,
       [s IN all_symptoms WHERE NOT s IN matched_symptoms]   AS missing_symptoms,
       match_count,
       total_symptom_count,
       total_score,
       total_score / sqrt(toFloat(total_symptom_count))      AS normalized_score
ORDER BY normalized_score DESC