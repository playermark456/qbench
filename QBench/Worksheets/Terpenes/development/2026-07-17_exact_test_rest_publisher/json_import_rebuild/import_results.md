# JSON import compatibility result

Classification:
**`unqualified_address_candidate_local_validation_passed_save_retry_pending`**

Manual testing of the prior native-envelope candidate proved that it rendered
the expected 40x26 grid and loaded all 43 named cells. That render is valid
structural evidence, but it is not saved-version evidence.

QBench rejected **Save As New Version** with:

`Invalid cell definition Data!A2 for field name terpenes_instrument_conc_01`

The logical contract maps the first analyte to `Data!D2`; there is no intended
A2 destination. The actionable compatibility finding is that the old
single-tab save validator rejects sheet-qualified JSON cell definitions.

The regenerated candidate uses 43 unqualified runtime cells while preserving
the successfully rendered worksheet structure. No QBench environment was
accessed and no corrected upload or save was attempted in this prompt.

- Corrected JSON cells unqualified: 43/43
- First analyte: `D2`
- A2 mapping: absent
- Corrected Draft row visibly established: no
- Corrected saved/reopened export: no
- `destination_contract_proven=false`
