CREATE TABLE IF NOT EXISTS exists_on
(
	q_code INTEGER NOT NULL,
	domain TEXT NOT NULL,
	PRIMARY KEY (q_code,domain),
	FOREIGN KEY (q_code) REFERENCES question(q_code) ON DELETE CASCADE ON UPDATE CASCADE,
	FOREIGN KEY (domain) REFERENCES online_judge (domain) ON DELETE CASCADE ON UPDATE CASCADE
);