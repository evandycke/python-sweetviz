# coding: utf-8

"""
	Ce script a pour objectif de produire une visualisation avec Sweetviz.
"""

from __future__ import annotations
from threading import Lock, Thread
from typing import Optional

import os, logging
import pandas as pd
import sweetviz as sv

class SweetvizAnalyzeMeta(type): # Définition de la classe SweetvizAnalyzeMeta
    """Classe permettant d'implémenter un Singleton thread-safe"""

    _instance: Optional[SweetvizAnalyze] = None

    _lock: Lock = Lock()
    """On a posé un verrou sur cet objet. Il sera utilisé pour la synchronisation des threads lors du premier accès au Singleton."""

    def __call__(cls, *args, **kwargs):
        # Now, imagine that the program has just been launched. Since there's no
        # Singleton instance yet, multiple threads can simultaneously pass the
        # previous conditional and reach this point almost at the same time. The
        # first of them will acquire lock and will proceed further, while the
        # rest will wait here.
        with cls._lock:
            # The first thread to acquire the lock, reaches this conditional,
            # goes inside and creates the Singleton instance. Once it leaves the
            # lock block, a thread that might have been waiting for the lock
            # release may then enter this section. But since the Singleton field
            # is already initialized, the thread won't create a new object.
            if not cls._instance:
                cls._instance = super().__call__(*args, **kwargs)
        return cls._instance

class SweetvizAnalyze(metaclass=SweetvizAnalyzeMeta): # Définition de la classe SweetvizAnalyze
    """Classe définissant SweetvizAnalyze, qui permettra d'obtenir une visualisation d'un jeu de données"""

    def __init__(self): # Constructeur

        # On configure le logger
        LOG_FORMAT = "%(levelname)s %(asctime)s - %(message)s"
        logging.basicConfig(level=logging.DEBUG, filemode='w', format=LOG_FORMAT)
        formatter = logging.Formatter(LOG_FORMAT)
        self.logger = logging.getLogger('sweetviz')

        # Les logs seront inscrits dans un fichier
        fileHandler = logging.FileHandler("../log/sweetviz.log", mode='w')
        fileHandler.setFormatter(formatter)
        self.logger.addHandler(fileHandler)
        self.logger.info("Logger initialization complete ...")

    def inspect(self):
        """Lance l'inspection du jeu de données"""

        # On charge les données
        df = pd.read_csv('../in/MOCK_DATA.csv')
        self.logger.info("Data loading completed")

        # On analyse les données
        r = sv.analyze(df)
        self.logger.info("Data analysis completed")

        # On affiche le rapport
        r.show_html('../out/myReport.html')

        # On compare les 500 premières lignes avec les 500 dernières
        df1 = sv.compare(df[500:], df[:500])
        df1.show_html('../out/comparaison.html')

if __name__ == "__main__":
	v = SweetvizAnalyze()
	v.inspect()