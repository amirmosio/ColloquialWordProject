#!/usr/bin/env python


class MyWeightedFleissKappa:
    def __init__(self, vote_options_count_dict, options_model_scores):
        # Parameters need for tuning
        """
        0.7 is the assumed word2vec model acc,
        and is the probability of model suggesting right options between 9 suggestions
        or the probability of 'none' option being the right answer
        """
        self.assumed_word2vec_acc = 0.7
        self.model_effect_in_vote_coeff = 0.2
        self.min_valid_kappa = 0.25
        """
        state fields
        """
        self.vote_options_count_dict = vote_options_count_dict

        options_model_scores = options_model_scores + [1 - self.assumed_word2vec_acc]
        self.options_model_scores = [round(float(i) / sum(options_model_scores), 3) for i in options_model_scores]

        self.voters_count = sum(list(vote_options_count_dict.values()))
        self.options_count = len(vote_options_count_dict.keys())

        # At this time, model predictions will be considered as people votes
        self.model_effect_in_vote = self.voters_count * self.model_effect_in_vote_coeff

        self.rates = self._calculate_rates_matrix()
        self.kappa = self.calculating_kappa()
        self.acceptable = self.kappa >= self.min_valid_kappa
        self.final_selected_option = self._find_final_selected_option()

    def get_results(self):
        return self.kappa, self.acceptable, self.final_selected_option

    def _find_final_selected_option(self):
        options_vote = [item[0] for item in self.rates]
        max_value = max(options_vote)
        return options_vote.index(max_value)

    def _calculate_rates_matrix(self):
        """
        each option has a yes or no categories, K=2
        """
        K = 2
        N = self.options_count
        rates = [[0 for i in range(K)] for j in range(N)]
        for option, vote in self.vote_options_count_dict.items():
            model_score = self.options_model_scores[option]
            model_yes = self.model_effect_in_vote * model_score
            model_no = self.model_effect_in_vote - model_yes
            rates[option][0] = round(vote + model_yes, 3)
            rates[option][1] = round(self.voters_count - vote + model_no, 3)
        return rates

    def calculating_kappa(self):
        n = self.voters_count + self.model_effect_in_vote
        return self._fleissKappa(self._calculate_rates_matrix(), n)

    @staticmethod
    def _fleissKappa(rate, n):
        '''
        Created on Aug 1, 2016
        @author: skarumbaiah
        Computes Fleiss' Kappa
        Joseph L. Fleiss, Measuring Nominal Scale Agreement Among Many Raters, 1971.
        '''

        def checkInput(rate, n):
            N = len(rate)
            k = len(rate[0])
            assert all(len(rate[i]) == k for i in range(k)), "Row length != #categories)"
            assert all(round(sum(row), 3) == n for row in rate), "Sum of ratings != #raters)"

        N = len(rate)
        k = len(rate[0])
        checkInput(rate, n)

        P_i_list = [(sum([i ** 2 for i in row]) - n) / (n * (n - 1)) for row in rate]
        PA = sum(P_i_list) / N

        PE = sum([j ** 2 for j in [sum([rows[i] for rows in rate]) / (N * n) for i in range(k)]])

        kappa = -float("inf")
        try:
            kappa = (PA - PE) / (1 - PE)
            kappa = float("{:.3f}".format(kappa))
        except ZeroDivisionError:
            print("Expected agreement = 1")

        return kappa


if __name__ == '__main__':
    rate = [
        [3, 4],
        [0, 7],
        [0, 7],
        [0, 7],
        [0, 7],
        [0, 7],
        [0, 7],
        [0, 7],
        [0, 7],
        [4, 3],
    ]
    weighted_fleiss_kappa = MyWeightedFleissKappa({0: 1, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0},
                                                  [0.5, 0.0, 0.11, .0, 0.0, 0.0, 0.0, 0.0, 0.00, 0.00])
    print(weighted_fleiss_kappa.kappa, weighted_fleiss_kappa.final_selected_option, weighted_fleiss_kappa.rates)
