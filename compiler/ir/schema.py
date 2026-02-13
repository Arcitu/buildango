from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List

class Parcel(BaseModel):
    parcel_id: str
    address: Optional[str] = None
    geom_wkt: Optional[str] = None  # keep it simple for the skeleton

class ZoningContext(BaseModel):
    jurisdiction: str
    zone_code: Optional[str] = None
    overlays: List[str] = Field(default_factory=list)

class BuildangoIR(BaseModel):
    parcel: Parcel
    zoning: ZoningContext
    constraints: Dict[str, Any] = Field(default_factory=dict)
    provenance: Dict[str, Any] = Field(default_factory=dict)  # sources + timestamps + hashes
