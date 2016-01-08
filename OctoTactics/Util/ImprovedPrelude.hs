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
    module OctoTactics.Util.ImprovedPrelude
    ) where

import Prelude hiding ((<$>))
import Data.Foldable as F (Foldable, toList)
import Data.Set (Set)
import qualified Data.Set as Set


infixl 4 <$$>
(<$$>) :: Functor' f a b => f a -> (a -> b) -> f b
(<$$>) = flip fmap'

infixl 4 <$>
(<$>) :: Functor' f a b => (a -> b) -> f a -> f b
(<$>) = fmap'

fpow :: Int -> (a -> a) -> (a -> a)
fpow 0 _ = id
fpow n f = f . fpow (n-1) f

infix 9 $^
($^) = flip fpow

infixl 4 <?
(<?) :: Foldable t => t a -> (a -> Bool) -> [a]
(<?) = flip filter . F.toList

infixl 4 <$>>
(<$>>) :: (F.Foldable t, F.Foldable u) => t a -> (a -> u b) -> [b]
xs <$>> f = concatMap (F.toList . f) xs

both :: (a -> b) -> (a, a) -> (b, b)
both f (a, b) = (f a, f b)

both2 :: (a -> b -> c) -> (a, a) -> (b, b) -> (c, c)
both2 f (a, b) (c, d) = (f a c, f b d)

class Functor' f a b where
    fmap' :: (a -> b) -> f a -> f b

instance Functor f => Functor' f a b where
    fmap' = fmap

instance {-# OVERLAPPING #-} Ord b => Functor' Set a b where
    fmap' = Set.map

