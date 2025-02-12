# Odoo Module for Keda Backend Test

## Notes
- The API route can be configured from the file `controllers/__init__.py`.
- The Odoo unit tests only check for models validation. Rest API endpoints are to be tested using the `manual_api_tests.py` script.
- The test requirement for the models are not very detailed so the fields properties are written with an assumption.
- I wrote `material.code` as a primary key in the ERD, but it turns out Odoo already sets `id` as primary key so I added a unique constraint instead.
