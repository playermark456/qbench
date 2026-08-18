# Resource Groups — production read-only capture

All 10 visible resource groups were captured from the Details, Inventory Items, and Equipment tabs. The evidence contains 105 group-to-item rows and 137 group-to-equipment rows; resources may legitimately appear in more than one group.

Important findings:

- Resource group 12, Pest (Quantitative) Analysis, is explicitly assigned to assay 21 but has zero inventory and zero equipment members.
- Resource groups 6, 10, and 11 have no explicit assay-side resource assignment. Their names are not treated as proof of association.
- Terpenes assay 8 has no explicit resource group.
- Only Water Activity group 3 visibly enables automatic equipment use. Group 12 did not expose the setting.
- Status/resource type, scheduling, availability, and required/optional behavior were not exposed and remain `not_exposed`.

`resource_group_associations.csv` records direct assay-side resource assignments. Its `assay_protocol_context_*` columns are indirect context copied from the assigned assay and are explicitly marked `indirect_assay_context_not_resource_assignment`; they do not assert a protocol-to-resource-group relationship.

Privacy boundary: safe resource-group descriptions were retained as configuration metadata. Inventory-item descriptions and catalog numbers, stock and lot data, serial numbers, exact locations, transactions, usage, attachments, and histories were not retained. Display sequence is observed UI order, not proof of configured scheduling or execution order.
