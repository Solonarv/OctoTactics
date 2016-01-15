{-# LANGUAGE
    StandaloneDeriving,
    DeriveFunctor,
    FlexibleInstances,
    KindSignatures,
    ConstraintKinds,
    MultiParamTypeClasses,
    NoImplicitPrelude
    #-}

module OctoTactics.Util.ImprovedPrelude (
    module Prelude,
    module OctoTactics.Util.ImprovedPrelude,
    module OctoTactics.Util.Combinators
    ) where

import Prelude hiding ((<$>))
import Data.Set (Set)
import qualified Data.Set as Set

import OctoTactics.Util.Combinators
import OctoTactics.Util.Class

instance {-# OVERLAPPING #-} Ord b => Functor' Set a b where
    fmap' = Set.map

