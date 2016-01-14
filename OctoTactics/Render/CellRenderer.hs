{-# LANGUAGE
    NoImplicitPrelude,
    RecordWildCards
    #-}

module OctoTactics.Render.CellRenderer where

import OctoTactics.Util.ImprovedPrelude

import OctoTactics.Model.Cell
import qualified OctoTactics.Model.Player as Player (color)

import qualified Graphics.Gloss as Gloss

type CellRenderer = Cell -> Picture

renderSquare :: CellRenderer
renderSquare = CellRenderer $ const $ Polygon $ rectanglePath 20 20

renderOctogon :: CellRenderer
renderOctogon = CellRenderer $ const $ Polygon [ (20, 1)
                                               , (50, 1)
                                               , (69, 20)
                                               , (69, 50)
                                               , (50, 69)
                                               , (20, 69)
                                               , (1, 50)
                                               , (1, 20)]