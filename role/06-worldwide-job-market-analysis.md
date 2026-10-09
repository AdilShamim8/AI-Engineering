# Understanding AI engineering job markets

Reviewed October 9, 2026. Regional comparisons need comparable data; a global title does not make a job-board sample representative.

## Evidence available here

The [reproduced job snapshot](../research/job-market-summary.json) describes 1,086 stored records observed September 23, 2026, from the original field guide's dataset. It supports sample-level counts, not a worldwide demand distribution. The earlier page's regional percentages, salary ranges, year-over-year growth figures, callback multiplier, and hiring-manager percentage lacked traceable records and have been removed.

The upstream dataset covers selected job-board locations and contains both raw descriptions and model-derived annotations. A location can describe eligibility, office location, remote scope, or several cities. These must be resolved explicitly before aggregating by geography. One advertisement can contain multiple locations; counting each as a separate vacancy inflates demand.

## Build a regional comparison that can be checked

| Measurement decision | Required documentation |
|---|---|
| Sampling frame | Boards/employer pages, countries, languages, collection period, search terms, inclusion/exclusion rules |
| Unit of analysis | Advertisement, distinct requisition, employer, or observed hiring event; these are different quantities |
| Geography | Office versus eligibility versus remote scope; multi-location and unknown-location handling |
| Role scope | Application engineering, model engineering, platform engineering, customer deployment; written classification rules |
| Duplicates | Requisition IDs, cross-board copies, recurring observations and normalized-description checks |
| Compensation | Local currency, base/bonus/equity distinction, disclosure coverage, period, level and employment type |
| Validation | Reviewed raw records, annotation disagreement, missingness, sampling bias and reproducible code |

Report results for the observed sample. Do not describe a change in advertisement wording or extraction model as a change in the labor market. Comparisons across dates require stable coverage, definitions and extraction methods.

For salary comparisons, keep each geography and currency separate before using a documented, dated conversion. Zurich is in Switzerland, not the EU. Singapore-dollar salaries do not describe Sydney or Tokyo. Contractor revenue, employee salary, and expected private-company equity liquidity are different measures.

## Evaluate an actual role

Read the responsibilities rather than relying on a title. Identify whether the job owns model development, application behavior, platform reliability, or customer integration. Inspect the employer's current posting for location eligibility, employment type, responsibilities, compensation disclosure and interview requirements.

Useful questions for a hiring team:

- What system or business outcome will this engineer own?
- Which datasets and evaluations establish that it works?
- Who owns security, on-call, deployment, and model/provider migrations?
- Is the role primarily product engineering, model research, infrastructure, or customer deployment?
- What level and compensation band are approved for this location and employment arrangement?

These questions support a more reliable job search than unsupported claims about universal AI premiums or framework-driven callback rates. See [skills and evidence](02-skills.md), [compensation comparison](../interview/07-global-compensation-and-job-market.md), and [research methodology](../research/README.md).
