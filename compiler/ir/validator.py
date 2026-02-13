from compiler.ir.schema import BuildangoIR

def validate_ir(ir: BuildangoIR) -> list[str]:
    errors: list[str] = []
    if not ir.parcel.parcel_id:
        errors.append("parcel.parcel_id is required")
    if not ir.zoning.jurisdiction:
        errors.append("zoning.jurisdiction is required")
    # TODO: add 10–20 deterministic checks (setbacks, height bounds, FAR bounds, etc.)
    return errors
