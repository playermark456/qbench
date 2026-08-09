# Project Status

## Checkpoint

- Current date: 2026-08-09
- GitHub repository: `playermark456/qbench`
- Active branch: `AIT-Feed-DDGs`
- Current SmartDraw master: `drawings/smartdraw/source/AIT_DDGS_Future_Space_Editable_Exact_Scale.sdr`
- Current drawing scale: Architectural 1/8 inch = 1 foot; 1 actual foot = 9 PDF points; the 20-foot verification ruler must measure 2.500 inches on the PDF.
- Last completed milestone: An editable exact-scale SmartDraw base for room 114 FUTURE was produced with corrected wall and door geometry, reference-on PDF/PNG/SVG audits, and a separate annotated plumbing/window-wall review. Scenario B equipment placement has not yet been completed.

## Base-plan corrections and constraints

- Preserve the complete irregular perimeter of room 114 FUTURE, including the curved southwest exterior/window wall and the long south exterior/window wall.
- Preserve the corrected north and northwest door openings, widths, swings, and alignment with the storage, hall, and drying-room interfaces.
- Recheck the east wall and hall/restroom-core interface against the architect sheets before finalizing fixtures or equipment.
- The annotated review marks the intended plumbing/wash-station area on the east side of room 114 FUTURE, adjacent to the hall/restroom core. Its planning purpose is a laboratory wash/handwash and wet-prep support point. Exact fixture type, drainage, supply, backflow, and routing require field and MEP verification.
- Treat the curved southwest wall and long south wall as window-wall constraints. Keep tall or opaque equipment away from the glazing, preserve access and required clearances, and verify sill, mullion, shading, and service-access conditions in the field.
- Planning assumption: serve central benches and suitable instruments with ceiling-drop power/data/utilities where practical so window walls remain unobstructed and floor penetrations are minimized. MEP and each OEM must verify voltage, load, gases, exhaust, data, water, drainage, and drop locations.

## Scenario B status

Scenario B is the current priority. The validated workbook defines it as `B - Gafta strict/lower capital`, a lowest-capex full-COA package using conventional Soxhlet and more manual fiber work. The workbook's current budget range is USD 334,500 to USD 555,500. Equipment has not yet been placed in the SmartDraw master.

The planning workflow should remain one-way: receive/login -> retain/bulk storage -> dirty primary grinding -> fine grinding/dividing -> wet chemistry and extraction -> clean instruments -> review/reporting and retain archive. Existing LCMS-8040RX, ICP-OES, and Multiwave 5000 remain in the existing controlled Prep Lab/Lab areas.

## Exact next Codex prompt

> Open `drawings/smartdraw/source/AIT_DDGS_Future_Space_Editable_Exact_Scale.sdr` in SmartDraw. Implement and verify the base-plan corrections shown in `references/annotated-plans/AIT_DDGS_Future_Space_Annotated_Plumbing_Window_Walls.pdf` while preserving the exact 1/8 inch = 1 foot scale and keeping every object independently movable. Then build Scenario B using `data/instrument-options/DDGS_instrument_options_GAFTA_strict_v3.xlsx`: keep tables, equipment, instruments, computers, utilities, labels, and clearance envelopes separate; place the wash station at the annotated east-side plumbing area subject to field and MEP verification; respect the curved southwest and long south window walls; and use ceiling utility drops as a planning assumption pending MEP and OEM confirmation. Export an updated SDR, reference-on PDF, native-only PDF, SVG, and PNG audit set, then update `PROJECT_STATUS.md` and `CHANGELOG.md`.

## Source-of-truth files

1. `drawings/smartdraw/source/AIT_DDGS_Future_Space_Editable_Exact_Scale.sdr` - editable exact-scale master.
2. `references/annotated-plans/AIT_DDGS_Future_Space_Annotated_Plumbing_Window_Walls.pdf` - plumbing and window-wall annotations.
3. `data/instrument-options/DDGS_instrument_options_GAFTA_strict_v3.xlsx` - current instrument, method, scenario, utility, and site-planning matrix.
4. `references/architect/AIT_DDGS_Architect_Plans_Original_Package.zip` and `AIT_DDGS_Future_Space_SmartDraw_Import_Guide.pdf` - architect reference package and scale/import basis.
5. `drawings/smartdraw/audit/AIT_DDGS_Future_Space_Reference_On.*` - current reference-on visual audit set.

## Unresolved verification questions

- Field/architect: confirm all room dimensions, window extents and sill heights, mullions, door sizes/swings, wall construction, egress, accessibility, and final room boundaries.
- Plumbing/MEP: confirm the east-side plumbing point, sink purpose and fixture, hot/cold water, drainage, venting, backflow, floor sink needs, and permitted routing.
- Electrical/data: confirm service capacity, voltage/phases, dedicated circuits, emergency power needs, data drops, ceiling-drop feasibility, and final locations.
- HVAC/exhaust/safety: confirm room heat loads, ventilation, solvent/fume exhaust, dust collection, gas-cylinder controls, flammable storage, fire/life-safety requirements, and chemical compatibility.
- OEM: confirm footprints, service clearances, bench/load/vibration limits, utilities, exhaust, gases, environmental ranges, installation paths, and service access for every selected Scenario B item.
- Operations: confirm final sample volume, staffing, storage volumes, waste routes, contamination controls, and the desired balance between analyst labor and capital cost.
