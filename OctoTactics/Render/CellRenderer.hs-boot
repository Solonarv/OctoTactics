module OctoTactics.Render.CellRenderer where

import Graphics.Gloss (Picture)

import OctoTactics.Model.Cell (Cell)

type CellRenderer = Cell -> Picture

renderSquare :: CellRenderer
renderOctogon :: CellRenderer