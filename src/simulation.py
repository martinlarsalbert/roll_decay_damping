import numpy as np
from scipy.integrate import solve_ivp
import pandas as pd

def get_updater(lambda_phi2d, coeffs):
    
    def updater(t, states):
       
        phi = states[0]
        phi1d = states[1]
            
        parameters = dict(coeffs)
        parameters['phi'] = phi
        parameters['phi1d'] = phi1d            
        phi2d = lambda_phi2d(**parameters)            
        d_states_dt = np.array([phi1d, phi2d])
        return d_states_dt
    
    return updater


def simulate(data, df_results, lambda_phi2d):
    
    coeffs= {str(key):value for key,value in df_results['coeff'].items()}
    updater = get_updater(lambda_phi2d=lambda_phi2d, coeffs=coeffs)
    
    t = data.index
    t_span = [t[0], t[-1]]
    y0 = data.iloc[0][['phi','phi1d']].values
    result = solve_ivp(fun=updater, t_span=t_span, y0=y0, t_eval=t)
    
    df_sim = pd.DataFrame(index=result.t, data=result.y.T, columns = ['phi','phi1d'])
    df_sim['phi2d'] = lambda_phi2d(**coeffs,**df_sim)
    assert result.success
    
    return df_sim