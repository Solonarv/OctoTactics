{-# LANGUAGE
    NoImplicitPrelude
    #-}


module OctoTactics.Model.Player where

import OctoTactics.Util.ImprovedPrelude

-- Good enough for now
data Player = Red | Blue deriving (Eq, Show)

allied :: Maybe Player -> Maybe Player -> Bool
allied = (==)

color :: Maybe Player -> (Int, Int, Int)
color Nothing     = (255, 255, 255)
color (Just Red)  = (255, 0,   0  )
color (Just Blue) = (0,   0,   255)