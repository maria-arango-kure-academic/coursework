# Fallacy pairs

A matching game for the course Technology and Society at Jönköping International Business School. Six cards each show one argument. The player picks the two that commit the same fallacy, and a matched pair turns over to show the fallacy's name, definition and type.

A game runs round after round. Each match earns 100 points plus a time bonus, clearing a round earns 200, and a wrong pair costs one of three lives. When the lives run out, a score that reaches the top 10 is saved with the player's name and the date.

## Run it

The page needs a web server, because it loads `fallacies.json` at start.

```
python -m http.server 8000
```

Then open `http://localhost:8000`.

## Files

- `index.html`: the page, its styles and the game. The rules are the constants at the top of the script.
- `fallacies.json`: the fallacies and their examples.
- `wg/`: the interface kit, fonts and grid tiles used by the page.

## Add fallacies or examples

Edit `fallacies.json`. Each fallacy has `n`, `name`, `type`, `definition` and a list of `examples`. A fallacy is dealt once it has two examples. When it has more, two are drawn at random each round.

## Scores

The top 10 is one JSON list, read from and written to `/api/blob/fallacy-pairs-top10` on the same host. Any small JSON store that answers `GET` and `PUT` at that address will do. Without one, the game still works and keeps the scores in the player's own browser.

Maria Arango-Kure, 2026
