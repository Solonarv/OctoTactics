module OctoTactics.Model.Cell (
    type Cell(..), 
    CellType(..),
    newCell,
    cell
    ) where

import Data.Set (Set)
import qualified Data.Set as Set

import Data.Array (Array)
import qualified Data.Array as Array

import OctoTactics.Data.Direction
import OctoTactics.Model.Player (Player)

-- | The cell type itself
data Cell = Cell { !cPosition    :: (Int, Int)
                 , !cType        :: CellType
                 , !cEnergy      :: Double
                 , !cConnections :: Set (Int, Int)
                 , !cSide        :: Player
                 }

-- | Stores information about cell types.
data CellType = CellType { !legalDirections   :: (Set Direction)
                         , !maxTargets        :: Int
                         , !startingEnergy    :: Double
                         , !regenRate         :: Double
                         , !transferRates     :: Array Int Double
                         , !receptionModifier :: Double
                         }
                deriving (Eq, Show)

octagon = CellType { legalDirections   = Set.fromList [North .. NorthWest]
                   , maxTargets        = 3
                   , startingEnergy    = 5
                   , regenRate         = 3.75
                   , transferRates     = listArray (0, 3) [0, 0.216, 0.146, 0.122]
                   , receptionModifier = 1
                   }

square  = CellType { legalDirections   = Set.fromList [North, East, South, West]
                   , maxTargets        = 1
                   , startingEnergy    = 5
                   , regenRate         = 3
                   , transferRates     = listArray (0, 1) [0, 0.35]
                   , receptionModifier = 0.8
                   }

-- | Create a new cell, with no connections.
newCell :: (Int, Int) -- ^ The cell's position
        -> CellType   -- ^ The cell's type
        -> Cell
newCell pos typ = Cell pos typ (startingEnergy typ) Set.empty

-- | Smart constructor for Cell
cell :: (Int, Int)`    -- ^ the cell's position
     -> CellType       -- ^ the cell's type
     -> Double         -- ^ the cell's energy
     -> Set (Int, Int) -- ^ the locations of the cells this cell is connected to
     -> Maybe Cell
cell pos typ energy connections = if connections `Set.isSubsetOf` (legalDirections typ) && length connections <= maxTargets typ
                                  then Just (Cell pos typ energy connections)
                                  else Nothing