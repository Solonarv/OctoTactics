{-# LANGUAGE
    NoImplicitPrelude
    #-}

module OctoTactics.Model.Board where

import Control.Arrow

import Data.Array (Array, (!), (//))
import qualified Data.Array as Array

import Data.Set (Set)
import qualified Data.Set as Set

import OctoTactics.Util.ImprovedPrelude
import OctoTactics.Model.Cell
import OctoTactics.Model.Player
import OctoTactics.Data.Direction

type Position = (Int, Int)

type Board a = Array Position (Position, a)

data BoardType = Cutoff | Toroidal

tick :: Board Cell
     -> Board Cell
tick = addEnergy . drainCells . generateEnergy

generateEnergy :: Board Cell
               -> Board Cell
generateEnergy = fmap $ second $ \c -> c { cEnergy = cEnergy c + regenRate (cType c) }

drainCells :: Board Cell
           -> Board (Cell, Set (Position, Double))
drainCells b = b <$$> \(pos, c) -> let targets    = cConnections c
                                       ccount     = length (cConnections c)
                                       energy     = cEnergy c
                                       baseAmount = energy * transferRates (cType c) ! ccount
                                       transfers  = targets <$$> \tpos -> let tc = snd $ b ! tpos
                                                                              modifier = receptionModifier (cType tc) * (if cSide tc `allied` cSide c then 1 else -1)
                                                                          in (tpos, baseAmount * modifier)
                                       next       = c { cEnergy = energy - sum (snd <$> transfers) }
                                   in (pos, (next, transfers))

addEnergy :: Board (Cell, Set (Position, Double))
          -> Board Cell
addEnergy b = b <$$> \(pos, (c, _)) -> let deltaE = sum $  b <$$> snd $>>= \(c', ts) -> ts <? ((== pos) . fst) <$$> snd
                                       in (pos, c { cEnergy = cEnergy c + deltaE })

cellAt :: Position -> Board a -> a
cellAt p = snd . (! p)

setCell :: Position -> a -> Board a -> Board a
setCell pos c bd = bd // [(pos, (pos, c))]