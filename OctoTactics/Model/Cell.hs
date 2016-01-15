{-# LANGUAGE
    ExplicitNamespaces,
    NoImplicitPrelude,
    TemplateHaskell
    #-}

module OctoTactics.Model.Cell (
    type Cell(..),
    HasCell(..),
    HasCellType(..),
    CellType(..),
    newCell,
    mkCell
    ) where

import Data.Set (Set)
import qualified Data.Set as Set

import Data.Array (Array)
import qualified Data.Array as Array

import Control.Lens hiding (both)

import OctoTactics.Data.Direction
import OctoTactics.Model.Player (Player)
import OctoTactics.Render.CellRenderer (CellRenderer, renderOctogon, renderSquare)
import OctoTactics.Util.ImprovedPrelude
import OctoTactics.Util.Conversion (intToDouble)

                 
-- | Stores information about _cell types.
data CellType = CellType { _legalDirections   :: !(Set Direction)
                         , _name              :: !String
                         , _maxTargets        :: !Int
                         , _startingEnergy    :: !Double
                         , _regenRate         :: !Double
                         , _transferRates     :: !(Array Int Double)
                         , _receptionModifier :: !Double
                         , _renderer          :: !CellRenderer
                         , _rangeSquared      :: !Double
                         }

makeClassy ''CellType

-- | The _cell type itself
data Cell = Cell { _cType        :: !CellType
                 , _cEnergy      :: !Double
                 , _cConnections :: !(Set (Int, Int))
                 , _cSide        :: !(Maybe Player)
                 }

makeClassy ''Cell

instance HasCellType Cell where
    cellType = lens _cType $ \c t -> (cType.~t) c

instance Eq CellType where
    (==) = (==) `on` _name

octogon = CellType { _legalDirections   = Set.fromList [North .. NorthWest]
                   , _name              = "octogon"
                   , _maxTargets        = 3
                   , _startingEnergy    = 5
                   , _regenRate         = 3.75
                   , _transferRates     = Array.listArray (0, 3) [0, 0.216, 0.146, 0.122]
                   , _receptionModifier = 1
                   , _renderer          = renderOctogon
                   , _rangeSquared      = 1.1
                   }

square  = CellType { _legalDirections   = Set.fromList [North, East, South, West]
                   , _name              = "square"
                   , _maxTargets        = 1
                   , _startingEnergy    = 5
                   , _regenRate         = 3
                   , _transferRates     = Array.listArray (0, 1) [0, 0.35]
                   , _receptionModifier = 0.8
                   , _renderer          = renderSquare
                   , _rangeSquared      = 2.2
                   }

-- | Create a new cell, with no connections.
newCell :: CellType     -- ^ The cell's type
        -> Maybe Player -- ^ The cell's owner
        -> Cell
newCell typ = Cell typ (typ^.startingEnergy) Set.empty

-- | Smart _constru_ctor for Cell
mkCell :: CellType       -- ^ The cell's type
       -> Double         -- ^ The cell's energy
       -> Set (Int, Int) -- ^ The locations of the cells this cell is connected to
       -> Maybe Player   -- ^ The cell's owner
       -> Maybe Cell
mkCell typ energy connections owner = if length connections <= typ^.maxTargets -- && all ((<= (typ^.rangeSquared)) . intToDouble . uncurry (*) . both abs. both2 (-) pos) connections
                                      then Just (Cell typ energy connections owner)
                                      else Nothing