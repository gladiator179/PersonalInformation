USE personal_information;

/*
 * 本文件主要用于对各个表创建索引
 */
CREATE INDEX u_in ON basic_information(user_name, user_sex);

CREATE INDEX m_in ON memorandum(memo_date);

CREATE INDEX al_in ON address_list(al_name);

CREATE INDEX p_in ON personal_journal(j_subject);

CREATE INDEX f_in ON friends(f_name)
