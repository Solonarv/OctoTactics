{-# LANGUAGE
    NoImplicitPrelude
    #-}


module OctoTactics.Model.Player where

import OctoTactics.Util.ImprovedPrelude

-- Good enough for now
data Player = Red | Blue deriving (Eq, Show)

allied :: Maybe Player -> Maybe Player -> Bool
allied = (==)