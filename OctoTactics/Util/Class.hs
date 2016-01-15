{-# LANGUAGE
    NoImplicitPrelude,
    MultiParamTypeClasses,
    FlexibleInstances,
    FunctionalDependencies
    #-}

module OctoTactics.Util.Class where

import Data.Functor (Functor, fmap)
import Data.Either (Either(..))
import Data.Function ((.), id)

class Functor' f a b where
    fmap' :: (a -> b) -> f a -> f b

instance Functor f => Functor' f a b where
    fmap' = fmap

class Bifunctor f where
    bifmap :: (a -> c) -> (b -> d) -> f a b -> f c d
    lmap :: (a -> c) -> f a b -> f c b
    rmap :: (b -> c) -> f a b -> f a c
    
    lmap l = bifmap l id
    rmap r = bifmap id r
    bifmap l r = lmap l . rmap r
    
    {-# MINIMAL bifmap | lmap, rmap #-}

instance Bifunctor Either where
    bifmap l _ (Left x)  = Left  (l x)
    bifmap _ r (Right y) = Right (r y)

instance Bifunctor (,) where
    bifmap l r (x, y) = (l x, r y)

class Swap f where
    swap :: f a b -> f b a

instance Swap Either where
    swap (Left x)  = Right x
    swap (Right y) = Left  y

instance Swap (,) where
    swap (x, y) = (y, x)
    
class Assoc a b where
    assoc :: a -> b

instance Assoc ((a, b), c) (a, (b, c)) where assoc ((x, y), z) = (x, (y, z))
instance Assoc (a, (b, c)) ((a, b), c) where assoc (x, (y, z)) = ((x, y), z)

instance Assoc (Either a (Either b c)) (Either (Either a b) c) where assoc (Left         x ) = Left  (Left  x)
                                                                     assoc (Right (Left  y)) = Left  (Right y)
                                                                     assoc (Right (Right z)) = Right        z
instance Assoc (Either (Either a b) c) (Either a (Either b c)) where assoc (Left (Left  x))  = Left         x 
                                                                     assoc (Left (Right y))  = Right (Left  y)
                                                                     assoc (Right       z )  = Right (Right z)