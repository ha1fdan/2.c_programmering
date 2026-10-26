# Kiosk Checkout

A self-checkout kiosk that identifies items by weight. Customers place items on a serial scale one at a time, and the kiosk works out what each one is by comparing the added weight with the items in the database.

## Features

- [x] Read stable weights from a serial scale (auto-detects the FT230X adapter)
- [x] Item database in SQLite (name, category, price, weight, tolerance, stock)
- [x] CLI for adding, updating, deleting and listing items (`add_item.py`)
- [x] Self-checkout page that identifies items by weight alone
- [x] Pick from a list when several items have a similar weight
- [x] Block payment when the scale and basket disagree
- [x] Stock is reduced on checkout
- [x] Inventory admin panel (`/admin`) with optional password
- [x] Fill an item's weight straight from the scale in the admin panel
- [ ] Real payment integration
- [ ] Receipt printing
- [ ] Recognise several items placed at once
- [ ] Sales history and reports
- [ ] Multiple scales / units
- [x] Automated tests (pytest)

## Requirements

- Python 3.14 (see `.python-version`)
- A serial scale connected through an FT230X USB-UART adapter, 9600 baud
- [uv](https://docs.astral.sh/uv/) or pip

Dependencies are listed in `requirements.txt` (`pyserial` for the scale, `flask` for the web app).

## Setup

```sh
uv venv
uv pip install -r requirements.txt
```

## Usage

### Run the kiosk

```sh
uv run python3 main.py
```

Then open <http://127.0.0.1:5000>. The app exits at startup if no serial port with `FT230X Basic UART` in its name is found.

### Admin panel

Open <http://127.0.0.1:5000/admin> to edit the inventory. To require a login, set a password when starting the app (any username works):

```sh
KIOSK_ADMIN_PASSWORD=secret uv run python3 main.py
```

Without it, `/admin` is open to anyone who can reach the page.

### Manage items from the command line

```sh
uv run python3 add_item.py add "Cola" 15 532 --category drinks --stock 24
uv run python3 add_item.py update Cola --price 16 --stock 20
uv run python3 add_item.py delete Cola
uv run python3 add_item.py list
```

`add` takes a name, a price in DKK and the weight of one item in grams. Optional flags are `--category`, `--tolerance` (grams, default 5) and `--stock` (default 0).

## Tests

```sh
uv pip install -r requirements-dev.txt
uv run pytest
```

The tests use a fake scale and a temporary database, so no hardware is needed and `kiosk.db` is never touched.

## How it works

1. A background thread reads lines from the scale and keeps the latest stable weight in grams. Fragments and unstable (`?`) readings are discarded.
2. The kiosk page polls the weight and waits for it to settle.
3. The difference from the last accounted-for weight is matched against each item's weight within its tolerance.
4. One match adds the item, several matches ask the customer to choose, and no match shows "not recognised".
5. **Pay** unlocks only when the scale agrees with the basket.

Give every item a tolerance that is large enough to cover scale noise but smaller than the weight gap to similar items.

## Project layout

```
main.py           Flask app and scale reader
add_item.py       CLI for managing items (also defines the table schema)
templates/
  kiosk.html      Customer checkout page
  admin.html      Inventory admin panel
tests/            pytest suite
kiosk.db          SQLite database
```

## Notes

- Weights are in grams and prices in DKK throughout.
- The server listens on `127.0.0.1` only. Change `host` in `main.py` to expose it to other devices.
