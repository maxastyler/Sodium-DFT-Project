#!/usr/bin/env stack
-- stack --resolver lts-10.3 script
{-# LANGUAGE NoMonomorphismRestriction #-}
{-# LANGUAGE FlexibleContexts #-}
{-# LANGUAGE TypeFamilies #-}

-- Run with 
-- $ stack figure_generator.hs -o test.svg -w 400 && feh --magick-timeout 1 test.svg

import Diagrams.Prelude
import Diagrams.Backend.SVG.CmdLine

myCircle :: Diagram B
myCircle = circle 1

linspace :: (Num a, Fractional a) => a -> Int -> a -> [a]
linspace x1 n x2 = take n $ iterate ((+) diff) x1
    where diff = (x2-x1) / (fromIntegral n)

lattice_basis = [(unitX), rotateBy (0.1) unitY]

points = [ origin .+^ (fromIntegral a * (lattice_basis!!0)) .+^ (fromIntegral b * (lattice_basis!!1)) | a<-[(-2)..2], b<-[(-2)..2]]
p_1 = origin
p_2 = p2 (1, 1)


arrowText p n =  text (n) # fontSizeL 0.2 # translate p

arrows = mconcat $ map (\x -> arrowBetween origin (origin .+^ x)) lattice_basis

lattice_basis_diagram :: Diagram B
lattice_basis_diagram =  arrowText (r2 (-0.14, 0.4)) "v2" <> arrowText (r2 (0.48, 0.10)) "v1" <> arrows <> atPoints points ( repeat $ circle 0.1 # fc green )  
main = mainWith lattice_basis_diagram
