{-# LANGUAGE
    ExplicitNamespaces,
    NoImplicitPrelude
    #-}

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
import OctoTactics.Render.CellRenderer (CellRenderer(DummyRenderer))
import OctoTactics.Util.ImprovedPrelude
import OctoTactics.Util.Conversion (intToDouble)

-- | The cell type itself
data Cell = Cell { cPosition    :: !(Int, Int)
                 , cType        :: !CellType
                 , cEnergy      :: !Double
                 , cConnections :: !(Set (Int, Int))
                 , cSide        :: !(Maybe Player)
                 }

-- | Stores information about cell types.
data CellType = CellType { legalDirections   :: !(Set Direction)
                         , maxTargets        :: !Int
                         , startingEnergy    :: !Double
                         , regenRate         :: !Double
                         , transferRates     :: !(Array Int Double)
                         , receptionModifier :: !Double
                         , renderer          :: !CellRenderer
                         , rangeSquared      :: !Double
                         }
                deriving (Eq, Show)

octogon = CellType { legalDirections   = Set.fromList [North .. NorthWest]
                   , maxTargets        = 3
                   , startingEnergy    = 5
                   , regenRate         = 3.75
                   , transferRates     = Array.listArray (0, 3) [0, 0.216, 0.146, 0.122]
                   , receptionModifier = 1
                   , renderer          = renderOctogon
                   , rangeSquared      = 1.1
                   }

square  = CellType { legalDirections   = Set.fromList [North, East, South, West]
                   , maxTargets        = 1
                   , startingEnergy    = 5
                   , regenRate         = 3
                   , transferRates     = Array.listArray (0, 1) [0, 0.35]
                   , receptionModifier = 0.8
                   , renderer          = renderSquare
                   , rangeSquared      = 2.2
                   }

-- | Create a new cell, with no connections.
newCell :: (Int, Int)   -- ^ The cell's position
        -> CellType     -- ^ The cell's type
        -> Maybe Player -- ^ The cell's owner
        -> Cell
newCell pos typ = Cell pos typ (startingEnergy typ) Set.empty

-- | Smart constructor for Cell
cell :: (Int, Int)     -- ^ The cell's position
     -> CellType       -- ^ The cell's type
     -> Double         -- ^ The cell's energy
     -> Set (Int, Int) -- ^ The locations of the cells this cell is connected to
     -> Maybe Player   -- ^ The cell's owner
     -> Maybe Cell
cell pos typ energy connections owner = if length connections <= maxTargets typ && all ((<= rangeSquared typ) . intToDouble . uncurry (*) . both abs. both2 (-) pos) connections
                                        then Just (Cell pos typ energy connections owner)
                                        else Nothing