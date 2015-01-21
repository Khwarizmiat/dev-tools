# -*- coding: utf-8 -*-
###############################################################################
#
#   Module for OpenERP
#   Copyright (C) 2014 Akretion (http://www.akretion.com).
#   @author Sébastien BEAU <sebastien.beau@akretion.com>
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU Affero General Public License as
#   published by the Free Software Foundation, either version 3 of the
#   License, or (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU Affero General Public License for more details.
#
#   You should have received a copy of the GNU Affero General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
###############################################################################

from openerp.osv import orm
from openerp.sql_db import Cursor
import pdb
from datetime import datetime
import logging
_logger = logging.getLogger(__name__)

LOG_FILTER = set()


class SqlLogger(orm.AbstractModel):
    _name = 'sql.logger'

    def active(self, cr, uid, key, context=None):
        LOG_FILTER.add(key)
        return True

    def inactive(self, cr, uid, key, context=None):
        LOG_FILTER.remove(key)
        return True

original_execute = Cursor.execute


def execute(self, query, params=None, log_exceptions=None):
    now = datetime.now()
    stop = False
    res = original_execute(
        self, query,
        params=params, log_exceptions=log_exceptions)
    for key in LOG_FILTER:
        if key in query:
            stop = True

    if stop:
        delay = datetime.now() - now
        _logger.info("query: %s. Delay : %s", self._obj.query[0:50], delay)
        pdb.set_trace()
    return res


Cursor.execute = execute
