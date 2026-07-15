# Rollback and cleanup plan

Stage 0 created no QBench object and requires no QBench rollback.

For later authorized stages:

1. Never delete evidence objects automatically.
2. Record the exact disposable Sandbox object name and type without committing
   internal IDs.
3. Keep draft parsers inactive unless a stage explicitly authorizes a tightly
   isolated temporary activation.
4. If activation is authorized, deactivate immediately after the controlled
   test and record both transitions.
5. Restore disposable worksheet baseline only with a previously proven narrow
   patch and only when the authorized stage allows it.
6. If failure behavior is partial, unclear, or not safely reversible, stop and
   request method-owner direction.
7. Await method-owner approval before deleting any parser draft, worksheet
   version, Batch, or attachment.

Production cleanup is never applicable because production activity is
permanently prohibited.
