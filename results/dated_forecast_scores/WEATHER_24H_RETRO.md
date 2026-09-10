# Weather 24 h retrospective

*Generated 2026-09-10T00:05:46.540345+00:00 · pin D1D38A*

Issued JSON is **frozen**. This asks whether the first SI day of a 48 h
window would have given the same hold/kill. New issues use 24 h.

Compared **28/28** windows with observations (agree 24 h vs 48 h).

| ID | Buoy | 48 h | 24 h | Same | n24 / n48 |
|----|------|------|------|:----:|----------:|
| `FCAST-WX-20260825-01` | RDDA2 | hold | hold | True | 234/471 |
| `FCAST-WX-20260825-02` | WRXA2 | hold | hold | True | 144/288 |
| `FCAST-WX-20260825-03` | UQXA2 | hold | hold | True | 144/286 |
| `FCAST-WX-20260825-04` | KOZA2 | hold | hold | True | 144/287 |
| `FCAST-WX-20260825-05` | DHXA2 | hold | hold | True | 144/288 |
| `FCAST-WX-20260825T0121-01` | WRXA2 | hold | hold | True | 144/288 |
| `FCAST-WX-20260825T0121-02` | SGXA2 | hold | hold | True | 144/288 |
| `FCAST-WX-20260825T0121-03` | OLCN6 | kill | kill | True | 144/288 |
| `FCAST-WX-20260825T0121-04` | 45144 | no_obs | no_obs | None | 0/0 |
| `FCAST-WX-20260825T0121-05` | 42058 | kill | kill | True | 143/284 |
| `FCAST-WX-20260825T0121-06` | BABT2 | hold | hold | True | 237/474 |
| `FCAST-WX-20260825T0222-01` | UQXA2 | hold | hold | True | 142/286 |
| `FCAST-WX-20260825T0222-02` | 46208 | no_obs | no_obs | None | 0/0 |
| `FCAST-WX-20260825T0222-03` | OLCN6 | kill | kill | True | 144/288 |
| `FCAST-WX-20260825T0222-04` | 45145 | no_obs | no_obs | None | 0/0 |
| `FCAST-WX-20260825T0222-05` | 42058 | kill | kill | True | 143/284 |
| `FCAST-WX-20260825T0222-06` | EPTT2 | hold | hold | True | 240/478 |
| `FCAST-WX-20260831T2357-01` | MDXA2 | hold | hold | True | 144/288 |
| `FCAST-WX-20260831T2357-02` | PPXA2 | hold | hold | True | 144/288 |
| `FCAST-WX-20260831T2357-03` | APRP7 | hold | hold | True | 240/480 |
| `FCAST-WX-20260831T2357-04` | BZST2 | hold | hold | True | 240/480 |
| `FCAST-WX-20260831T2357-05` | 44078 | kill | kill | True | 144/288 |
| `FCAST-WX-20260901T0032-01` | MDXA2 | hold | hold | True | 144/288 |
| `FCAST-WX-20260901T0032-02` | PPXA2 | hold | hold | True | 144/288 |
| `FCAST-WX-20260901T0032-03` | 42013 | hold | hold | True | 48/95 |
| `FCAST-WX-20260901T0032-04` | APRP7 | hold | hold | True | 240/480 |
| `FCAST-WX-20260901T0032-05` | 62146 | no_obs | no_obs | None | 0/0 |
| `FCAST-WX-20260909T1854-01` | 62442 | kill | kill | True | 5/5 |
| `FCAST-WX-20260909T1854-02` | 46070 | hold | hold | True | 12/12 |
| `FCAST-WX-20260909T1854-03` | 64046 | hold | hold | True | 5/5 |
| `FCAST-WX-20260909T1854-04` | 51002 | hold | hold | True | 12/12 |
| `FCAST-WX-20260909T1854-05` | PTIT2 | hold | hold | True | 44/44 |

Kill: rewriting issued JSON. Kill: retuning POOF to swallow a miss.

Refresh: `python scripts/retro_weather_24h.py`
