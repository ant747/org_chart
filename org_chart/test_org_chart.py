import os
import org_chart
import unittest
import tempfile
import json

class ChartTestCase(unittest.TestCase):

    def setUp(self):
        self.db_fd, org_chart.app.config['TEMP_DB'] = tempfile.mkstemp()
        org_chart.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + org_chart.app.config['TEMP_DB']
        org_chart.app.testing = True
        self.app = org_chart.app.test_client()
        with org_chart.app.app_context():
            org_chart.db.create_all()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(org_chart.app.config['TEMP_DB'])

    def test_empty_db(self):
        rv = self.app.get('/')
        assert b'empty' in rv.data

    def test_reset_db(self):
        rv = self.app.post('/api/orgchart/new')
        assert b'reset' in rv.data



if __name__ == '__main__':
    unittest.main()