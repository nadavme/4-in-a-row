#############################################################
# FILE : ai.py
# WRITERS :  Nadav_Meidan, nadav.meidan, 200990240
#            Mattan Yeroushalmi, mattan, 312292584
# EXERCISE : intro2cs ex12 2017-2018
# DESCRIPTION : A program that contains automatic player process for a move.
#############################################################
import random


class AI:
    def find_legal_move(self, func, timeout=None):
        """
        Finds a legal move for the AI
        :param func: the function to be called with the move - in our case
        event handler.
        :param timeout: irrelevant since we chose the naive random choice "AI"
        :return: Calls the function event handler or raises an exception if
        there are no possible moves.
        """
        columns = [0, 1, 2, 3, 4, 5, 6]
        random.shuffle(columns)
        for ind in columns:
            try:
                return func(ind, msg=False)
            except Exception: # if "illegal move!" exception is raised.
                continue

        raise Exception('No possible AI moves.')
