# household

Small helpers for sharing a household's bills.

- `split_bill(total_cents, people)` splits a bill into whole cents. The shares always add up to exactly
  `total_cents`; the cents left over go one each to the first people in the list, so a share never differs from
  another by more than one cent.
- `due_dates(first, count)` lists the dates of `count` monthly payments, starting on `first` and falling on the
  same day of each following month (the last day of a shorter month when that day does not exist).

Run the tests with `python3 -m unittest -q`.
