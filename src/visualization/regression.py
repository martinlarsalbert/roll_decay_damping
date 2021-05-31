import pandas as pd

def results_summary_to_dataframe(results):
    '''take the result of an statsmodel results table and transforms it into a dataframe'''
    pvals = results.pvalues
    coeff = results.params
    conf_lower = results.conf_int()[0]
    conf_higher = results.conf_int()[1]

    results_df = pd.DataFrame({"P>|t|":pvals,
                               "coeff":coeff,
                               "$conf_{lower}$":conf_lower,
                               "$conf_{higher}$":conf_higher
                                })

    #Reordering...
    results_df = results_df[["coeff","P>|t|","$conf_{lower}$","$conf_{higher}$"]]
    return results_df