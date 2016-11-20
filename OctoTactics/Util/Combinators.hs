{-# LANGUAGE
    NoImplicitPrelude,
    LambdaCase
    #-}


module OctoTactics.Util.Combinators where

import Prelude hiding ((<$>))

import OctoTactics.Util.Class

import Data.Foldable (Foldable, toList)
import Data.Bifunctor

const2 :: a -> b -> c -> a
const2 = const . const

on :: (b -> b -> c) -> (a -> b) -> (a -> a -> c)
op `on` f = curry (uncurry op . both f)

both :: (a -> b) -> (a, a) -> (b, b)
both = twice bimap

both2 :: (a -> b -> c) -> (a, a) -> (b, b) -> (c, c)
both2 f (a, b) (c, d) = (f a c, f b d)

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
(<?) = flip filter . toList

infixl 4 $>>=
($>>=) :: (Foldable t, Foldable u) => t a -> (a -> u b) -> [b]
xs $>>= f = concatMap (toList . f) xs

infixr 6 \/
(\/) :: (a -> c) -> (b -> c) -> Either a b -> c
l \/ r = dedup . bimap l r

infixr 7 /\
(/\) :: (a -> b) -> (a -> b) -> a -> (b, b)
l /\ r = bimap l r . dup

dedup :: Either a a -> a
dedup (Left x)  = x
dedup (Right y) = y

dup :: a -> (a, a)
dup x = (x, x)

twice :: (a -> a -> b) -> a -> b
twice f x = f x x

infixl 4 #$>, #$$>
(#$>) :: Bifunctor f => (a -> c, b -> d) -> f a b -> f c d
(#$>) = uncurry bimap

(#$$>) :: Bifunctor f => f a b -> (a -> c, b -> d) -> f c d
(#$$>) = flip $ uncurry bimap

keep :: (a -> b) -> a -> (a, b)
keep f = second f . dup