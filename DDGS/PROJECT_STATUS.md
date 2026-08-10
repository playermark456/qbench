# Project Status

## Checkpoint

- Current date: 2026-08-09
- GitHub repository: `playermark456/qbench`
- Active branch: `AIT-Feed-DDGs`
- Current SmartDraw master: `drawings/smartdraw/source/AIT_DDGS_Future_Space_v02_MASTER.sdr`
- Current drawing scale: Architectural 1/8 inch = 1 foot; 1 actual foot = 9 PDF points; the 20-foot verification ruler must measure 2.500 inches on the PDF.
- Last completed milestone: The v02 audit-correction pass produced a sparse Room 114 equipment-planning shell. The architect reference was uniformly corrected to 99.826% while preserving its anchor, then relocked and kept independently hideable. Native room labels were hidden, redundant perimeter and door dimensions were removed, the 34'-0" finished-face south-wall dimension was retained, and the curved southwest and long south window walls plus the east-side plumbing/wash-station utility constraint were marked. Door locations remain approximate by explicit project direction and were not calibrated or verified. Scenario B equipment placement has not started.
- Architectural-base status: frozen for DDGS equipment-planning use at v02. No further architectural correction pass is required unless explicitly requested. This is not a construction-ready drawing; field, architect, MEP, safety, and OEM verification remain required.

## Base-plan corrections and constraints

- Preserve the complete irregular perimeter of room 114 FUTURE, including the curved southwest exterior/window wall and the long south exterior/window wall.
- Preserve entrances/openings only as approximate access references. Do not resume door-width, swing, hinge, snapping, or diagonal-dimension work unless explicitly requested.
- Recheck the east wall and hall/restroom-core interface against the architect sheets before finalizing fixtures or equipment.
- The annotated review marks the intended plumbing/wash-station area on the east side of room 114 FUTURE, adjacent to the hall/restroom core. Its planning purpose is a laboratory wash/handwash and wet-prep support point. Exact fixture type, drainage, supply, backflow, and routing require field and MEP verification.
- Treat the curved southwest wall and long south wall as window-wall constraints. Keep tall or opaque equipment away from the glazing, preserve access and required clearances, and verify sill, mullion, shading, and service-access conditions in the field.
- Planning assumption: serve central benches and suitable instruments with ceiling-drop power/data/utilities where practical so window walls remain unobstructed and floor penetrations are minimized. MEP and each OEM must verify voltage, load, gases, exhaust, data, water, drainage, and drop locations.

## Scenario B status

Scenario B is the current priority. The validated workbook defines it as `B - Gafta strict/lower capital`, a lowest-capex full-COA package using conventional Soxhlet and more manual fiber work. The workbook's current budget range is USD 334,500 to USD 555,500. Equipment has not yet been placed in the SmartDraw master.

The planning workflow should remain one-way: receive/login -> retain/bulk storage -> dirty primary grinding -> fine grinding/dividing -> wet chemistry and extraction -> clean instruments -> review/reporting and retain archive. Existing LCMS-8040RX, ICP-OES, and Multiwave 5000 remain in the existing controlled Prep Lab/Lab areas.

## Exact next Codex prompt

> Open `drawings/smartdraw/source/AIT_DDGS_Future_Space_v02_MASTER.sdr` in SmartDraw and use it as the frozen architectural planning base. Do not revise or verify doors. Build Scenario B using `data/instrument-options/DDGS_instrument_options_GAFTA_strict_v3.xlsx`: keep every table, bench, instrument, computer/docking station, storage element, utility drop, exhaust/vent point, label, and clearance envelope independently movable; place the wash station at the east-side `EXISTING PLUMBING / WASH STATION UTILITY ZONE - FIELD VERIFY` constraint; respect the curved southwest and long south window walls; preserve clear access paths and large open planning areas; and use ceiling utility drops only as a planning assumption pending MEP and OEM confirmation. Export an updated SDR, reference-on PDF, native-only PDF, SVG, and PNG audit set, then update `PROJECT_STATUS.md`, `FILE_MANIFEST.md`, and `CHANGELOG.md`.

## Source-of-truth files

1. `drawings/smartdraw/source/AIT_DDGS_Future_Space_v02_MASTER.sdr` - frozen editable v02 equipment-planning master.
2. `references/annotated-plans/AIT_DDGS_Future_Space_Annotated_Plumbing_Window_Walls.pdf` - plumbing and window-wall annotations.
3. `data/instrument-options/DDGS_instrument_options_GAFTA_strict_v3.xlsx` - current instrument, method, scenario, utility, and site-planning matrix.
4. `references/architect/AIT_DDGS_Architect_Plans_Original_Package.zip` and `AIT_DDGS_Future_Space_SmartDraw_Import_Guide.pdf` - architect reference package and scale/import basis.
5. `drawings/smartdraw/audit/AIT_DDGS_Future_Space_v02_REFERENCE_ON.pdf`, `AIT_DDGS_Future_Space_v02_NATIVE_ONLY.pdf`, `AIT_DDGS_Future_Space_v02_NATIVE_ONLY.svg`, and `AIT_DDGS_Future_Space_v02_PREVIEW.png` - current v02 visual audit set.

## Unresolved verification questions

- Field/architect: confirm all room dimensions, window extents and sill heights, mullions, door sizes/swings, wall construction, egress, accessibility, and final room boundaries.
- Plumbing/MEP: confirm the east-side plumbing point, sink purpose and fixture, hot/cold water, drainage, venting, backflow, floor sink needs, and permitted routing.
- Electrical/data: confirm service capacity, voltage/phases, dedicated circuits, emergency power needs, data drops, ceiling-drop feasibility, and final locations.
- HVAC/exhaust/safety: confirm room heat loads, ventilation, solvent/fume exhaust, dust collection, gas-cylinder controls, flammable storage, fire/life-safety requirements, and chemical compatibility.
- OEM: confirm footprints, service clearances, bench/load/vibration limits, utilities, exhaust, gases, environmental ranges, installation paths, and service access for every selected Scenario B item.
- Operations: confirm final sample volume, staffing, storage volumes, waste routes, contamination controls, and the desired balance between analyst labor and capital cost.
