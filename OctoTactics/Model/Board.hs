module OctoTactics.Model.Board where

import Control.Arrow

import Data.Array (Array)
import qualified Data.Array as Array

import OctoTactics.Util.Functional ((<$$>))

import OctoTactics.Model.Cell

import OctoTactics.Data.Direction

type Position = Position

type Board a = Array Position (Position, a)

data BoardType = Cutoff | Toroidal

tick :: Board Cell
     -> Board Cell
tick = addEnergy . drainCells . generateEnergy

generateEnergy :: Board Cell -> Board Cell
generateEnergy = fmap \c -> c { cEnergy = cEnergy c + regenRate (cType c) }

drainCells :: Board Cell
           -> Board (Cell, Set (Position, Double))
drainCells b = b <$$> \(pos, c) -> let targets    = cConnections c
                                       ccount     = length (cConnections c)
                                       energy     = cEnergy c
                                       baseAmount = energy * transferRates (cType c) ! ccount
                                       transfers  = targets <$$> \tpos -> let tc = b ! tpos
                                                                              modifier = receptionModifier (cType tc) * (if tc `allied` c then 1 else -1)
                                                                          in (tpos, baseAmount * modifier)
                                          next       = c { cEnergy = energy - sum (snd <$> transfers) }
                                      in ((x, y), (next, transfers))

addEnergy :: Board (Cell, Set (Position, Double))
          -> Board Cell
addEnergy b = b <$$> \(pos, (c, _)) -> let deltaE = sum $  b <$$> snd <$>> \(c', ts) -> ts <? ((== pos) . fst) <$$> snd
                                       in c { cEnergy = cEnergy c + deltaE }