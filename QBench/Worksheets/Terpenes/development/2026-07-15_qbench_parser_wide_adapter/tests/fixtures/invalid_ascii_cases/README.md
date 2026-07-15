# Invalid ASCII cases

The JavaScript tests generate invalid LabSolutions ASCII cases in memory from
`../Output_redacted_fixture.txt` so the controlled redacted fixture remains the
single raw source file. Cases covered include missing sections, malformed row
width, missing/duplicate analytes, unknown Compound Results names, ID/name
mismatch, text concentrations, oversized input, and excessive line length.
