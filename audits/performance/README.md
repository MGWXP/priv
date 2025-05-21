# Performance Metrics

This folder contains performance data produced during test runs and CI
executions. Metrics are tracked against the budgets defined in
`execution-budget.yaml` to ensure the project meets responsiveness targets.

Use the workflow CLI to update metrics after running the test suite:

```bash
./scripts/ai_workflow_cli.py monitor-performance --update --metrics '{"test_count": 0}'
```

Generated dashboards will appear in `audits/dashboards/`. Historical data is
stored here for trend analysis and capacity planning.
