import numpy as np
import scipy.stats as st
""" 
Followed this tutorial:
    https://ipython-books.github.io/76-estimating-a-probability-distribution-nonparametrically-with-a-kernel-density-estimation/
This is also useful: 
    https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.gaussian_kde.html
Another kde to check out is scikit-learn:
    https://scikit-learn.org/stable/modules/density.html    
"""    
def GaussianKde(points, X,Y):
    bandFactor = 1.0; # bandwith of Gaussian used
    # Take input swarm object with k many 
    kde = st.gaussian_kde(points, bandFactor);
    # We reshape the grid for the kde() function.
    mesh = np.vstack((X.ravel(), Y.ravel()))
    dim1, dim2 = X.shape
    # We evaluate the kde() function on the grid.
    v = kde(mesh).reshape((dim1, dim2)) 
    # v returns the values of kde at (X,Y)
    return v;

def nearestNeighbours(swarm, curDrone, radius):
    neighbours=[];
    for drone in swarm:
        if drone.id != 0:
            if curDrone.distance(drone) < radius:
                neighbours.append(np.array([drone.x(), drone.y()]));
    return neighbours;

class localGaussian:
    def __init__(self, swarm, drone, radius, bandFactor = 0.2):          
        self.bandFactor = 0.2;
        self.cov = np.identity(2)*self.bandFactor;
        neighbours = nearestNeighbours(swarm, drone, radius);
        self.neighbourGauss = [];
        for drone in neighbours:
            self.neighbourGauss.append(st.multivariate_normal(mean=drone, cov = self.cov))
            
    def eval(self, x,y):
        density = 0;
        for gauss in self.neighbourGauss:
            density += gauss.pdf([x,y]);
        
        density = density/len(self.neighbourGauss);
        return density;

    def grad(self,x,y):
        gradient = np.zeros(2);
        pos = np.array([x,y])
        invCov = np.linalg.inv(gradient);
        for gauss in self.neighbourGauss:
            gradient += gauss.pdf(pos)*invCov.dot(pos - gauss.mean);
        
        gradient = gradient/len(self.neighbourGauss);
        return gradient;
            
        
    