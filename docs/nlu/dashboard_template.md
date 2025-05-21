# Documentation Health Dashboard

## Overview

<% if metrics.overall_score >= 90 %>
**Status: 🟢 EXCELLENT**
<% elseif metrics.overall_score >= 75 %>
**Status: 🟡 GOOD**
<% elseif metrics.overall_score >= 50 %>
**Status: 🟠 NEEDS IMPROVEMENT**
<% else %>
**Status: 🔴 CRITICAL**
<% endif %>

_Last updated: <%= current_date %>_

## Key Metrics

| Metric | Value | Target | Status |
|--------|-------|--------|---------|
| Overall Documentation Score | <%= metrics.overall_score %>% | 85% | <%= metrics.overall_score >= 85 ? "✅" : "❌" %> |
| Code Documentation Coverage | <%= metrics.code_coverage %>% | 80% | <%= metrics.code_coverage >= 80 ? "✅" : "❌" %> |
| Prompt Module Completeness | <%= metrics.prompt_completeness %>% | 100% | <%= metrics.prompt_completeness >= 100 ? "✅" : "❌" %> |
| Test Coverage | <%= metrics.test_coverage %>% | 80% | <%= metrics.test_coverage >= 80 ? "✅" : "❌" %> |
| Orphaned Documents | <%= metrics.orphaned_count %> | < 5 | <%= metrics.orphaned_count < 5 ? "✅" : "❌" %> |

## Documentation Health Trends

```
<%= graph %>
```

## Recent Changes

<% for change in recent_changes %>
- **<%= change.date %>**: <%= change.description %> (<%= change.impact %>)
<% endfor %>

## Critical Issues

<% if critical_issues.length > 0 %>
The following issues require immediate attention:

<% for issue in critical_issues %>
- <%= issue.description %> in `<%= issue.location %>`
<% endfor %>
<% else %>
No critical documentation issues found. 🎉
<% endif %>

## Recommendations

<% for recommendation in recommendations %>
<%= recommendation.priority %>. <%= recommendation.description %>
<% endfor %>

## Next Steps

1. Address critical issues identified in validation report
2. Review knowledge graph for disconnected components
3. Schedule documentation update for low-coverage areas
4. Run comprehensive analysis again after changes

[View Full Validation Report](../synthesis/reports/validation_report.md) | [Explore Knowledge Graph](../synthesis/visualizations/knowledge_graph_viewer.html)