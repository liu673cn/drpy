#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File  : models.py
# Author: DaShenHan&道长-----先苦后甜，任凭晚风拂柳颜------
# Date  : 2022/8/27

from db_operation.db_init import *

def get_dynamic_table_name_class(table_name):
  # 定义一个内部类
  class myTable(Base):
    # 给表名赋值
    __tablename__ = table_name
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(20))
    class_name = Column(String(32))
    class_url = Column(String(32))

    def __repr__(self):
        return "<Table(name='%s', class_name='%s', class_url='%s')>" % (
            self.name, self.class_name, self.class_url)
  # 把动态设置表名的类返回去
  return myTable

RuleClass = get_dynamic_table_name_class('rule_class')

# Base.metadata.create_all(engine, checkfirst=True)
# Base.metadata.create_all(engine, tables=[Base.metadata.tables['rule_class']],checkfirst=True)
RuleClass.__table__.create(engine, checkfirst=True)