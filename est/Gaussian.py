import numpy as np
import scipy.stats as st
""" 
Followed this tutorial:
    https://ipython-books.github.io/76-estimating-a-probability-distribution-nonparametrically-with-a-kernel-density-estimation/
This is also useful: 
    https://ipython-books.github.io/76-estimating-a-probability-distribution-nonparametrically-with-a-kernel-density-estimation/
Another kde to check out is scikit-learn:
    https://scikit-learn.org/stable/modules/density.html    
"""    
def GaussianKde(points, X,Y):
    bandFactor = 0.2; # bandwith of Gaussian used
    # Take input swarm object with k many 
    kde = st.gaussian_kde(points, bandFactor);
    # We reshape the grid for the kde() function.
    mesh = np.vstack((X.ravel(), Y.ravel()))
    dim1, dim2 = X.shape
    # We evaluate the kde() function on the grid.
    v = kde(mesh).reshape((dim1, dim2)) 
    # v returns the values of kde at (X,Y)
    return v;
