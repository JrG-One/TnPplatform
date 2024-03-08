from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import Job_Opening
from .serializer import JobOpeningSerializer
import unittest
import requests

job_opening_data = {
            'NameofCompany':'Vyson',
            'profileOfCompany':'Software',
            'JobProfile': 'Software Engineer',
            'BranchChoice':'CSE',
            'ctc': '13LPA',
            'Eligibility': 'B.Tech',
            'Selection': 'Virtual',
            'location': 'Surat',
            'stipend': 10000,
            "start":"2024-03-18",
            'join_date': '2024-03-01',
            'end_of_registration': '2025-02-10'
        }

put_job_opening_data = {
            'NameofCompany':'KasperTech',
            'profileOfCompany':'Software',
            'JobProfile': 'Software Engineer',
            'BranchChoice':'CSE',
            'ctc': '13LPA',
            'Eligibility': 'B.Tech',
            'Selection': 'Offline',
            'location': 'Surat',
            'stipend': 10000,
            'join_date': '2024-03-01',
            'end_of_registration': '2024-02-15'
        }

updated_data = {
            'title': 'Senior Software Engineer',
            'description': 'Updated job opening for a software engineer',
            'location': 'Jaipur',
            'salary': 120000,
        }

import unittest
import requests
import json

class TestJobOpeningAPI(unittest.TestCase):
    def test_post_request(self):
        for i in range(5):
            response = requests.post('http://localhost:8000/job_openings/', data=json.dumps(job_opening_data), headers={'Content-Type': 'application/json'})
            self.assertEqual(response.status_code, 201)
            i=i+1

    def test_get_request(self):
        job_opening_id = 1
        response = requests.get(f'http://localhost:8000/job_openings/{job_opening_id}/')
        self.assertEqual(response.status_code, 200)

    def test_put_request(self):
        job_opening_id = 2
        response = requests.put(f'http://localhost:8000/job_openings/{job_opening_id}/', data=json.dumps(put_job_opening_data), headers={'Content-Type': 'application/json'})
        self.assertEqual(response.status_code, 200)

    def test_patch_request(self):
        job_opening_id = 8
        response = requests.patch(f'http://localhost:8000/job_openings/{job_opening_id}/', data=json.dumps(updated_data), headers={'Content-Type': 'application/json'})
        self.assertEqual(response.status_code, 200)

    def test_delete_request(self):
        job_opening_id = 4
        response = requests.delete(f'http://localhost:8000/job_openings/{job_opening_id}/')
        self.assertEqual(response.status_code, 204)

if __name__ == '__main__':
    unittest.main()