{-# LANGUAGE
    NoImplicitPrelude,
    DeriveFunctor,
    LambdaCase
    #-}

module OctoTactics.Model.BoardManipulate where

import Control.Monad.Free
import Control.Monad.State

import Data.Set (union, singleton)

import OctoTactics.Model.Board
import OctoTactics.Model.Cell

import OctoTactics.Util.ImprovedPrelude

data BoardManipulateF next = Tick next
                           | GetCell Position (Cell -> next)
                           | TargetCell Position Position (Bool -> next)
                           deriving Functor

type BoardManipulate = Free BoardManipulateF

eval :: BoardManipulate a -> State (Board Cell) a
eval = foldFree $ \case
     Tick next            -> modify tick >> eval (return next)
     GetCell pos f        -> gets (cellAt pos) >>= eval . return . f
     TargetCell pos tar f -> do cell <- gets (cellAt pos)
                                let (x, y) = pos
                                    (x', y') = tar
                                    conns = cConnections cell
                                if (fromIntegral ((x' - x)^2 + (y' - y)^2) > rangeSquared (cType cell) || length conns >= maxTargets (cType cell))
                                then eval (return (f False))
                                else modify (setCell pos (cell {cConnections = conns `union` (singleton pos)} )) >> eval (return (f True))