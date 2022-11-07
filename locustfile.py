from locust import task
from locust import between
from locust import HttpUser

sample = {"geo_level_1_id": 17,
 "geo_level_2_id": 596,
 "geo_level_3_id": 11307,
 "count_floors_pre_eq": 3,
 "age": 20,
 "area_percentage": 7,
 "height_percentage": 6,
 "land_surface_condition": "t",
 "foundation_type": "r",
 "roof_type": "n",
 "ground_floor_type": "f",
 "other_floor_type": "q",
 "position": "s",
 "plan_configuration": "d",
 "has_superstructure_adobe_mud": 0,
 "has_superstructure_mud_mortar_stone": 1,
 "has_superstructure_stone_flag": 0,
 "has_superstructure_cement_mortar_stone": 0,
 "has_superstructure_mud_mortar_brick": 0,
 "has_superstructure_cement_mortar_brick": 0,
 "has_superstructure_timber": 0,
 "has_superstructure_bamboo": 0,
 "has_superstructure_rc_non_engineered": 0,
 "has_superstructure_rc_engineered": 0,
 "has_superstructure_other": 0,
 "legal_ownership_status": "v",
"count_families": 1,
 "has_secondary_use": 0,
 "has_secondary_use_agriculture": 0,
 "has_secondary_use_hotel": 0,
 "has_secondary_use_rental": 0,
 "has_secondary_use_institution": 0,
 "has_secondary_use_school": 0,
 "has_secondary_use_industry": 0,
 "has_secondary_use_health_post": 0,
 "has_secondary_use_gov_office": 0,
 "has_secondary_use_use_police": 0,
 "has_secondary_use_other": 0}

class RitcherPredictUser(HttpUser):
    """
    Usage:
        Start locust load testing client with:

            locust -H http://localhost:3000

        Open browser at http://0.0.0.0:8089, adjust desired number of users and spawn
        rate for the load test from the Web UI and start swarming.
    """

    @task
    def classify(self):
        self.client.post("/classify", json=sample)

    wait_time = between(0.01, 2)