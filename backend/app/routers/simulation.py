from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, validator

router = APIRouter()

# ----------------------------------------------------
# Input Model for Simulation
# ----------------------------------------------------
class SimulationInput(BaseModel):
    vehicle_speed: float          # km/h
    vru_distance: float           # meters
    vru_type: str                 # pedestrian, cyclist, animal, 2-wheeler
    weather: str                  # clear, rain, fog, snow
    lighting: str                 # day, night

    @validator("vehicle_speed")
    def speed_must_be_positive(cls, v):
        if v is None:
            raise ValueError("Vehicle speed is required")
        if v <= 0:
            raise ValueError("Vehicle speed must be greater than zero")
        return v

    @validator("vru_distance")
    def distance_must_be_positive(cls, v):
        if v < 0:
            raise ValueError("Distance cannot be negative")
        return v

    @validator("vru_type")
    def validate_vru(cls, v):
        allowed = ["pedestrian", "cyclist", "2-wheeler", "animal"]
        if v.lower() not in allowed:
            raise ValueError(f"Invalid VRU type. Allowed: {allowed}")
        return v

    @validator("weather")
    def validate_weather(cls, v):
        allowed = ["clear", "rain", "fog", "snow"]
        if v.lower() not in allowed:
            raise ValueError(f"Invalid weather. Allowed: {allowed}")
        return v

    @validator("lighting")
    def validate_lighting(cls, v):
        allowed = ["day", "night"]
        if v.lower() not in allowed:
            raise ValueError(f"Invalid lighting. Allowed: {allowed}")
        return v


# ----------------------------------------------------
# Risk Factors
# ----------------------------------------------------
VRU_VULNERABILITY = {
    "pedestrian": 1.5,
    "cyclist": 1.3,
    "2-wheeler": 1.4,
    "animal": 1.2
}

WEATHER_RISK = {
    "clear": 1.0,
    "rain": 1.2,
    "fog": 1.4,
    "snow": 1.6
}

LIGHTING_RISK = {
    "day": 1.0,
    "night": 1.3
}

# ----------------------------------------------------
# Status Route
# ----------------------------------------------------
@router.get("/status")
def simulation_status():
    return {"module": "Simulation Engine", "status": "OK"}


# ----------------------------------------------------
# Main Simulation Route
# ----------------------------------------------------
@router.post("/run")
def run_simulation(data: SimulationInput):

    speed = data.vehicle_speed
    distance = data.vru_distance

    # Convert km/h → m/s
    speed_m_s = speed / 3.6

    # Reaction + braking distance
    reaction_time = 1.5
    reaction_distance = speed_m_s * reaction_time
    braking_distance = (speed_m_s ** 2) / (2 * 6)

    total_stopping_distance = reaction_distance + braking_distance

    # Risk Factors
    weather_factor = WEATHER_RISK[data.weather.lower()]
    lighting_factor = LIGHTING_RISK[data.lighting.lower()]
    vru_factor = VRU_VULNERABILITY[data.vru_type.lower()]

    # Risk Score Formula
    risk_score = (
        (speed / 10)
        + (max(0, (total_stopping_distance - distance)) * 2)
        + (weather_factor * 5)
        + (lighting_factor * 3)
        + (vru_factor * 4)
    )

    # Classification
    if risk_score < 20:
        risk_level = "LOW"
    elif risk_score < 40:
        risk_level = "MEDIUM"
    elif risk_score < 60:
        risk_level = "HIGH"
    else:
        risk_level = "CRITICAL"

    return {
        "input": data.dict(),
        "speed_m_s": round(speed_m_s, 2),
        "reaction_distance": round(reaction_distance, 2),
        "braking_distance": round(braking_distance, 2),
        "total_stopping_distance": round(total_stopping_distance, 2),
        "risk_score": round(risk_score, 2),
        "risk_level": risk_level,
        "collision_likely": distance < total_stopping_distance
    }
