{-# LANGUAGE
    MagicHash,
    NoImplicitPrelude
    #-}

module OctoTactics.Util.Conversion (
    intToDouble
    ) where

import GHC.Prim (int2Double#)
import GHC.Types (Int(I#), Double(D#))

-- One machine instruction.
intToDouble :: Int -> Double
intToDouble (I# i) = D# (int2Double# i)