module OctoTactics.Model.Player where

-- Good enough for now
data Player = Red | Blue deriving (Eq, Show)

allied :: Player -> Player -> Bool
allied = (==)