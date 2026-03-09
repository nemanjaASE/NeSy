MATCH (s:Symptom)
RETURN s.n4sch__label[0] AS label, s.embedding AS embedding