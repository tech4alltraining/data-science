# Datasets

Every dataset the book uses lives here. **No chapter builds its data inline** — each one
loads a file, the way a real project does.

Chapters load by a path relative to the project root:

```python
df = pd.read_csv("datasets/messy_customers.csv")
```

That works from any chapter because `_quarto.yml` sets `execute-dir: project`.

## Two kinds of file

| Kind | Where it comes from | How to rebuild |
|---|---|---|
| **Real** | published datasets from the [course catalog](https://github.com/tech4alltraining/aiml/tree/main/datasets) | `python datasets/download_real.py` |
| **Generated** | a seeded script in this folder | `python datasets/make_all.py` |

**Real data is preferred** and is used wherever it fits. Data is generated only when a
chapter needs a property no real file has — a known cluster structure, a planted
association rule, a deliberate leak, or a controlled amount of mess.

Every generator is **seeded**, so rebuilding produces byte-identical files.

## Real datasets

| File | Rows × cols | Why this one | Used in |
|---|---|---|---|
| `pre_data.csv` | 12 × 4 | small enough to clean by hand; already contains a duplicate and three gaps | 3 |
| `salary_data.csv` | 375 × 2 | one feature, one line — and 220 duplicate rows to find first | 3, 9 |
| `advertising.csv` | 200 × 4 | a real, clean spend-versus-sales relationship | 1 |
| `iris.csv` | 150 × 5 | the standard clean multiclass problem; 3 duplicates | 10 |
| `heart_failure_raw.csv` | 299 × 14 | 45 missing values across 3 columns, numbers stored as text | 3, 7 |
| `Mall_Customers.csv` | 200 × 5 | visible cluster structure with unequal scales | 10 |
| `cardekho_dataset.csv` | 15,411 × 14 | strongly skewed prices; mean and median disagree | 4, 7, 8 |
| `loan_data_10k.csv` | 10,000 × 14 | imbalanced target, mixed types, columns on different scales | 5, 16 |

## Generated datasets

One script per session. Run any of them on its own:

```bash
python datasets/make_session_07.py     # just Session 7's files
python datasets/make_all.py            # all sixteen
```

| Script | Produces | The property it exists for |
|---|---|---|
| `make_session_01.py` | `orders.csv` · `orders.json` · `order_notes.txt` · `flats.csv` · `daily_demand.csv` · `film_ratings.csv` · `daily_price.csv` | the same facts in three formats; a gap to fill |
| `make_session_02.py` | `town_incomes.csv` · `messy_customers.csv` · `shop_sales.csv` · `inventory.xlsx` · `survey_ages_typo.csv` | a population with real subgroup differences; every cleaning problem in ten rows |
| `make_session_03.py` | `sensor_readings.csv` | noise on a known signal, so smoothing can be scored against the truth |
| `make_session_04.py` | `customers.csv` · `purchases.csv` · `regions_dirty.csv` · `sales_jan/feb/mar.csv` · `subscribers_*.csv` | joins that lose rows, multiply rows, and fail on key formatting |
| `make_session_05.py` | `pure_noise.csv` · `city_rent.csv` · `six_earners.csv` · `loan_applicants.csv` · others | a target that is literally a coin flip; categories with no ordering |
| `make_session_06.py` | `signal_and_noise.csv` · `body_measurements.csv` · `survey_responses.csv` · `salaries_large.csv` · others | 3 real columns against 190 junk ones; 12 questions from 4 hidden factors |
| `make_session_07.py` | `team_salaries.csv` · `three_shapes.csv` · `daily_returns.csv` · `two_cohorts.csv` · others | skew, kurtosis and bimodality with known values |
| `make_session_08.py` | `city_homes.csv` · `four_relationships.csv` · `icecream_drownings.csv` · `cubic_pair.csv` | a confounder we planted, so it can be proved |
| `make_session_09.py` | `house_prices.csv` · `fuel_efficiency.csv` · `experience_salary.csv` | known coefficients the model must recover; a curve a line cannot fit |
| `make_session_10.py` | `three_blobs.csv` · `moons.csv` · `random_noise.csv` | shapes K-Means handles, shapes it cannot, and data with no structure at all |
| `make_session_11.py` | `noisy_line.csv` · `weak_signal.csv` · `residual_cases.csv` · others | a signal weak enough that tuning on the test set visibly cheats |
| `make_session_12.py` | `house_prices_simple.csv` · `property_portfolio.csv` · `incoming_requests.csv` | a batch-scoring input, and live inputs that drift |
| `make_session_13.py` | `transactions.csv` (200k) · `regional_sales.csv` | a file worth chunking; a trend that reverses by region |
| `make_session_14.py` | `word_count_lines.txt` · `chunks/*.csv` · `server_logs.csv` · `uneven_groups.csv` | one logical table split across files, as HDFS would |
| `make_session_15.py` | `product_catalog.json` · `store_sales.json` · `overplot_points.csv` (200k) · `request_logs.csv` (300k) · `customers_by_signup.csv` (200k) | records that do not share a shape; enough points to overplot; rows ordered so `head()` lies |
| `make_session_16.py` | `telecom_churn.csv` · `grocery_baskets.csv` · `baskets_small.txt` | three association rules planted on purpose, so the algorithm can be checked |

## Formats

The course deliberately uses more than one, because real data arrives in more than one:

| Format | Files | Introduced in |
|---|---|---|
| CSV | most | Session 1 |
| JSON | `orders.json`, `product_catalog.json`, `store_sales.json` | Sessions 1, 15 |
| Plain text | `order_notes.txt`, `word_count_lines.txt`, `baskets_small.txt` | Sessions 1, 14, 16 |
| Excel | `inventory.xlsx` | Session 2 |
| SQL | built from `orders.csv` into an in-memory SQLite database | Session 2 |
| Many files as one table | `chunks/city_sales_*.csv` | Session 14 |

## Licence and provenance

The real files are redistributed from the course catalog linked above, retrieved
2026-09-11. Generated files are synthetic and carry no restrictions.
