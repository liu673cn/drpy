#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File  : play_parse.py
# Author: DaShenHan&道长-----先苦后甜，任凭晚风拂柳颜------
# Date  : 2022/8/28


def init(db):
    class PlayParse(db.Model):
        __tablename__ = 'play_parse'
        id = db.Column(db.Integer, primary_key=True, autoincrement=True)
        play_url = db.Column(db.String(255))
        real_url = db.Column(db.String(255))

        def __repr__(self):
            return "<PlayParse(play_url='%s', real_url='%s')>" % (
                self.play_url, self.real_url)

    # db.create_all()
    db.create_all()
    return PlayParse