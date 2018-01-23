#!/usr/bin/env stack
-- stack --resolver lts-10.3 script
{-# LANGUAGE NoMonomorphismRestriction #-}
{-# LANGUAGE FlexibleContexts #-}
{-# LANGUAGE TypeFamilies #-}

-- Run with 
-- $ stack figure_generator.hs -o name.svg -w 400 && feh --magick-timeout 1 name.svg

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

sodium :: Diagram B
sodium = text "Na" # fc white <> circle 1 # fc red

chlorine :: Diagram B
chlorine = text "Cl" # fc white <> circle 1.5 # fc purple

cubic_points = [ origin .+^ (fromIntegral a * (unitX)) .+^ (fromIntegral b * (unitY)) | a<-[(-2)..2], b<-[(-2)..2]]
na_points = cubic_points
cl_points = map (\x -> x .+^(r2 (0.5, 0))) cubic_points

fcc_cross_section = [ origin .+^ (fromIntegral a * (unitX)) .+^ (fromIntegral b * (r2 (0.5, 0.5))) | a<-[(-2)..2], b<-[(-2)..2]]

nacltext p n =  text (n) # fontSizeL 0.1 # translate p

na_cl :: Diagram B
na_cl = rectEnvelope (p2 (-1.25, -1.25)) (r2 (2, 2)) $ nacltext (r2(-0.85, -0.75)) "v2" <> nacltext (r2(-0.74, -1.07)) "v1" <> (arrowBetween (p2(-1, -1)) (p2(0, -1))) <> (arrowBetween (p2(-1, -1)) (p2(-0.5, -0.5))) <>  (atPoints fcc_cross_section $ repeat na_cl_basis)

na_cl_basis :: Diagram B
na_cl_basis = atPoints [p2 (0, 0), p2 (0.5, 0)] [sodium # scale 0.1, chlorine # scale 0.1]
main = mainWith na_cl_basis
