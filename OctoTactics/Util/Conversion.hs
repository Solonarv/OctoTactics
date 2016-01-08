{-# LANGUAGE
    MagicHash,
    NoImplicitPrelude
    #-}

module OctoTactics.Util.Conversion (
    intToDouble
    ) where

import GHC.Prim (int2Double#)
import GHC.Types (Int(I#), Double(D#))

-- VERY VERY FAST, usage of GHC primitive operations means this is basically one machine instruction
intToDouble :: Int -> Double
intToDouble (I# i) = D# (int2Double# i)