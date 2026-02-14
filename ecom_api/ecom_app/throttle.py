from rest_framework.throttling import UserRateThrottle

class BrustRateThrottle(UserRateThrottle):
    scope = "brust"

class SustainedRateThrottle(UserRateThrottle):
    scope = "sustained"