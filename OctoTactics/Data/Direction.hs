module OctoTactics.Data.Direction (
    Direction(..),
    opposite
    ) where

import Data.List.Split (chunksOf)

data Direction = North
               | NorthEast
               | East
               | SouthEast
               | South
               | SouthWest
               | West
               | NorthWest
               deriving (Show, Eq, Ord, Bounded)

instance Enum Direction where
    succ North = NorthEast
    succ NorthEast = East
    succ East = SouthEast
    succ SouthEast = South
    succ South = SouthWest
    succ SouthWest = West
    succ West = NorthWest
    succ NorthWest = North
    
    pred NorthEast = North
    pred East = NorthEast
    pred SouthEast = East
    pred South = SouthEast
    pred SouthWest = South
    pred West = SouthWest
    pred NorthWest = West
    pred North = NorthWest
    
    toEnum 0 = North
    toEnum 1 = NorthEast
    toEnum 2 = East
    toEnum 3 = SouthEast
    toEnum 4 = South
    toEnum 5 = SouthWest
    toEnum 6 = West
    toEnum 7 = NorthWest
    toEnum n = toEnum (n `mod` 8)
    
    fromEnum North = 0
    fromEnum NorthEast = 1
    fromEnum East = 2
    fromEnum SouthEast = 3
    fromEnum South = 4
    fromEnum SouthWest = 5
    fromEnum West = 6
    fromEnum NorthWest = 7
    
    enumFrom = iterate succ
    enumFromThen s t = iterate (succ `fpow` ((fromEnum t - fromEnum s) `mod` 8)) s
        where fpow 0 _ = id
              fpow n f = f . fpow (n-1) f
    enumFromTo s e = take ((fromEnum e - fromEnum s) `mod` 8) $ enumFrom s
    enumFromThenTo s t e = map head $ chunksOf ((fromEnum t - fromEnum s) `mod` 8) $ enumFromTo s e

opposite :: Direction -> Direction
opposite = succ . succ . succ . succ