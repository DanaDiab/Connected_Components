#!/usr/bin/env python3
"""
compute sizes of all connected components.
sort and display.
"""

from math import sqrt
from timeit import timeit
from sys import argv
from geo.tycat import tycat
from geo.point import Point
from geo.quadrant import Quadrant
from math import floor


def load_instance(filename):
    """
    loads .pts file.
    returns distance limit and points.
    """
    with open(filename, "r") as instance_file:
        lines = iter(instance_file)
        distance = float(next(lines))
        points = [Point([float(f) for f in l.split(",")]) for l in lines]

    return distance, points


def print_components_sizes(distance, points):
    """
    affichage des tailles triees de chaque composante
    """
    print(methode_performante(distance,points))



def methode_naive(distance, points):
    """ Resolution du problème par la méthode naïve, qui sera expliqué en détails dans le rapport """
    visited = set()
    composantes = []
    for point in points:
        if point not in visited:
            composante = set()
            to_visit = [point]
            while to_visit:
                curr = to_visit.pop()
                if curr not in visited:
                    visited.add(curr)
                    composante.add(curr)
                    voisins = [p for p in points if p not in visited and curr.distance_to(p) <= distance]
                    to_visit.extend(voisins)
            composantes.append(composante)
    sizes = [len(composante) for composante in composantes]
    sizes.sort(reverse=True)
    return sizes


def methode_performante(distance, points):
    """Diviser l'espace en sous espaces carrés tel que tous les points
      appartenant au même cadrant appartiennent à la même composante connexe 
      et travailler avec ces cadrants au lieux de parcourir tous les points"""
    d = dict()                  #Clé : Quadrant, Valeur: list de point appartenant au quadrant clé.
    cote=distance/sqrt(2)
    for pt in points :
        key = (floor(pt.coordinates[0]/cote),floor(pt.coordinates[1]/cote))
        if key in d:
            d[key].append(pt)
        else:
            d[key] = [pt]
    composantes=list()          #Contient les quadrants constituants même une composante connexe
    visited= set()              #Quadrant déjà visité et appartenant à une composante connexe
    for key in d.keys():
        if key in visited :
            continue
        visited.add(key)
        file=list()             # Voisins du quadrant key qu'il faut étudier/visiter
        composante=[key]
        for i in range(-2,3):
            for j in range(-2,3):
                #On test pas pour un quadrant avec lui même ou avec les quadrants dans les 4 coins extrêmes
                if (i==0 and j==0 )or (abs(i)==2 and abs(j)==2):    
                    continue
                flag=0              # Si on trouve deux points des deux quadrants liées, pas la peine de continuer la recherche.
                q=(key[0]+i, key[1]+j)
                if q in visited:
                    continue
                if q in d.keys():
                    for p1 in d[key]:
                        for p2 in d[q]:
                            if p1.distance_to(p2)<=distance:
                                file.append(q)
                                visited.add(q)
                                composante.append(q)
                                flag=1
                                break
                        if flag==1:
                            break
        k = 0
        while k<len(file):
            q=file[k]               # Quadrant de priorité la plus élevée
            for i in range(-2,3):
                for j in range(-2,3):
                    if (i==0 and j==0)or (abs(i)==2 and abs(j)==2):
                        continue
                    flag=0
                    voisin=(q[0]+i, q[1]+j)
                    if voisin in visited:
                        continue
                    if voisin in d.keys():
                        for p1 in d[voisin]:
                            for p2 in d[q]:
                                if p1.distance_to(p2)<=distance:
                                    file.append(voisin)
                                    visited.add(voisin)
                                    composante.append(voisin)
                                    flag=1
                                    break
                            if flag==1:
                                break
            k+=1
        composantes.append(composante)
    res=list()                              # Les tailles des composantes connexes.
    for composante in composantes:
        sum=0
        for q in composante:
            sum+=len(d[q])
        res.append(sum)
    res.sort(reverse=True)
    return res



def main():
    """
    ne pas modifier: on charge une instance et on affiche les tailles
    """
    for instance in argv[1:]:
        distance, points = load_instance(instance)
        print_components_sizes(distance, points)


main()
