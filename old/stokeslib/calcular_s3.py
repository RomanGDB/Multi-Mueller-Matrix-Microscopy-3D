import numpy as np

def calcular_s3(S_in, DoP, gamma, thetas, beta):

  # S3 Modulo
  S_in[:,:,:,3,:] = np.sqrt(DoP**2 * S_in[:,:,:,0,:].astype(float)**2 - S_in[:,:,:,1,:].astype(float)**2 - S_in[:,:,:,2,:].astype(float)**2)

  # Calcula cambios de signo
  signos = []
  phis = gamma*np.array(thetas) + beta
  omegas = (phis - thetas) % 360

  for omega in omegas:
    if 0 <= omega < 90:
      signo = 1
    elif 90 <= omega < 180:
      signo = -1
    elif 180 <= omega < 270:
      signo = 1
    elif 270 <= omega < 360:
      signo = -1
    signos.append(signo)

  # Aplicar S3 Signo
  for i, signo in enumerate(signos):
    S_in[:,:,:,3,i] = signo * S_in[:,:,:,3,i]

  return S_in