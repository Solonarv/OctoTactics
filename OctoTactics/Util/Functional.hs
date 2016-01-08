module OctoTactics.Util.Functional where

infixl 4 <$$>
(<$$>) :: Functor f => f a -> (a -> b) -> f b
(<$$>) = flip fmap

fpow :: Int -> (a -> a) -> (a -> a)
fpow 0 _ = id
fpow n f = f . fpow (n-1) f

infixl 4 <?
(<?) :: Foldable t => t a -> (a -> Bool) -> [a]
(<?) = flip filter . toList

infixl 4 <$>>
(<$>>) :: (Foldable t, Foldable u) => t a -> (a -> u b) -> [b]
xs <$>> f = concatMap (toList . f) xs