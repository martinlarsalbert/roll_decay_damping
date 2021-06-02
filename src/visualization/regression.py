import pandas as pd
from src.df_to_latex import LateXTable
from sympy.physics.vector.printing import vlatex

def results_summary_to_dataframe(results):
    '''take the result of an statsmodel results table and transforms it into a dataframe'''
    pvals = results.pvalues
    coeff = results.params
    conf_lower = results.conf_int()[0]
    conf_higher = results.conf_int()[1]

    results_df = pd.DataFrame({"$P_{value}$":pvals,
                               "coeff":coeff,
                               "$conf_{lower}$":conf_lower,
                               "$conf_{higher}$":conf_higher
                                })
    
    #Reordering...
    results_df = results_df[["coeff","$P_{value}$","$conf_{lower}$","$conf_{higher}$"]]
    return results_df

def result_table(df_results2, caption:str, label:str):
    df_table = df_results2.reset_index()
    df_table = df_table.round(decimals=3)

    df_table['index'] = df_table['index'].apply(lambda x : f'${vlatex(x)}$')

    units={'index':''}

    lt = LateXTable(df_table, rename={'index':'coeff','coeff':'mean'}, 
                caption=caption, label=label, units=units)
    
    return lt