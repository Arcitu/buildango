from compiler.ir.schema import BuildangoIR

def apply_zoning_rules(ir: BuildangoIR) -> BuildangoIR:
    # TODO: translate jurisdiction-specific rules into constraints
    # Example:
    ir.constraints.setdefault("max_height_ft", 35)
    ir.constraints.setdefault("min_front_setback_ft", 15)
    return ir
