-- Variable to represent the hostname of grafana
grafana_host = "http://metrics.cloud.gov:3000"

-- Mapping between Env Value and what it corresponds to for dashboard urls.
dashboard_ending = {}
dashboard_ending["cf-chili"]="prd"
dashboard_ending["cf-green"]="np"
