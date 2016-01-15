{-# LANGUAGE
    NoImplicitPrelude,
    RecordWildCards
    #-}

module OctoTactics.Render.CellRenderer where

import OctoTactics.Util.ImprovedPrelude

import qualified OctoTactics.Model.Player as Player
import OctoTactics.Model.Player (Player)

import Graphics.Gloss (Picture(..), rectanglePath)

type CellRenderer = Maybe Player -> Double -> Picture

renderSquare :: CellRenderer
renderSquare = const2 $ Polygon $ rectanglePath 20 20

renderOctogon :: CellRenderer
renderOctogon = const2 $ Polygon [ (20, 1)
                                     , (50, 1)
                                     , (69, 20)
                                     , (69, 50)
                                     , (50, 69)
                                     , (20, 69)
                                     , (1, 50)
                                     , (1, 20)]