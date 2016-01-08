module OctoTactics.Model.Board where

import Data.Array (Array)
import qualified Data.Array as Array

import OctoTactics.Model.Cell

type Board = Array (Int, Int) Cell