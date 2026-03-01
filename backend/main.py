import os
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import math
import random
import time

BASE_DIR = Path(__file__).resolve().parent.parent
FRONTEND_DIR = BASE_DIR / "frontend"
APP_ENV = os.getenv("APP_ENV", "development").strip().lower()
PORT = int(os.getenv("PORT", "8000"))
HOST = os.getenv("HOST", "0.0.0.0")
CORS_ORIGINS_ENV = os.getenv("CORS_ORIGINS", "").strip()


def _build_cors_origins() -> list[str]:
    if CORS_ORIGINS_ENV:
        return [origin.strip() for origin in CORS_ORIGINS_ENV.split(",") if origin.strip()]
    if APP_ENV == "production":
        return []
    return ["*"]


app = FastAPI(
    title="Smart Campus AI API",
    description="Production-ready Smart Campus AI backend and frontend server",
    version="1.0.0",
)

cors_origins = _build_cors_origins()
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins if cors_origins else [],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

if FRONTEND_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(FRONTEND_DIR)), name="static")

# Fixed coordinate anchors for buildings (exact values provided).
building_coordinates = {
    # TECH PARK ZONE
    "Tech Park": {"lat": 12.82490, "lon": 80.04507},
    "TP-2": {"lat": 12.82521, "lon": 80.04578},
    "TP Auditorium": {"lat": 12.82483, "lon": 80.04668},
    "Vendhar Square": {"lat": 12.82336, "lon": 80.04523},
    "Java Food Court": {"lat": 12.82335, "lon": 80.04451},

    # ACADEMIC ZONE
    "Law College": {"lat": 12.82591, "lon": 80.04595},
    "CV Raman Block": {"lat": 12.8250, "lon": 80.04436},
    "SRM Polytechnic": {"lat": 12.82563, "lon": 80.04485},
    "Faculty of Science and Humanities": {"lat": 12.82535, "lon": 80.04644},
    "Biotech Block": {"lat": 12.82489, "lon": 80.04413},
    "SRM Dental College": {"lat": 12.82531, "lon": 80.04753},
    "BEL Block": {"lat": 12.82358, "lon": 80.04357},
    "University Building": {"lat": 12.82357, "lon": 80.04200},

    # HOSPITAL ZONE
    "SRM General Hospital": {"lat": 12.82299, "lon": 80.04803},
    "SRM Medical College": {"lat": 12.82089, "lon": 80.04817},

    # HOSTEL ZONE
    "APJ Girls Hostel": {"lat": 12.82422, "lon": 80.04916},
    "Dr. Muthulakshmi Hostel": {"lat": 12.82447, "lon": 80.04959},
    "N Block": {"lat": 12.82087, "lon": 80.04666},
    "M Block": {"lat": 12.82080, "lon": 80.04596},
    "Kalpana Chawla Hostel": {"lat": 12.82055, "lon": 80.04536},
    "D Mess": {"lat": 12.82086, "lon": 80.04460},
    "Malligai": {"lat": 12.82069, "lon": 80.04480},
    "Thamarai": {"lat": 12.82064, "lon": 80.04449},
    "Mullai": {"lat": 12.82075, "lon": 80.04415},
    "Manoranjitham": {"lat": 12.82054, "lon": 80.04390},
    "Sannasi Mess": {"lat": 12.82165, "lon": 80.04411},
    "Agasthiyar": {"lat": 12.82086, "lon": 80.04367},
    "Nelson": {"lat": 12.82128, "lon": 80.04346},
    "Adhiaman": {"lat": 12.82152, "lon": 80.04355},
    "Oori": {"lat": 12.82183, "lon": 80.04334},
    "Kaari": {"lat": 12.82213, "lon": 80.04344},
    "Paari": {"lat": 12.82260, "lon": 80.04351},
    "Meenakshi Hostel": {"lat": 12.82222, "lon": 80.04243},
}


# Real campus zone model (building + floor based infrastructure).
campus_zones = {
    "admin_zone": {
        "zone_type": "admin",
        "buildings": [
            {"name": "University Building", "floors": 15, "students": 2200},
        ],
    },
    "tech_park_zone": {
        "zone_type": "tech_park",
        "buildings": [
            {"name": "Tech Park", "floors": 10, "students": 1500},
            {"name": "TP-2", "floors": 10, "students": 1400},
            {"name": "TP Auditorium", "floors": 5, "students": 700},
            {"name": "Vendhar Square", "floors": 5, "students": 650},
            {"name": "Java Food Court", "floors": 5, "students": 600},
        ],
    },
    "academic_zone": {
        "zone_type": "academic",
        "buildings": [
            {"name": "Law College", "floors": 5, "students": 780},
            {"name": "CV Raman Block", "floors": 5, "students": 720},
            {"name": "SRM Polytechnic", "floors": 5, "students": 680},
            {"name": "Faculty of Science and Humanities", "floors": 5, "students": 900},
            {"name": "Biotech Block", "floors": 5, "students": 650},
            {"name": "SRM Dental College", "floors": 5, "students": 740},
            {"name": "BEL Block", "floors": 5, "students": 700},
            {"name": "University Building", "floors": 15, "students": 2600},
        ],
    },
    "hostel_zone": {
        "zone_type": "hostel",
        "buildings": [
            {"name": "APJ Girls Hostel", "floors": 10, "students": 930},
            {"name": "Dr. Muthulakshmi Hostel", "floors": 10, "students": 910},
            {"name": "N Block", "floors": 10, "students": 740},
            {"name": "M Block", "floors": 10, "students": 760},
            {"name": "Kalpana Chawla Hostel", "floors": 10, "students": 890},
            {"name": "D Mess", "floors": 10, "students": 820},
            {"name": "Malligai", "floors": 10, "students": 940},
            {"name": "Mullai", "floors": 10, "students": 860},
            {"name": "Thamarai", "floors": 10, "students": 880},
            {"name": "Paari", "floors": 10, "students": 910},
            {"name": "Kaari", "floors": 10, "students": 930},
            {"name": "Oori", "floors": 10, "students": 890},
            {"name": "Adhiaman", "floors": 10, "students": 910},
            {"name": "Nelson", "floors": 10, "students": 980},
            {"name": "Sannasi Mess", "floors": 10, "students": 840},
            {"name": "Manoranjitham", "floors": 10, "students": 920},
            {"name": "Agasthiyar", "floors": 10, "students": 900},
            {"name": "Meenakshi Hostel", "floors": 10, "students": 870},
        ],
    },
    "sports_zone": {
        "zone_type": "sports",
        "buildings": [
            {"name": "SRM Dental Ground", "floors": 5, "students": 700},
            {"name": "TP Ground", "floors": 5, "students": 650},
        ],
    },
    "hospital_zone": {
        "zone_type": "hospital",
        "buildings": [
            {"name": "SRM General Hospital", "floors": 10, "students": 1200},
            {"name": "SRM Medical College", "floors": 10, "students": 950},
        ],
    },
}


def _zone_base_config(zone_name: str):
    zone_type = campus_zones[zone_name]["zone_type"]
    if zone_type == "hostel":
        return {"waste_factor": 1.3, "water_pressure_bias": 4.2, "energy_bias": 7.0}
    if zone_type == "admin":
        return {"waste_factor": 1.0, "water_pressure_bias": 1.5, "energy_bias": 11.0}
    if zone_type == "sports":
        return {"waste_factor": 0.9, "water_pressure_bias": 3.0, "energy_bias": 4.0}
    if zone_type == "tech_park":
        return {"waste_factor": 1.15, "water_pressure_bias": 2.2, "energy_bias": 13.0}
    if zone_type == "hospital":
        return {"waste_factor": 1.35, "water_pressure_bias": 3.5, "energy_bias": 12.0}
    return {"waste_factor": 1.1, "water_pressure_bias": 2.0, "energy_bias": 9.0}


def _building_bin_count(zone_name: str, building: dict):
    """
    Floor-based scaling formula:
    - bins = max(1, floors // 2)
    """
    floors = max(int(building.get("floors", 1)), 1)
    return max(1, floors // 2)


def _build_runtime_zone_definitions():
    """Generate bins/water/energy nodes from real building infrastructure."""
    definitions = {}
    next_bin_id = 1000
    next_water_id = 2000
    next_energy_id = 3000

    for zone_name, zone_data in campus_zones.items():
        base_cfg = _zone_base_config(zone_name)
        bins = []
        water_nodes = []
        energy_nodes = []

        for building in zone_data["buildings"]:
            count = _building_bin_count(zone_name, building)
            anchor = building_coordinates.get(building["name"])
            if anchor is None:
                # Fallback keeps generation valid even if a building has no configured anchor.
                anchor = {"lat": 12.8230, "lon": 80.0440}
            lat = anchor["lat"]
            lon = anchor["lon"]

            # Deterministic local offsets keep bins tightly around building anchor (no global clustering).
            local_rng = random.Random(f"{zone_name}:{building['name']}")
            for _ in range(count):
                bins.append(
                    {
                        "id": next_bin_id,
                        "building_name": building["name"],
                        "floors": building["floors"],
                        "students": building["students"],
                        "lat": round(lat + local_rng.uniform(-0.00002, 0.00002), 6),
                        "lon": round(lon + local_rng.uniform(-0.00002, 0.00002), 6),
                    }
                )
                next_bin_id += 1

            water_nodes.append(
                {
                    "id": next_water_id,
                    "building_name": building["name"],
                    "lat": round(lat + 0.00005, 6),
                    "lon": round(lon - 0.00005, 6),
                }
            )
            next_water_id += 1

            energy_nodes.append(
                {
                    "id": next_energy_id,
                    "name": building["name"],
                    "floors": building["floors"],
                    "lat": round(lat - 0.00005, 6),
                    "lon": round(lon + 0.00005, 6),
                }
            )
            next_energy_id += 1

        definitions[zone_name] = {
            **base_cfg,
            "buildings": zone_data["buildings"],
            "bins": bins,
            "water_nodes": water_nodes,
            "energy_nodes": energy_nodes,
        }
    return definitions


# Runtime zone map used by live simulation engine.
ZONE_DEFINITIONS = _build_runtime_zone_definitions()

SCENARIO_PROFILES = {
    "normal_day": {
        "waste_rate_multiplier": 1.0,
        "water_pressure_bias": 0.0,
        "water_leak_threshold": 50.0,
        "energy_load_bias": 0.0,
        "energy_growth_min": 1.0,
        "energy_growth_max": 1.3,
    },
    "festival_peak": {
        "waste_rate_multiplier": 1.55,
        "water_pressure_bias": 5.0,
        "water_leak_threshold": 52.0,
        "energy_load_bias": 12.0,
        "energy_growth_min": 1.1,
        "energy_growth_max": 1.35,
    },
    "rainstorm": {
        "waste_rate_multiplier": 1.2,
        "water_pressure_bias": 11.0,
        "water_leak_threshold": 56.0,
        "energy_load_bias": 4.0,
        "energy_growth_min": 1.0,
        "energy_growth_max": 1.25,
    },
    "exam_week": {
        "waste_rate_multiplier": 1.1,
        "water_pressure_bias": 2.0,
        "water_leak_threshold": 50.0,
        "energy_load_bias": 9.0,
        "energy_growth_min": 1.05,
        "energy_growth_max": 1.32,
    },
}

MODE_PROFILES = {
    "normal": {"global_pressure": 1.0, "risk_decay": 5.0},
    "conservative": {"global_pressure": 0.85, "risk_decay": 8.0},
    "aggressive": {"global_pressure": 1.2, "risk_decay": 3.0},
}

twin_config = {
    "scenario": "normal_day",
    "mode": "normal",
    "stress_test": False,
    "stress_level": 1,
}

# Per-scope state: zone-specific and entire-campus scopes.
# Scope key is zone name or "__all__".
escalation_state = {}
risk_history = {}
sustainability_history = {}
system_cache = {}
CACHE_SECONDS = 1.5

# In-memory waste state per bin id.
bin_state = {}
bin_history = {}
for zone_data in ZONE_DEFINITIONS.values():
    for bin_item in zone_data["bins"]:
        initial_fill = random.randint(15, 40)
        now = time.time()
        bin_state[bin_item["id"]] = {
            "fill_level": float(initial_fill),
            "last_updated": now,
            "base_rate_per_min": random.uniform(0.8, 2.5),
        }
        bin_history[bin_item["id"]] = [(now, float(initial_fill))]


def _scope_key(zone: str | None) -> str:
    if zone and zone in ZONE_DEFINITIONS:
        return zone
    return "__all__"


def _zones_for_scope(scope_key: str):
    if scope_key == "__all__":
        return list(ZONE_DEFINITIONS.keys())
    return [scope_key]


def _scope_label(scope_key: str) -> str:
    return "entire_campus" if scope_key == "__all__" else scope_key


def _get_escalation_index(scope_key: str) -> float:
    if scope_key not in escalation_state:
        escalation_state[scope_key] = {"index": 0.0, "updated_at": time.time()}
    return escalation_state[scope_key]["index"]


def _set_escalation_index(scope_key: str, index_value: float):
    escalation_state[scope_key] = {
        "index": max(0.0, min(100.0, index_value)),
        "updated_at": time.time(),
    }


def _append_risk_history(scope_key: str, risk_score: int):
    if scope_key not in risk_history:
        risk_history[scope_key] = []
    risk_history[scope_key].append(risk_score)
    if len(risk_history[scope_key]) > 10:
        del risk_history[scope_key][0]


def _append_sustainability_history(scope_key: str, sustainability_score: int):
    if scope_key not in sustainability_history:
        sustainability_history[scope_key] = []
    sustainability_history[scope_key].append(sustainability_score)
    if len(sustainability_history[scope_key]) > 10:
        del sustainability_history[scope_key][0]


def _stress_multiplier() -> float:
    if not twin_config["stress_test"]:
        return 1.0
    return 1.0 + (0.25 * twin_config["stress_level"])


def _mode_pressure() -> float:
    mode = twin_config["mode"]
    return MODE_PROFILES.get(mode, MODE_PROFILES["normal"])["global_pressure"]


def _active_profile():
    scenario = twin_config["scenario"]
    return SCENARIO_PROFILES.get(scenario, SCENARIO_PROFILES["normal_day"])


def _zone_waste_time_multiplier(zone_name: str) -> float:
    """Optional advanced profile: zone-specific time behavior for waste generation."""
    zone_type = campus_zones[zone_name]["zone_type"]
    hour = time.localtime().tm_hour

    if zone_type == "hostel":
        return 1.25
    if zone_type == "academic":
        return 1.3 if 9 <= hour <= 17 else 0.82
    if zone_type == "admin":
        return 1.0 if 8 <= hour <= 18 else 0.75
    if zone_type == "sports":
        return 1.5 if 17 <= hour <= 21 else 0.7
    if zone_type == "hospital":
        return 1.35
    return 1.0


def _simulate_fill(bin_id: int, rate_multiplier: float) -> float:
    state = bin_state[bin_id]
    now = time.time()
    elapsed_minutes = max((now - state["last_updated"]) / 60.0, 0.0)

    base_rate = state["base_rate_per_min"] * rate_multiplier
    effective_rate = max(base_rate + random.uniform(-0.15, 0.15), 0.05)
    new_fill = min(100.0, state["fill_level"] + (effective_rate * elapsed_minutes))

    state["fill_level"] = new_fill
    state["last_updated"] = now

    history = bin_history[bin_id]
    history.append((now, new_fill))
    if len(history) > 30:
        del history[0]

    return new_fill


def _rate_per_minute(bin_id: int) -> float:
    history = bin_history[bin_id]
    if len(history) < 2:
        return bin_state[bin_id]["base_rate_per_min"]

    t0, f0 = history[0]
    t1, f1 = history[-1]
    delta_minutes = (t1 - t0) / 60.0
    if delta_minutes <= 0:
        return bin_state[bin_id]["base_rate_per_min"]

    return max((f1 - f0) / delta_minutes, 0.0)


def _predict_overflow_minutes(current_fill: float, rate_per_min: float):
    if current_fill >= 100.0:
        return 0
    if rate_per_min <= 0:
        return None

    minutes_left = (100.0 - current_fill) / rate_per_min
    return max(int(round(minutes_left)), 0)


def _status_from_prediction(predicted_overflow_minutes):
    if predicted_overflow_minutes is not None and predicted_overflow_minutes < 30:
        return "CRITICAL"
    if predicted_overflow_minutes is not None and predicted_overflow_minutes < 60:
        return "WARNING"
    return "NORMAL"


def _build_bins_snapshot(profile, selected_zones: list[str], escalation_index: float):
    snapshot = []
    for zone_name in selected_zones:
        zone_data = ZONE_DEFINITIONS[zone_name]
        zone_rate = zone_data["waste_factor"]
        time_multiplier = _zone_waste_time_multiplier(zone_name)
        rate_multiplier = (
            profile["waste_rate_multiplier"]
            * _mode_pressure()
            * _stress_multiplier()
            * zone_rate
            * time_multiplier
            * (1.0 + escalation_index / 260.0)
        )

        for bin_item in zone_data["bins"]:
            bin_id = bin_item["id"]
            current_fill = _simulate_fill(bin_id, rate_multiplier)
            rate = _rate_per_minute(bin_id)
            predicted_minutes = _predict_overflow_minutes(current_fill, rate)

            snapshot.append(
                {
                    "id": bin_id,
                    "zone": zone_name,
                    "building_name": bin_item["building_name"],
                    "floors": bin_item["floors"],
                    "lat": bin_item["lat"],
                    "lon": bin_item["lon"],
                    "fill_level": int(round(current_fill)),
                    "predicted_overflow_minutes": predicted_minutes,
                    "status": _status_from_prediction(predicted_minutes),
                }
            )
    return snapshot


def _build_water_snapshot(profile, selected_zones: list[str], escalation_index: float):
    snapshot = []
    stress = _stress_multiplier()
    escalation_bias = escalation_index * 0.12
    leak_threshold = profile["water_leak_threshold"] + (2.0 if twin_config["stress_test"] else 0.0)

    for zone_name in selected_zones:
        zone_data = ZONE_DEFINITIONS[zone_name]
        for node in zone_data["water_nodes"]:
            pressure = random.uniform(40, 100)
            pressure -= profile["water_pressure_bias"]
            pressure -= zone_data["water_pressure_bias"]
            pressure -= escalation_bias
            pressure -= (stress - 1.0) * 3.5
            pressure = round(max(20.0, min(110.0, pressure)), 1)
            status = "LEAK" if pressure < leak_threshold else "NORMAL"

            snapshot.append(
                {
                    "id": node["id"],
                    "zone": zone_name,
                    "lat": node["lat"],
                    "lon": node["lon"],
                    "pressure": pressure,
                    "status": status,
                }
            )
    return snapshot


def _build_energy_snapshot(profile, selected_zones: list[str], escalation_index: float):
    snapshot = []
    stress = _stress_multiplier()
    escalation_bias = escalation_index * 0.35

    growth_min = profile["energy_growth_min"]
    growth_max = profile["energy_growth_max"] + ((stress - 1.0) * 0.18)
    overload_threshold = max(135.0, 160.0 - (escalation_index * 0.12))

    for zone_name in selected_zones:
        zone_data = ZONE_DEFINITIONS[zone_name]
        for node in zone_data["energy_nodes"]:
            current_load = random.uniform(50, 150)
            current_load += profile["energy_load_bias"]
            current_load += zone_data["energy_bias"]
            current_load += escalation_bias
            current_load = round(max(35.0, min(210.0, current_load)), 1)

            growth_factor = round(random.uniform(growth_min, growth_max), 2)
            predicted_load = round(current_load * growth_factor, 1)
            status = "OVERLOAD" if predicted_load > overload_threshold else "NORMAL"

            snapshot.append(
                {
                    "id": node["id"],
                    "zone": zone_name,
                    "name": node["name"],
                    "lat": node["lat"],
                    "lon": node["lon"],
                    "current_load": current_load,
                    "predicted_load": predicted_load,
                    "status": status,
                }
            )
    return snapshot


def _update_escalation_index(scope_key: str, critical_count: int, leak_count: int, overload_count: int):
    mode = twin_config["mode"]
    mode_cfg = MODE_PROFILES.get(mode, MODE_PROFILES["normal"])

    current_index = _get_escalation_index(scope_key)
    stress_bonus = 12.0 * twin_config["stress_level"] if twin_config["stress_test"] else 0.0
    increase = (critical_count * 12.0) + (leak_count * 10.0) + (overload_count * 8.0) + stress_bonus
    decay = mode_cfg["risk_decay"]

    _set_escalation_index(scope_key, current_index + increase - decay)


def _compute_risk_score(critical_count: int, warning_count: int, leak_count: int, overload_count: int, escalation_index: float):
    risk = (critical_count * 40) + (warning_count * 20)
    risk += leak_count * 30
    risk += overload_count * 25
    risk += round(escalation_index * 0.35)
    return max(0, min(100, int(risk)))


def _linear_forecast(start_value: float, delta_per_step: float, steps: int = 6, clamp_min: float = 0.0, clamp_max: float = 100.0):
    series = []
    for step in range(1, steps + 1):
        value = start_value + (delta_per_step * step)
        value = max(clamp_min, min(clamp_max, value))
        series.append(round(value, 1))
    return series


def _haversine_km(lat1: float, lon1: float, lat2: float, lon2: float):
    # Lightweight great-circle distance approximation for route cost simulation.
    radius_km = 6371.0
    d_lat = math.radians(lat2 - lat1)
    d_lon = math.radians(lon2 - lon1)
    a = (
        math.sin(d_lat / 2) ** 2
        + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(d_lon / 2) ** 2
    )
    return radius_km * (2 * math.atan2(math.sqrt(a), math.sqrt(1 - a)))


def _path_distance_km(points: list[tuple[float, float]], depot: tuple[float, float] = (12.8235, 80.0445)):
    if not points:
        return 0.0
    total = 0.0
    prev_lat, prev_lon = depot
    for lat, lon in points:
        total += _haversine_km(prev_lat, prev_lon, lat, lon)
        prev_lat, prev_lon = lat, lon
    total += _haversine_km(prev_lat, prev_lon, depot[0], depot[1])
    return total


def _compute_cost_optimization(zone: str | None = None):
    """
    Cost optimization intelligence:
    - Estimates economic savings from optimized AI-driven operations.
    - Uses in-memory sensor and routing simulation only.
    """
    system = _build_system_snapshot(zone=zone)
    bins_snapshot = system["bins"]
    water_snapshot = system["water_nodes"]
    energy_snapshot = system["energy_nodes"]

    # Cost assumptions (hackathon-friendly constants).
    fuel_cost_per_liter = 100.0
    water_cost_per_liter = 0.05
    energy_cost_per_kwh = 8.0
    co2_per_liter_fuel = 2.68
    fuel_liters_per_km = 0.35
    avg_route_speed_kmph = 22.0

    # Waste optimization: compare broad pickup route vs targeted risk-based route.
    baseline_bins = [item for item in bins_snapshot if item["fill_level"] >= 45]
    optimized_bins = [item for item in bins_snapshot if item["status"] in {"CRITICAL", "WARNING"}]
    if not baseline_bins:
        baseline_bins = bins_snapshot[:]
    if not optimized_bins and bins_snapshot:
        optimized_bins = bins_snapshot[: max(1, len(bins_snapshot) // 3)]

    baseline_points = [(item["lat"], item["lon"]) for item in baseline_bins]
    optimized_points = [(item["lat"], item["lon"]) for item in optimized_bins]
    baseline_km = _path_distance_km(baseline_points)
    optimized_km = _path_distance_km(optimized_points)
    distance_saved_km = max(baseline_km - optimized_km, 0.0)

    fuel_saved_liters = distance_saved_km * fuel_liters_per_km
    minutes_saved = (distance_saved_km / avg_route_speed_kmph) * 60.0 if avg_route_speed_kmph > 0 else 0.0
    co2_prevented_kg = fuel_saved_liters * co2_per_liter_fuel
    waste_cost_saved = fuel_saved_liters * fuel_cost_per_liter

    # Water leak prevention: estimate hourly avoidable loss from detected leak severity.
    leak_nodes = [item for item in water_snapshot if item["status"] == "LEAK"]
    liters_loss_prevented = 0.0
    for node in leak_nodes:
        pressure_deficit = max(50.0 - node["pressure"], 0.0)
        liters_loss_prevented += 90.0 + (pressure_deficit * 14.0)
    water_cost_saved = liters_loss_prevented * water_cost_per_liter

    # Energy management: estimate recoverable energy from overload excess.
    overload_nodes = [item for item in energy_snapshot if item["status"] == "OVERLOAD"]
    kwh_saved = 0.0
    peak_reduction_kw = 0.0
    for node in overload_nodes:
        overload_excess = max(node["predicted_load"] - 160.0, 0.0)
        kwh_saved += overload_excess * 1.6
        peak_reduction_kw += overload_excess * 0.45
    energy_cost_saved = kwh_saved * energy_cost_per_kwh

    total_saved = waste_cost_saved + water_cost_saved + energy_cost_saved

    # Baseline vs optimized cost summary for analytics chart.
    predicted_problem_cost = (baseline_km * fuel_liters_per_km * fuel_cost_per_liter) + (liters_loss_prevented * water_cost_per_liter) + (kwh_saved * energy_cost_per_kwh * 1.2)
    optimized_cost = max(predicted_problem_cost - total_saved, 0.0)

    return {
        "waste": {
            "fuel_saved_liters": round(fuel_saved_liters, 2),
            "minutes_saved": int(round(minutes_saved)),
            "co2_prevented_kg": round(co2_prevented_kg, 2),
            "cost_saved_₹": round(waste_cost_saved, 2),
        },
        "water": {
            "liters_loss_prevented": round(liters_loss_prevented, 2),
            "cost_saved_₹": round(water_cost_saved, 2),
        },
        "energy": {
            "kwh_saved": round(kwh_saved, 2),
            "cost_saved_₹": round(energy_cost_saved, 2),
            "peak_reduction_kw": round(peak_reduction_kw, 2),
        },
        "total_savings_₹": round(total_saved, 2),
        "comparison": {
            "predicted_problem_cost_₹": round(predicted_problem_cost, 2),
            "post_optimization_cost_₹": round(optimized_cost, 2),
        },
        "active_zone": system["scope"]["active_zone"],
    }


def _compute_sustainability_score(zone: str | None = None):
    """
    Sustainability model:
    - Base score: 100 - escalation_index
    - Penalties: critical waste, leaks, overloads
    - Bonuses: cost savings, CO2 reduction, water preservation, energy savings
    """
    scope_key = _scope_key(zone)
    system = _build_system_snapshot(zone=zone)
    cost = _compute_cost_optimization(zone=zone)

    bins_snapshot = system["bins"]
    water_snapshot = system["water_nodes"]
    energy_snapshot = system["energy_nodes"]
    escalation_index = system["twin"]["escalation_index"]

    critical_count = sum(1 for item in bins_snapshot if item["status"] == "CRITICAL")
    leak_count = sum(1 for item in water_snapshot if item["status"] == "LEAK")
    overload_count = sum(1 for item in energy_snapshot if item["status"] == "OVERLOAD")

    base_score = 100.0 - float(escalation_index)

    waste_penalty = critical_count * 3.0
    water_penalty = leak_count * 4.0
    energy_penalty = overload_count * 3.0
    total_penalty = waste_penalty + water_penalty + energy_penalty

    # Keep bonuses bounded so score stays interpretable.
    bonus_cost = min((cost["total_savings_₹"] / 180.0), 14.0)
    bonus_co2 = min((cost["waste"]["co2_prevented_kg"] / 4.0), 8.0)
    bonus_water = min((cost["water"]["liters_loss_prevented"] / 220.0), 8.0)
    bonus_energy = min((cost["energy"]["kwh_saved"] / 35.0), 8.0)
    total_bonus = bonus_cost + bonus_co2 + bonus_water + bonus_energy

    score = int(round(max(0.0, min(100.0, base_score - total_penalty + total_bonus))))
    _append_sustainability_history(scope_key, score)

    if score >= 80:
        status = "SUSTAINABLE"
    elif score >= 50:
        status = "AT RISK"
    else:
        status = "CRITICAL"

    total_impact = total_penalty if total_penalty > 0 else 1.0
    waste_impact_pct = round((waste_penalty / total_impact) * 100.0, 1)
    water_impact_pct = round((water_penalty / total_impact) * 100.0, 1)
    energy_impact_pct = round((energy_penalty / total_impact) * 100.0, 1)

    return {
        "sustainability_score": score,
        "status": status,
        "co2_saved_kg": round(cost["waste"]["co2_prevented_kg"], 2),
        "water_saved_liters": round(cost["water"]["liters_loss_prevented"], 2),
        "energy_saved_kwh": round(cost["energy"]["kwh_saved"], 2),
        "trend": sustainability_history.get(scope_key, [])[-10:],
        "impact_breakdown": {
            "waste_impact_pct": waste_impact_pct,
            "water_impact_pct": water_impact_pct,
            "energy_impact_pct": energy_impact_pct,
        },
        "active_zone": system["scope"]["active_zone"],
    }


def _cross_system_intelligence(zone: str | None = None):
    """
    Cross-system reasoning layer:
    - Correlates simultaneous waste/water/energy risks.
    - Produces coordinated actions instead of isolated module actions.
    - Uses scenario + mode + time context for actionable guidance.
    """
    system = _build_system_snapshot(zone=zone)
    bins_snapshot = system["bins"]
    water_snapshot = system["water_nodes"]
    energy_snapshot = system["energy_nodes"]

    critical_bins = [item for item in bins_snapshot if item["status"] == "CRITICAL"]
    leak_nodes = [item for item in water_snapshot if item["status"] == "LEAK"]
    overload_nodes = [item for item in energy_snapshot if item["status"] == "OVERLOAD"]

    # Group risk signals by zone for co-occurrence reasoning.
    waste_zones = {item["zone"] for item in critical_bins}
    water_zones = {item["zone"] for item in leak_nodes}
    energy_zones = {item["zone"] for item in overload_nodes}

    all_risk_zones = sorted(waste_zones | water_zones | energy_zones)
    three_way_zones = sorted(waste_zones & water_zones & energy_zones)
    water_energy_zones = sorted(water_zones & energy_zones)
    waste_water_zones = sorted(waste_zones & water_zones)
    waste_energy_zones = sorted(waste_zones & energy_zones)

    scenario = system["twin"]["scenario"]
    mode = system["twin"]["mode"]
    risk_score = system["twin"]["risk_score"]
    escalation_index = system["twin"]["escalation_index"]
    hour = time.localtime().tm_hour

    composite_actions = []
    explanation_parts = []

    # Highest priority: compound tri-system failures in same zone.
    if three_way_zones:
        composite_actions.append(
            {
                "priority": "CRITICAL",
                "zones": three_way_zones,
                "recommended_action": "Activate emergency response protocol: synchronize waste clearance, leak isolation, and temporary energy load shedding.",
                "confidence": 0.94,
            }
        )
        explanation_parts.append(
            f"Tri-system co-occurrence detected in {', '.join(three_way_zones)}"
        )

    # Cascade candidate: leak + overload suggests electrical/water safety risk.
    if water_energy_zones:
        composite_actions.append(
            {
                "priority": "CRITICAL",
                "zones": water_energy_zones,
                "recommended_action": "Shift energy load to auxiliary grid and dispatch water team immediately.",
                "confidence": 0.9,
            }
        )
        explanation_parts.append(
            f"Water leaks and energy overloads co-occur in {', '.join(water_energy_zones)}"
        )

    # Cross-operations coordination with scheduling.
    if waste_water_zones and not three_way_zones:
        composite_actions.append(
            {
                "priority": "MEDIUM",
                "zones": waste_water_zones,
                "recommended_action": "Dispatch leak maintenance first, then route waste teams through cleared corridors.",
                "confidence": 0.83,
            }
        )
        explanation_parts.append(
            f"Waste and water risks overlap in {', '.join(waste_water_zones)}"
        )

    if waste_energy_zones and not three_way_zones:
        composite_actions.append(
            {
                "priority": "MEDIUM",
                "zones": waste_energy_zones,
                "recommended_action": "Stage waste pickups around high-load facilities and stagger HVAC-intensive operations.",
                "confidence": 0.8,
            }
        )
        explanation_parts.append(
            f"Waste and energy pressure overlap in {', '.join(waste_energy_zones)}"
        )

    # Contextual modifiers: scenario/time/mode can escalate coordination guidance.
    if not composite_actions:
        if risk_score >= 70 or escalation_index >= 70:
            composite_actions.append(
                {
                    "priority": "MEDIUM",
                    "zones": all_risk_zones or [system["scope"]["active_zone"]],
                    "recommended_action": "Run preventive coordination drill: pre-position technicians, rebalance loads, and pre-emptively clear high-fill bins.",
                    "confidence": 0.74,
                }
            )
            explanation_parts.append("High global risk without a single dominant overlap pattern")
        else:
            composite_actions.append(
                {
                    "priority": "LOW",
                    "zones": [system["scope"]["active_zone"]],
                    "recommended_action": "System stable. Maintain standard monitoring cadence and readiness.",
                    "confidence": 0.72,
                }
            )
            explanation_parts.append("No significant cross-module co-occurrence detected")

    # Time/scenario context note for operator awareness.
    context_note = f"Scenario={scenario}, Mode={mode}, Hour={hour}"
    if scenario == "festival_peak":
        context_note += ", expected crowd-driven load and waste spikes"
    elif scenario == "rainstorm":
        context_note += ", elevated leak probability and mobility constraints"

    return {
        "composite_actions": composite_actions,
        "explanation": ". ".join(explanation_parts),
        "context": context_note,
        "active_zone": system["scope"]["active_zone"],
        "risk_score": risk_score,
        "escalation_index": escalation_index,
    }


def _build_system_snapshot(force_refresh: bool = False, zone: str | None = None):
    scope_key = _scope_key(zone)
    now = time.time()

    cached = system_cache.get(scope_key)
    if (
        not force_refresh
        and cached is not None
        and (now - cached["timestamp"] <= CACHE_SECONDS)
    ):
        return cached["data"]

    profile = _active_profile()
    selected_zones = _zones_for_scope(scope_key)
    escalation_index = _get_escalation_index(scope_key)

    bins_snapshot = _build_bins_snapshot(profile, selected_zones, escalation_index)
    water_snapshot = _build_water_snapshot(profile, selected_zones, escalation_index)
    energy_snapshot = _build_energy_snapshot(profile, selected_zones, escalation_index)

    critical_count = sum(1 for item in bins_snapshot if item["status"] == "CRITICAL")
    warning_count = sum(1 for item in bins_snapshot if item["status"] == "WARNING")
    leak_count = sum(1 for item in water_snapshot if item["status"] == "LEAK")
    overload_count = sum(1 for item in energy_snapshot if item["status"] == "OVERLOAD")

    _update_escalation_index(scope_key, critical_count, leak_count, overload_count)
    escalation_index = _get_escalation_index(scope_key)
    risk_score = _compute_risk_score(critical_count, warning_count, leak_count, overload_count, escalation_index)
    _append_risk_history(scope_key, risk_score)

    data = {
        "bins": bins_snapshot,
        "water_nodes": water_snapshot,
        "energy_nodes": energy_snapshot,
        "scope": {
            "active_zone": _scope_label(scope_key),
            "is_zone_filtered": scope_key != "__all__",
            "zones_in_scope": selected_zones,
            "zone_count": len(selected_zones),
            "total_zones": len(ZONE_DEFINITIONS),
        },
        "twin": {
            "scenario": twin_config["scenario"],
            "mode": twin_config["mode"],
            "stress_test": twin_config["stress_test"],
            "stress_level": twin_config["stress_level"],
            "escalation_index": round(escalation_index, 1),
            "risk_score": risk_score,
            "generated_at": now,
        },
    }

    system_cache[scope_key] = {"timestamp": now, "data": data}
    return data


def _frontend_file(name: str) -> FileResponse:
    target = FRONTEND_DIR / name
    if not target.exists():
        raise HTTPException(status_code=404, detail=f"Missing frontend file: {name}")
    return FileResponse(target)


@app.get("/")
def landing_page():
    return _frontend_file("index.html")


@app.get("/dashboard")
def dashboard_page():
    return _frontend_file("dashboard.html")


@app.get("/analytics")
def analytics_page():
    return _frontend_file("analytics.html")


@app.get("/digital-twin")
def digital_twin_page():
    return _frontend_file("digital-twin.html")


@app.get("/healthz")
def health_check():
    return {
        "status": "ok",
        "env": APP_ENV,
        "host": HOST,
        "port": PORT,
        "service": "smart-campus-ai",
    }


@app.get("/bins")
def get_bins(zone: str | None = None):
    return _build_system_snapshot(zone=zone)["bins"]


@app.get("/optimized-route")
def optimized_route(zone: str | None = None):
    snapshot = _build_system_snapshot(zone=zone)["bins"]

    route_bins = [
        bin_item
        for bin_item in snapshot
        if bin_item["status"] in {"CRITICAL", "WARNING"}
    ]

    severity_rank = {"CRITICAL": 0, "WARNING": 1, "NORMAL": 2}
    route_bins.sort(
        key=lambda item: (
            severity_rank.get(item["status"], 99),
            item["predicted_overflow_minutes"] if item["predicted_overflow_minutes"] is not None else 10**9,
        )
    )

    return {"route": route_bins}


@app.get("/water-nodes")
def get_water_nodes(zone: str | None = None):
    return _build_system_snapshot(zone=zone)["water_nodes"]


@app.get("/energy-nodes")
def get_energy_nodes(zone: str | None = None):
    return _build_system_snapshot(zone=zone)["energy_nodes"]


@app.get("/ai-decisions")
def ai_decisions(zone: str | None = None):
    """
    AI recommendation engine with zone-aware context.
    """
    system = _build_system_snapshot(zone=zone)
    bins_snapshot = system["bins"]
    water_snapshot = system["water_nodes"]
    energy_snapshot = system["energy_nodes"]

    critical_bins = [item for item in bins_snapshot if item["status"] == "CRITICAL"]
    leak_nodes = [item for item in water_snapshot if item["status"] == "LEAK"]
    overload_nodes = [item for item in energy_snapshot if item["status"] == "OVERLOAD"]
    escalation_index = system["twin"]["escalation_index"]

    decisions = []
    if critical_bins:
        decisions.append(
            {
                "priority": "HIGH",
                "message": f"Deploy waste collection teams to {len(critical_bins)} critical zones.",
            }
        )
    if leak_nodes:
        decisions.append(
            {
                "priority": "HIGH",
                "message": f"Dispatch water maintenance to {len(leak_nodes)} leak nodes.",
            }
        )
    if overload_nodes:
        decisions.append(
            {
                "priority": "MEDIUM",
                "message": f"Initiate load balancing for {len(overload_nodes)} overloaded buildings.",
            }
        )
    if escalation_index >= 75:
        decisions.append(
            {
                "priority": "HIGH",
                "message": "Escalation spike detected. Activate command-center incident protocol.",
            }
        )
    if not decisions:
        decisions.append({"priority": "LOW", "message": "System stable"})

    return {
        "decisions": decisions,
        "escalation_index": escalation_index,
        "active_zone": system["scope"]["active_zone"],
    }


@app.get("/digital-twin/status")
def digital_twin_status(zone: str | None = None):
    system = _build_system_snapshot(zone=zone)
    return {
        "scenario": twin_config["scenario"],
        "mode": twin_config["mode"],
        "stress_test": twin_config["stress_test"],
        "stress_level": twin_config["stress_level"],
        "active_zone": system["scope"]["active_zone"],
        "zone_count": system["scope"]["zone_count"],
        "total_zones": system["scope"]["total_zones"],
        "escalation_index": system["twin"]["escalation_index"],
        "risk_score": system["twin"]["risk_score"],
        "generated_at": system["twin"]["generated_at"],
        "available_zones": list(ZONE_DEFINITIONS.keys()),
        "available_scenarios": list(SCENARIO_PROFILES.keys()),
        "available_modes": list(MODE_PROFILES.keys()),
    }


@app.post("/digital-twin/config")
def set_digital_twin_config(
    scenario: str | None = None,
    mode: str | None = None,
    stress_test: bool | None = None,
    stress_level: int | None = None,
):
    """Real-time behavior switching endpoint for demo controls."""
    if scenario is not None and scenario in SCENARIO_PROFILES:
        twin_config["scenario"] = scenario

    if mode is not None and mode in MODE_PROFILES:
        twin_config["mode"] = mode

    if stress_test is not None:
        twin_config["stress_test"] = stress_test

    if stress_level is not None:
        twin_config["stress_level"] = max(1, min(3, stress_level))

    # Refresh all known scopes after config updates.
    for key in ["__all__"] + list(ZONE_DEFINITIONS.keys()):
        _build_system_snapshot(force_refresh=True, zone=None if key == "__all__" else key)

    return {
        "message": "Digital twin configuration updated",
        "config": twin_config,
        "supported_zones": list(ZONE_DEFINITIONS.keys()),
    }


@app.get("/forecast")
def forecast(zone: str | None = None):
    """
    Zone-aware forecast endpoint:
    - waste_forecast: next 60 minutes at 10-minute intervals
    - energy_forecast: next 60 minutes at 10-minute intervals
    - risk_trend: rolling history of last 10 risk scores for scope
    """
    scope_key = _scope_key(zone)
    system = _build_system_snapshot(zone=zone)
    bins_snapshot = system["bins"]
    energy_snapshot = system["energy_nodes"]

    if bins_snapshot:
        avg_fill_now = sum(item["fill_level"] for item in bins_snapshot) / len(bins_snapshot)
        avg_rate_per_min = sum(_rate_per_minute(item["id"]) for item in bins_snapshot) / len(bins_snapshot)
    else:
        avg_fill_now = 0.0
        avg_rate_per_min = 0.0

    waste_delta_per_10min = avg_rate_per_min * 10.0
    waste_forecast = _linear_forecast(
        start_value=avg_fill_now,
        delta_per_step=waste_delta_per_10min,
        steps=6,
        clamp_min=0.0,
        clamp_max=100.0,
    )

    if energy_snapshot:
        avg_current_load = sum(item["current_load"] for item in energy_snapshot) / len(energy_snapshot)
        avg_growth = sum(item["predicted_load"] - item["current_load"] for item in energy_snapshot) / len(energy_snapshot)
    else:
        avg_current_load = 0.0
        avg_growth = 0.0

    energy_forecast = _linear_forecast(
        start_value=avg_current_load,
        delta_per_step=max(avg_growth, 0.0),
        steps=6,
        clamp_min=0.0,
        clamp_max=300.0,
    )

    return {
        "active_zone": system["scope"]["active_zone"],
        "waste_forecast": waste_forecast,
        "energy_forecast": energy_forecast,
        "risk_trend": risk_history.get(scope_key, [])[-10:],
    }


@app.get("/cost-optimization")
def cost_optimization(zone: str | None = None):
    return _compute_cost_optimization(zone=zone)


@app.get("/cross-intelligence")
def cross_intelligence(zone: str | None = None):
    return _cross_system_intelligence(zone=zone)


@app.get("/sustainability-score")
def sustainability_score(zone: str | None = None):
    return _compute_sustainability_score(zone=zone)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("backend.main:app", host=HOST, port=PORT, reload=APP_ENV != "production")
