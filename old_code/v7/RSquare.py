import numpy as np 
import matplotlib.pyplot as plt

aaaaa = [0.70563148213810711, 0.81682430657459071, 0.067072132347088864, 0.74088625962826571, 0.58238442529459467, 
0.44197242312500484, 0.72715618761980894, 0.81784835695673874, 0.67508667343132978, 0.76686258015743891, 
0.78045447657589095, 0.81104889756864118, 0.80523218718985912, 0.68092790960769811, 0.24035001297636494, 
0.079087421938158209, 0.81683420971881415, 0.39899061654756107, 0.78711975685577873, 0.73217339035452733, 
0.65744678313211447, 0.47352026336298736, 0.87139866225858142, 0.81968689803181183, 0.58205940168259618, 
0.5762402804024167, 0.91732562790428473, 0.91410644976612487, 0.84196550259153158, 0.75281612689602417, 
0.77011860182228142, 0.79244809903201552, 0.10775804102154707, 0.74551991506263393, 0.56043521248253558, 
0.43269296392577283, 0.69747640248931431, 0.81493472530716438, 0.67497202464655026, 0.77257874513965197, 
0.78256490878886842, 0.65416132391306503, 0.4594591689586609, 0.57338346749139735, 0.092597553160961299, 
0.66397961547416018, 0.64516028510139556, 0.70688279029681267, 0.33406781857722956, 0.77660579733447477, 
0.76348672584693267, 0.68850697110554848, 0.76389498128603561, 0.82816236193327875, 0.65049092506544515, 
0.72957897067209387, 0.55821809821164137, 0.67160557195330139, 0.64318742127851047, 0.67942032388007911, 
0.81210972547619864, 0.66518855337634464, 0.77627558397237595, 0.95612424964646758, 0.58559210037542608, 
0.74658918953392395, 0.94686655423098831, 0.57796315140288024, 0.85568787740339425, 0.92775145387759084, 
0.45399412258133787, 0.75972927815305646, 0.80252105673393648, 0.10529076150535144, -0.10315196549478456, 
0.47189065518257811, 0.50361717365112157, 0.53807205185040663, 0.47610264261980872, 0.7817701264489163, 
0.7534028747746736, 0.86383508609410375, 0.85600346069618538, 0.78250877596166268, 0.81183152671303882, 
0.8045071401212941, 0.55289239929977985, 0.11868777040676304, 0.43687570534461417, 0.2815706354790567, 
0.44955315800038242, 0.5391640145326112, 0.046484899634088306, 0.15758459981615447, 0.56540210313569017, 
0.69940839696210455, 0.80412074209614803, 0.83568455982095358, 0.83017233932546641, 0.038534395625384188]
RSquareVec = np.array(aaaaa)
totalGames = len(aaaaa)

plt.plot(range(1, totalGames+1), RSquareVec, 'bo-')
plt.ylabel('R^2 of each linear regression')
plt.xlabel('Game')
plt.savefig('RSquare.eps')
plt.show()