# Parcel Schema v1.0 (UD Case Viewer)

## Geometry
- width (m)
- depth (m)
- height (m)
- volume_m3 = width * depth * height

## Physics
- weight_kg (real or demo fallback)
- max_top_load_kg (real or demo rule)

## Handling
- stackable (bool demo rule; later: data-driven)
- fragile_flag (future)
- orientation (future)

## Identification
- parcel_id (provided or generated)

## Placement (simulation fields)
- x, y, z (origin coordinates inside locker)
