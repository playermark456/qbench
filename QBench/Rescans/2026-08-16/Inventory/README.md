# Inventory configuration — production read-only capture

The complete item list reconciles to 158 unique IDs across eight pages. Item ID, item name, category, source page, explicit resource-group IDs, and units/size exposed by safe resource-group membership rows were retained. Item active state and inventory type were not exposed. Seven inventory categories are active: Consumables, Formulation, General Consumables, Reagents, Reference Standards, Solvents, and Stocks.

The tenant-wide setting “Do not allow the usage of expired Inventory Stock for all Inventory Items” was not enabled on the read-only Settings tab. This does not establish item-level expiration behavior.

The Phase 3 field inventory exposes 12 Inventory Item and 9 Inventory Stock field definitions, including manufacturer/catalog, lot, expiration, and location-oriented structure. Field presence alone does not prove that lot, expiration, storage-location, reorder, or minimum-stock behavior is enabled. Resource-group assignments are recorded in `../Resource_Groups/resource_group_inventory_items.csv`.

Two configured items had a blank category in the captured list: IDs 292 and 273. All nonblank item categories reconcile to the seven active category definitions. Across the resource-group membership rows, `default_quantity` was blank for all 105 rows; item 174 had no displayed size and item 292 had no displayed category ID. These are preserved as visible configuration gaps, not filled by inference.

Descriptions, separate supplier/manufacturer fields, catalog values, prices, stock balances, lots, quantities, storage locations, transactions, purchases, attachments, and notes were omitted. Verbatim item names were preserved and may contain parenthetical qualifiers such as `(Fisher)`; those strings are part of the configured name, not retained supplier-account data.
